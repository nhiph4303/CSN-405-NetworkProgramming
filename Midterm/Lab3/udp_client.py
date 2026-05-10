import socket

HOST = "127.0.0.1"
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.settimeout(3)
print(f"[CLIENT] UDP connected {HOST}: {PORT}")

try:
    
    while True:
        message = input("Enter a message (exit to close): ")
    
        client_socket.sendto(message.encode(), (HOST, PORT))
        if message == "exit":
            break

        try:
            data, server_add = client_socket.recvfrom(1024)
            if not data:
                print("Server closed")
                break
        except socket.timeout:
            print("Timeout closed")
            break
        print("[CLIENT] Letter 'n' count:", data.decode())

except Exception as e:
    print("Error:", e)

finally:
    client_socket.close()      