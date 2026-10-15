bill_amount = int(input("Enter your bill amount: "))
tip_percent = int(input("Enter the tip percent: "))
people = int(input("Enter the number of people: "))
pattern = "=" * 30
tip = (tip_percent /100)*bill_amount
total_amt = bill_amount + tip
each_pays = total_amt/people
print(f"Tip amount paid is: {tip:.2f}")
print(f"Total amount paid with tip is: {total_amt:.2f}")
print(f"Amount each person should pay is: {each_pays:.2f}")
