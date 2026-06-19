import socket

HOST = "127.0.0.1"
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[Server] UDP Server is running on {HOST}: {PORT}")


try:
    while True: 
        data, client_add = server_socket.recvfrom(1024)
        data = data.decode()
        print("[SERVER] received from: " ,client_add, data)
    
        if data == "exit":
            print("[SEVER] client is closed")
            break
        
        # reply = data.upper().encode()
        # server_socket.sendto(reply, client_add)

        count = data.count('n')
        server_socket.sendto(str(count).encode(), client_add)

except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
    print("Server closed.")
    