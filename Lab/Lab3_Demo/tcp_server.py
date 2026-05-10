import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[Server] Server is running on {HOST}: {PORT}")

#accept
client_socket, client_add = server_socket.accept()
print(f"[SEVER] client is connected: ", client_add)
print(client_socket)

while True: 
    data = client_socket.recv(1024)

    data = data.decode()
    print("[SEVER] received: ", data)
    
    if data == "exit":
        print("[SEVER] client is closed")
        break
    reply = data.upper().encode()
    client_socket.sendall(reply)

client_socket.close()
server_socket.close()
