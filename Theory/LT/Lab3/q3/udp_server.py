import socket

HOST = "127.0.0.1"
PORT = 5001  

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[SERVER] UDP Server is running on {HOST}:{PORT}")

try:
    while True:
        data, client_address = server_socket.recvfrom(1024)
        
        message = data.decode().strip()
        print(f"[SERVER] Received: {message} from {client_address}")

        if message.lower() == "exit":
            print(f"[SERVER] Client {client_address} requested to exit.")
            continue 

        count_n = message.lower().count('n')
        
        server_socket.sendto(str(count_n).encode(), client_address)

except Exception as e:
    print(f"[SERVER] Error: {e}")
finally:
    print("[SERVER] Closing server socket...")
    server_socket.close()