import socket

HOST = "127.0.0.1"
PORT = 5050

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to Quiz server {HOST}:{PORT}")

    while True:
        # Nhận câu hỏi từ server
        question = client_socket.recv(1024).decode()
        print(f"\n[QUIZ] {question}")

        # Kiểm tra server báo kết thúc
        if "Quiz finished" in question or "Goodbye" in question:
            break

        # Nhập câu trả lời
        answer = input("Your answer: ")
        client_socket.sendall(answer.encode())

        # Thoát nếu quit/exit
        if answer in ["quit", "exit"]:
            break

        # Nhận và hiển thị kết quả
        result = client_socket.recv(1024).decode()
        print(f"[RESULT] {result}")

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")
