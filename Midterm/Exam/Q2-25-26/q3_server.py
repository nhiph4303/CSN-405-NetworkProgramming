import socket
import random      # ✅ TÁI SỬ DỤNG: sinh số ngẫu nhiên (từ Q2)
import threading   # 🆕 THREADING: thêm để xử lý nhiều client

HOST = "127.0.0.1"
PORT = 2026

# 🆕 THREADING: Tách logic xử lý client thành hàm riêng
# Mỗi thread sẽ gọi hàm này để phục vụ 1 client độc lập
def handle_client(client_socket, client_add):
    try:
        print(f"[SERVER] Client connected from {client_add}")

        # ✅ TÁI SỬ DỤNG: Logic game từ Q2 — giữ nguyên hoàn toàn
        target = random.randint(1, 100)
        attempts = 0

        while True:
            data = client_socket.recv(1024).decode().strip()

            if data in ["quit", "exit"]:
                client_socket.sendall("Goodbye!".encode())
                break

            guess = int(data)
            attempts += 1

            if guess > target:
                client_socket.sendall("Too high! Try again.".encode())
            elif guess < target:
                client_socket.sendall("Too low! Try again.".encode())
            else:
                msg = f"Congratulations! You guessed correctly in {attempts} attempts!"
                client_socket.sendall(msg.encode())
                break

    except Exception as e:
        print(f"Error with {client_add}: {e}")
    finally:
        # ✅ TÁI SỬ DỤNG: Đóng socket client khi xong
        client_socket.close()
        print(f"[SERVER] Client {client_add} disconnected.")

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Q2)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)   # 🆕 THREADING: tăng lên 5 để chấp nhận nhiều client chờ
print(f"[SERVER] The server is listening on {HOST}:{PORT}")

try:
    # 🆕 THREADING: Vòng lặp vô tận — mỗi accept tạo 1 thread mới
    while True:
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")

        # 🆕 THREADING: Tạo thread — target=handle_client, args=(conn, addr)
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()   # 🆕 THREADING: Start thread → server tiếp tục accept client mới

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()


