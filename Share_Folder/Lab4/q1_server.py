import socket

HOST = "127.0.0.1"
PORT = 6000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[Server] Server running on {HOST}:{PORT}")

try:
    client_socket, client_add = server_socket.accept()
    client_ip   = client_add[0]
    client_port = client_add[1]
    
    print(f"[LOG] Client connected: {client_ip}:{client_port}")
    
    data = client_socket.recv(1024).decode()
    
    print(f"[LOG] Received: '{data}' from {client_ip}:{client_port}")
    
    processed = data[::-1].upper() + f" ({client_ip}:{client_port})"
    
    print(f"[LOG] Sending back: '{processed}'")
    
    client_socket.sendall(processed.encode())

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    server_socket.close()
    print("Server closed.")
