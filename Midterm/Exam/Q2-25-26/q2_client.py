import socket

# ✅ TÁI SỬ DỤNG: Setup TCP client (giống Lab4 Q1/Q2 client)
HOST = "127.0.0.1"
PORT = 2026     # ← ĐỀ YÊU CẦU: port 2026

# ✅ TÁI SỬ DỤNG: try/except/finally
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to {HOST}:{PORT}")
    print("[CLIENT] Guess a number between 1 and 100!")

    # ✅ TÁI SỬ DỤNG: vòng lặp gửi/nhận (giống Lab4 Q2)
    while True:
        # 🆕 MỚI: Nhập số đoán thay vì text
        guess = input("Enter your guess: ")

        if guess in ["quit", "exit"]:
            client_socket.sendall(guess.encode())
            break

        client_socket.sendall(guess.encode())

        # Nhận phản hồi từ server
        response = client_socket.recv(1024).decode()
        print(f"[SERVER] {response}")

        # 🆕 MỚI: Thoát khi đoán đúng (khác các bài lab trước)
        if "Congratulations" in response:
            break

except Exception as e:
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket trong finally
    client_socket.close()
    print("Client closed.")
