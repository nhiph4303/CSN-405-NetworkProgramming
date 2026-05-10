import socket

HOST = "127.0.0.1"
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5) 

print(f"[CLIENT] UDP Client ready to send to {HOST}:{PORT}")

try:
    while True:
        message = input("Enter text (type 'exit' to quit): ").strip()

        if not message:
            continue

        client_socket.sendto(message.encode(), (HOST, PORT))

        if message.lower() == "exit":
            break

        try:
            data, server_address = client_socket.recvfrom(1024)
            print(f"[CLIENT] Number of 'n' found: {data.decode()}")
        except socket.timeout:
            print("[CLIENT] Error: Response timeout from server.")

except Exception as e:
    print(f"[CLIENT] Error: {e}")
finally:
    print("[CLIENT] Closing client socket...")
    client_socket.close()