a = [1,2,3,4,5,6,7,8,9,10]

sum = 0
sum1 = 0
for x in a:
    if x % 2 == 0:
        sum = sum + x
    else:
        sum1 = sum1 + x

print("Sum of even number", sum)
print("Sum of odd number", sum1)

#Cach 2
# sum = 0
# sum1 = 0
# for x in range(11):
#     if x % 2 == 0:
#         sum = sum + x
#     else:
#         sum1 = sum1 + x

# print("Sum of even number", sum)
# print("Sum of odd number", sum1)
    