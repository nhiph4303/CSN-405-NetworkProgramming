x = 3
y = 10
print(f"{x} + {y} = {x+y}")

# Exercise
# Exercise 1
x = 15
y = 30
z = x + y

print(z)

# Exercise 2
x = 10.5
y = 5
z = x + y

print("The value of x is:", z)
print("Type of x is: ", type(z))

# Exercise 3
num1 = 2
num2 = 5
num3 = 1.5
num4 = 4

result = num1 * num2 * num3 * num4

print("The value of result is:", result)
print("Type of result is:", type(result))

# Lab1
# Assignment 1
x = int(input("Enter an integer x: "))
y = int(input("Enter an integer y: "))

total = x + y

print(f"The sum of {x} and {y} is: {total}")

# Asignment 2
x = float(input("Enter a float number (x): "))
y = int(input("Enter an integer (y): "))

z = (x + y) / 2

print(f"The average (z) is: {z}")
print(f"The data type of z is: {type(z)}")

# Assignment 3
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

sum_even = 0
sum_odd = 0

for num in numbers:
    if num % 2 == 0:
        sum_even += num
    else:
        sum_odd += num

print(f"The sum of even numbers is: {sum_even}")
print(f"The sum of odd numbers is: {sum_odd}")

# Assignment 4
arr = [2, 6, 9, 15, 21, 28, 30, 33]

user_input = float(input("Enter any number: "))

closest_num = arr[0]
min_distance = abs(arr[0] - user_input)

for num in arr:
    current_distance = abs(num - user_input)

    if current_distance < min_distance:
        closest_num = num
        min_distance = current_distance

print(f"The closest number to {user_input} is: {closest_num}")
print(f"The distance is: {min_distance}")

# Assignment 5
student = {"name": "Phan Ngọc Hạnh Nhi", "course": "CSE306", "point": 0}

student["GPA"] = 3.2

del student["point"]
print(student)
