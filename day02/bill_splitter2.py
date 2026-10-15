
import sqlite3
from pathlib import Path


people = []
expenses = []
#define connections
DB_FILE = Path(__file__).with_name("bill_splitter.db")
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
    
conn = sqlite3.connect("bill_splitter.db")
with open("bill_splitter_setup.sql", "r") as file:
    sql_script = file.read()
conn.executescript(sql_script)
conn.close()

def add_people():
    global people
    name = input ("Enter name: ").strip()

    conn = sqlite3.connect("bill_splitter.db")
    cursor = conn.cursor()

    cursor.execute(
    'INSERT INTO people (name) VALUES (?)',
        (name,)
    )
    conn.commit()
    conn.close()

    print("Person added successfully")

add_people()



'''
def load_data():
    global people, expenses
    try:
        with open(DATA_FILE,"r", encoding = "utf-8") as file:
            data = json.load(file)
        people = data.get("people",[])
        expenses = data.get("expenses",[])
        print("Saved data loaded successfully.")
    except FileNotFoundError:
        people = []
        expenses= []
        print("Starting with empty data.")

def save_data():
    data = {
        "people": people,
        "expenses": expenses
        }

    with open(DATA_FILE, "w", encoding ="utf-8") as file:
        json.dump(data, file, indent=4)
    print("Data saved susccessfully.")
def add_people():
    name  = input("Enter name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    if any(person.casefold() == name.casefold()
            for person in people):
            print(f"{name} already exists.")
            return
    people.append(name)
    save_data()
    print("Person added successfully..")

#selected_people=[]
def split_expense(amount):
    if not people:
        print("Add people before splitting an expense.")
        return None
    global selected_people
    selected_people = []
    print("Select people to split expense")
    for i, person in enumerate(people, start =1):
        print(f"{i}. {person}")

    choices = input("Choose names for split(by giving there corresponding numbers separated by space): ").split()

    for choice in choices:
        if not choice.isdigit():
            print(f"Invalid input: {choice}")
            continue
        index = int(choice)-1
        if not 0<= index < len(people):
            print(f"Invalid selection: {choice}")
            continue
        person = people[index]

        if person not in selected_people:
            selected_people.append(person)
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

def view_balance():
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- Saved Expenses ---")

    for expense in expenses:
        print(f"\nExpense: {expense['expense_name']}")
        print(f"Amount: Rs. {expense['amount']:.2f}")
        print(f"Paid by: {expense['paid_by']}")
        print(f"Participants: {', '.join(expense['selected_people'])}")
        print(f"Share per person: Rs. {expense['share']:.2f}")

load_data()
while True:
    num = int(input(" 1. Add people \n 2. Split expense \n 3. View balance \n 4. Exit  \n Choose an option "))
    match num:
        case 4:
            break
        case 1:
            result = add_people()
            print(people)
        case 2:
            if not people:
                print("Add people first")
                continue

            exp_name = input("Enter expense name: ").strip()
            amount =int(input("Enter amount to be split: Rs. "))
            paid_by = input("Who paid? ")
            print(f"Expense name: {exp_name} \nAmount: Rs. {amount} \nPaid by: {paid_by}")
            payer = next(
                (p for p in people
                 if p.casefold() == paid_by.casefold()),
                None
            )

            if payer is None:
                print("Payer must be someone in the people list.")
                continue

            result = split_expense(amount)

            if result is not None:
                selected_people, share = result

                expenses.append({
                    "expense_name": exp_name,
                    "amount": amount,
                    "paid_by": payer,
                    "selected_people": selected_people,
                    "share": share
                })

                save_data()
        case 3:
            view_balance() 
        case _:
            print("Choose an option from 1 to 4")

print("Loop finished!")
'''
