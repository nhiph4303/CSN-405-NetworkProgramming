import socket

#create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#get local machine name
host = '127.0.0.1'
port = 9999


#connect to the server
client_socket.connect((host, port))
print("Connected to server!")

while True:
    #receive data from server
    data = client_socket.recv(1024).decode('utf-8')   

    #print received message
    print("Server: ", data) 

    #send response to server
    message = input("Client: ")
    client_socket.send(message.encode('utf-8'))  

    #check for exit command
    if message == 'exit':
        break

#close the connection
client_socket.close()