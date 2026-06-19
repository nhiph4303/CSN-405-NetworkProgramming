a = [2,6,9,15,21,28,30,33]
x = float(input())

y = 0
dis = 0
minDis = float('inf')

for i in a:

    dis = abs(x - i)

    if dis < minDis:
        minDis = dis
        y = i

print ("The closest number is", y)
print("Distance is", minDis)
    