from socket import *
from cryptography.fernet import Fernet

key = b"_dzp0nR00VLZLesW_cv3tcWTzn_hhsA9BSXc0rSDEpM="
f = Fernet(key)

server_port = 3000
server_host = "127.0.0.1"
server_socket = socket(AF_INET, SOCK_STREAM)

server_socket.bind((server_host, server_port))
server_socket.listen(5)
print("Waiting for a connection...")

while True:
    connection_socket, addr = server_socket.accept()
    print("Connection from: ", addr)

    while True:
        data = connection_socket.recv(1024)
        decrypted_message = f.decrypt(data).decode("utf-8")
        print("Client message: ", decrypted_message)
        connection_socket.close()
