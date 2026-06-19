import socket
from cryptography.fernet import Fernet

key = b"_dzp0nR00VLZLesW_cv3tcWTzn_hhsA9BSXc0rSDEpM="
f = Fernet(key)

server_port = 3000

client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", server_port))
print("Connected to the server.")

while True:
    user_data = input("[CLIENT] Enter a message to send (or 'exit' to quit): ")

    if user_data.lower() == "exit":
        break
    message = user_data
    if message.lower() == "exit":   
        break

    encrypted_message = f.encrypt(message.encode())
    client_socket.sendall(encrypted_message)
    print("[CLIENT] Encrypted message sent to the server.")

client_socket.close()
print("Connection closed.")
exit()
