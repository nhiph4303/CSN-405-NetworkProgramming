import socket

HOST = "127.0.0.1"
PORT = 5050

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to Quiz server {HOST}:{PORT}")

    while True:
        server_msg = client_socket.recv(1024).decode()

        print(f"\n{server_msg}")

        if "Quiz finished" in server_msg or "Goodbye" in server_msg:
            break

        answer = input("Your answer: ")
        client_socket.sendall(answer.encode())

        if answer in ["quit", "exit"]:
            break

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")