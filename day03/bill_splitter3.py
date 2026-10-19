import os
import psycopg
from pathlib import Path
from dotenv import load_dotenv
from psycopg import IntegrityError

load_dotenv(Path(__file__).with_name(".env"))

SQL_FILE = Path(__file__).with_name("bill_splitter_setup.sql")

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured.")

    return psycopg.connect(database_url)


def initialize_database():
    conn = get_connection()

    try:
        with open(SQL_FILE, "r", encoding="utf-8") as file:
            sql_script = file.read()

        with conn.cursor() as cursor:
            cursor.execute(sql_script, prepare=False)

        conn.commit()
        print("Database initialized successfully.")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def add_people():
    name  = input("Enter name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    conn = get_connection()

    try:
        with conn:
            conn.execute(
                "INSERT INTO people (name) VALUES (%s)",
                (name,)
            )

        print("Person added successfully.")

    except IntegrityError as error:
        if error.sqlstate == "23505":
            print(f"{name} already exists.")
        else:
            print(f"Could not add person: {error}")

    finally:
        conn.close()

def get_people():
    conn = get_connection()

    try:
        cursor = conn.execute(
            "SELECT id, name FROM people ORDER BY id"
        )
        return cursor.fetchall()

    finally:
        conn.close()


def view_people():
    people = get_people()

    if not people:
        print("No people added yet.")
        return

    print("\n--- People ---")

    for person_id, name in people:
        print(f"{person_id}. {name}")

def split_expense(amount, people):

    if not people:
        print("Add people before splitting an expense.")
        return None

    print("Select people to split expense")
    for index, (person_id, name) in enumerate(people, start =1):
        print(f"{index}. {name}")

    choices = input("Enter participant numbers separated by space): ").split()

    selected_people= []

    for choice in choices:
        if not choice.isdigit():
            print(f"Invalid input: {choice}")
            continue
        index = int(choice)-1
        if not 0<= index < len(people):
            print(f"Invalid selection: {choice}")
            continue
        person_id, name = people[index]

        if person_id not in [
            selected_id for selected_id, _ in selected_people
        ]:
            selected_people.append((person_id, name))

    if not selected_people:
        print("No valid people selected.")
        return None

    permission =input("Split amount equally? Y/N ").strip().upper()

    if permission != "Y":
        print("Split cancelled. \nGoing back to main menu")
        return None
    share = amount/len(selected_people)
    print(f"RS.{share} split between {len(selected_people)} people")
    return selected_people, share

def add_expense():
    people = get_people()

    if not people:
        print("Add people first.")
        return

    expense_name = input("Enter expense name: ").strip()

    if not expense_name:
        print("Expense name cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: Rs. "))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

    except ValueError:
        print("Enter a valid amount.")
        return

    paid_by_name = input("Who paid? ").strip()

    if not paid_by_name:
        print("Payer name cannot be empty.")
        return

    # Find the payer's database ID.
    conn = get_connection()

    try:
        payer = conn.execute(
            "SELECT id, name FROM people WHERE name = %s",
            (paid_by_name,)
        ).fetchone()

    finally:
        conn.close()

    if payer is None:
        print("Payer must be someone in the people list.")
        return

    payer_id, payer_name = payer

    print(
        f"\nExpense: {expense_name}"
        f"\nAmount: Rs. {amount:.2f}"
        f"\nPaid by: {payer_name}"
    )

    result = split_expense(amount, people)

    if result is None:
        return

    selected_people, share = result

    conn = get_connection()

    try:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO expenses
                    (expense_name, amount, paid_by)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (expense_name, amount, payer_id)
            )

            expense_id = cursor.fetchone()[0]

            participant_rows = [
                (expense_id, person_id, share)
                for person_id, _ in selected_people
            ]
            with conn.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO expense_participants
                        (expense_id, person_id, share)
                    VALUES (%s, %s, %s)
                    """,
                    participant_rows
                )

        print("Expense saved successfully.")

    except psycopg.Error as error:
        print(f"Could not save expense: {error}")

    finally:
        conn.close()

def view_balance():
    people = get_people()

    if not people:
        print("No people added yet.")
        return

    print("\n--- Select Person ---")

    for index, (_, name) in enumerate(people, start=1):
        print(f"{index}. {name}")

    try:
        choice = int(
            input("Select person to see their balance: ")
        )

    except ValueError:
        print("Enter a valid number.")
        return

    if not 1 <= choice <= len(people):
        print("Invalid selection.")
        return

    user_id, user_name = people[choice - 1]

    conn = get_connection()

    try:
        transactions = conn.execute(
            """
            SELECT
                e.id,
                e.expense_name,
                e.amount,
                e.paid_by,
                payer.name,
                ep.share,
                (
                    SELECT COUNT(*)
                    FROM expense_participants AS ep2
                    WHERE ep2.expense_id = e.id
                ) AS participant_count
            FROM expenses AS e
            JOIN people AS payer ON payer.id = e.paid_by
            LEFT JOIN expense_participants AS ep
                ON ep.expense_id = e.id
                AND ep.person_id = %s
            WHERE e.paid_by = %s
               OR ep.person_id IS NOT NULL
            ORDER BY e.id
            """,
            (user_id, user_id)
        ).fetchall()

        if not transactions:
            print(
                f"{user_name} has not made any transactions yet."
            )
            return

        print(f"\n--- Transactions of {user_name} ---")

        for (
            expense_id,
            expense_name,
            amount,
            payer_id,
            payer_name,
            share,
            participant_count
        ) in transactions:

            if payer_id == user_id:
                if share is None:
                    gets_back = amount

                else:
                    gets_back = (
                        share * (participant_count - 1)
                    )

                if gets_back > 0:
                    print(
                        f"{expense_name}: {user_name} "
                        f"gets back Rs. {gets_back:.2f} "
                        f"from the other participants."
                    )

                else:
                    print(
                        f"{expense_name}: {user_name} "
                        "owes nothing to themselves."
                    )

            elif share is not None:
                print(
                    f"{expense_name}: {user_name} owes "
                    f"Rs. {share:.2f} to {payer_name}."
                )

    finally:
        conn.close()

def main():
    initialize_database()

    while True:
        print(
            f"\n{'=' * 20}"
            "\n     MAIN MENU"
            f"\n{'=' * 20}"
        )

        print(
            "1. Add people\n"
            "2. Split expense\n"
            "3. View balance\n"
            "4. View people\n"
            "5. Exit"
        )

        try:
            num = int(input("Choose an option: "))

        except ValueError:
            print("Please enter a number from 1 to 6.")
            continue

        match num:
            case 1:
                print("\n--- Add People ---")
                add_people()

            case 2:
                print("\n--- Split Expenses ---")
                add_expense()

            case 3:
                print("\n--- View Balance ---")
                view_balance()

            case 4:
                view_people()

            case 5:
                break

            case _:
                print("Choose an option from 1 to 6.")

    print("Loop finished!")


if __name__ == "__main__":
    main()