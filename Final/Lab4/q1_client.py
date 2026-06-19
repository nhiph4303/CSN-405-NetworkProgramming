import socket

HOST = "127.0.0.1"
PORT = 6000

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to {HOST}:{PORT}")
    
    message = input("Enter message: ")
    client_socket.sendall(message.encode())
    
    response = client_socket.recv(1024).decode()
    print(f"[CLIENT] Server response: {response}")

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")
