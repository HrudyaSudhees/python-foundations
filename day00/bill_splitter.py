'''bill_amount = int(input("Enter your bill amount: "))
tip_percent = int(input("Enter the tip percent: "))
people = int(input("Enter the number of people: "))
pattern = "=" * 30
tip = (tip_percent /100)*bill_amount
total_amt = bill_amount + tip
each_pays = total_amt/people
print(f"Tip amount paid is: {tip:.2f}")
print(f"Total amount paid with tip is: {total_amt:.2f}")
print(f"Amount each person should pay is: {each_pays:.2f}")
text1 = "SPLIT PAYMENTS"
print(f"{pattern} \n {text1: ^14} \n{pattern}")
'''
people = []
expenses = []
def add_people():
    name  = input("Enter name: ")
    people.append(name)
    print("Person added successfully..")
    return people
    
selected_people=[]
def split_expense():
    print("Select people to split expense")
    for i in range (len(people)):
        print(f"{i+1}. {people[i]}")
    choices = input("Choose names for split: ").split()
    #selected_people = []

    for choice in choices:
        if choice.isdigit():
            index = int(choice)-1
            if 0<= index < len(people):
                person = people[index]

                if person not in selected_people:
                    selected_people.append(person)
            else:
                print("invalid selection")
        else:
            print(f"invalid input {choice}")

    permission =input("Split amount equally? Y/N ")
    if permission.upper() == "Y":
        split_amt = amount/len(selected_people)
        print(f"RS.{split_amt} split between {len(selected_people)} people")
    else:
        return
    return split_amt
def view_balance():
    user = people[0]
    if not people:
        print("no people added yet")
        return
    else:
        if paid_by.strip().casefold() == people[0].strip().casefold():
            except_user = len(selected_people)-1
            amt_to_get = individual_amt * (except_user)
            print(f"{user} gets back Rs. {amt_to_get}")
        else:
            print(f"{user} must pay {individual_amt} to {paid_by}")

while True:
    num = int(input(" 1. Add people \n 2. Split expense \n 3. View balance \n 4. Exit \n Choose an option "))
    match num:
        case 4:
            break
        case 1:
            result = add_people()
            print(people)
        case 2:
            exp_name = input("Enter expense name: ")
            amount =int(input("Enter amount to be split: Rs. "))
            paid_by = input("Enter who paid the amount: ")
            print(f"Expense name: {exp_name} \nAmount: Rs. {amount} \nPaid by: {paid_by}")
            individual_amt = split_expense()
        case 3:
            view_balance() 

print("Loop finished!")
