import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"[CLIENT] connected {HOST}: {PORT}")

while True:
    message = input("Enter a message (exit to close): ")
    message = message.encode()
    
    client_socket.sendall(message)
    
    data = client_socket.recv(1024)
    if not data:
        print("Server closed")
        break
    
    print(f"[CLIENT] server replied: ", data.decode())

client_socket.close()