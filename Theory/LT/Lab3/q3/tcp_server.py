import socket

HOST = "127.0.0.1"
PORT = 5000 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[SERVER] TCP Server is running on {HOST}:{PORT}")
print("Waiting for connection...")

try:
    client_socket, client_address = server_socket.accept()
    print(f"[SERVER] Client connected: {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode().strip()
        print(f"[SERVER] Received: {message} from {client_address}")

        if message.lower() == "exit":
            print("[SERVER] Client requested to close.")
            break

        count_n = message.lower().count('n')
        client_socket.sendall(str(count_n).encode())

except Exception as e:
    print(f"[SERVER] Error: {e}")
finally:
    print("[SERVER] Closing connection...")
    if 'client_socket' in locals():
        client_socket.close()
    server_socket.close()