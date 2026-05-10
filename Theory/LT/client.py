from socket import *

server_port = 2027

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect(('127.0.0.1', server_port))
print("Connected to the server.")

while True:
    user_data = input("Enter a message: ")

    if user_data.lower() == 'exit':
        print("Closing client...")
        break

    client_socket.send(user_data.encode())

    server_reply = client_socket.recv(1024).decode()
    print(server_reply)

client_socket.close()
exit()