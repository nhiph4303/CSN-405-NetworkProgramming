import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

questions = [
    ("Port 80 is used for HTTP.", True),
    ("TCP is a connection-oriented protocol.", True),
    ("UDP guarantees delivery of packets.", False),
    ("Socket needs a tuple HOST and PORT", True),
    ("IPv4 is the only IP can be assigned for computer", False),
]

# Hàm xử lý mỗi client — chạy trong thread riêng
def handle_client(client_socket, client_add):
    client_ip   = client_add[0]
    client_port = client_add[1]

    try:
        print(f"[SERVER] Client connected from {client_ip}:{client_port}")

        # Gửi từng câu hỏi cho client
        for question, correct_answer in questions:
            client_socket.sendall((question + " (true/false): ").encode())

            # Nhận câu trả lời
            answer = client_socket.recv(1024).decode().strip().lower()
            print(f"[SERVER] Received from {client_ip}:{client_port}: {answer}")

            # Kiểm tra quit/exit
            if answer in ["quit", "exit"]:
                client_socket.sendall("Goodbye".encode())
                return

            # Kiểm tra đúng/sai
            if (answer == "true") == correct_answer:
                client_socket.sendall("Yes, it's correct!".encode())
            else:
                client_socket.sendall("No, it's wrong!".encode())

        # Hết câu hỏi
        client_socket.sendall("Quiz finished!".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print(f"[SERVER] Client {client_ip}:{client_port} disconnected.")

# Setup server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"[SERVER] The server is listening on {HOST}:{PORT} ...")

try:
    while True:
        # Mỗi accept() tạo ra 1 socket mới cho client đó
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")

        # Tạo thread riêng cho mỗi client
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()
