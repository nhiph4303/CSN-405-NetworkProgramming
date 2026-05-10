import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[SERVER] TCP Server is running on {HOST}: {PORT}")
print("Waiting for connection...")

client_socket, client_add = server_socket.accept()

print(f"[SERVER] Client is connected: ", client_add)
print(client_socket)

while True: 
    data = client_socket.recv(1024)

    if not data: 
        print("[SERVER] Client disconnected")
        break

    data = data.decode().strip()

    print("[SERVER] Received: ", data, "from " , client_add)
    
    if data.lower() == "exit":
        print("[SERVER] Client is closed")
        break
    
    reply = data.upper().encode()

    client_socket.sendall(reply)

client_socket.close()
server_socket.close()
