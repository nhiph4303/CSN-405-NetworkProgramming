import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] TCP connected to {HOST}:{PORT}")

    while True:
        message = input("Enter text (type 'exit' to quit): ").strip()

        if not message:
            continue

        client_socket.sendall(message.encode())

        if message.lower() == "exit":
            break

        data = client_socket.recv(1024)
        print(f"[CLIENT] Number of 'n' found: {data.decode()}")

except Exception as e:
    print(f"[CLIENT] Error: {e}")
finally:
    print("[CLIENT] Closing socket...")
    client_socket.close()