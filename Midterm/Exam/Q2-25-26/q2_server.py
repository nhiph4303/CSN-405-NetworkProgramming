import socket
import random   # ← MỚI: sinh số ngẫu nhiên

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Lab4 Q1/Q2 server)
HOST = "127.0.0.1"
PORT = 2026     # ← ĐỀ YÊU CẦU: port 2026

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[SERVER] The server is listening on {HOST}:{PORT}")

# ✅ TÁI SỬ DỤNG: try/except/finally (giống mọi bài lab)
try:
    client_socket, client_add = server_socket.accept()
    print(f"[SERVER] Client connected from {client_add}")

    # ← MỚI: Sinh số ngẫu nhiên khi client kết nối
    target = random.randint(1, 100)
    attempts = 0   # ← MỚI: Đếm số lần đoán

    while True:
        data = client_socket.recv(1024).decode().strip()

        # ✅ TÁI SỬ DỤNG: Xử lý quit/exit (giống Lab3/Lab4)
        if data in ["quit", "exit"]:
            client_socket.sendall("Goodbye!".encode())
            break

        # 🆕 MỚI: Chuyển sang số nguyên và tăng đếm lần đoán
        guess = int(data)
        attempts += 1

        if guess > target:
            client_socket.sendall("Too high! Try again.".encode())
        elif guess < target:
            client_socket.sendall("Too low! Try again.".encode())
        else:
            # 🆕 MỚI: Thông báo thắng kèm số lần đoán
            msg = f"Congratulations! You guessed correctly in {attempts} attempts!"
            client_socket.sendall(msg.encode())
            break

except Exception as e:
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket trong finally
    client_socket.close()
    server_socket.close()
    print("Server closed.")
