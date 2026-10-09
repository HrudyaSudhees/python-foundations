name = "Hrudya"
print(" Hello", name, " !")

num_1 = int(input("Enter 1st number"))
num_2 = int(input("Enter 2nd number"))
sum = num_1 + num_2
print("Sum of ",num_1, "and ", num_2, "is", sum)

for k in range(1, 11):
    print(k)

nums = [4, 9, 2, 7]
temp = nums[0]
print(temp)
for j in nums:
    if j > temp:
        temp = j
print(temp)

def is_even(n):
    if n%2 == 0:
        return True
    else:
        return False

print(is_even(5))
print(is_even(10))

person = { "name" : "Asha", "age":24}
name_p1 = person["name"]
age_p1 = person["age"]
print(f"{name_p1} is {age_p1} years old.")

word = input("Enter your word: ")
vowels = ["a", "e", "i", "o", "u"]
count = 0
for i in range(len(word)):
    if word[i] in vowels:
        count +=1
print(f"There are {count} vowels in you word.")
