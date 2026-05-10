# host = "127.0.0.1"
# port = 5000

# print("Server is running on: ", host, port)
# print("Server is running on: "+ host + " "+ str(port))
# print(f'Server is running on: {host}: {port}')

# x = 3
# y = 10
# print(f'{x} + {y} = {x+y}')

#user input data
#port = int(input("Enter a port: "))
#print(type(port))

#if else
# if 1 <= port < 10000:
#     print("valid port")

# elif port ==0:
#     print("zero")
# else: 
#     print("invalid port")

#loop 
# for i in range(5+1):
#     print("Inter: ", i)


# for i in range(1,6):
#     if i == 3:
#         continue
#     print(i)

#while 
x =1 
while x <= 5:
    print(x)
    x+=1

#Function
def say_hello():
    print("hiii")

say_hello()

def aver(x,y):
    return (x+y) /2

print(aver(4,6))

# list
port = [40,60,22,555]
print(port)

port.append(80)
print(port)
for p in port:
    print("port", p)

#tuple 
coor = (10,20)
socket = ("127.0.0.1", 8000)
host , port = socket
print("Host", host)

#dic
packet = {"src" : "A", "dst" : "B", "size" : 100}
packet["length"] = 500
packet["size"] += 50

del packet["size"]

for key, value in packet.items():
    print(f'{key}:{value}')

#xu li chuoi
text = 'python'
print(text[::-1])