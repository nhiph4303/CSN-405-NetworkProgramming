import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"[CLIENT] connected {HOST}: {PORT}")

try:
    while True:
        message = input("Enter a message (exit to close): ")
        message = message.encode()
        
        client_socket.sendall(message)
        
        if message.decode() == "exit":
            break
            
        data = client_socket.recv(1024)
        if not data:
            print("Server closed")
            break
        
        print(f"[CLIENT] server replied: ", data.decode())
except Exception as e:
    print(f"[CLIENT] Error: {e}")
finally:
    client_socket.close()