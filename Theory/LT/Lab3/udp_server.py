import socket

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[SERVER] UDP Server is running on {HOST}: {PORT}")

while True: 
    data, client_add = server_socket.recvfrom(1024)
    
    data = data.decode().strip()
    print("[SERVER] Received: " , data ,"from ",client_add)
    
    if data.lower() == "exit":
        print("[SERVER] Client is closed")
        break
    reply = data.upper().encode()
    server_socket.sendto(reply, client_add)

server_socket.close()
    