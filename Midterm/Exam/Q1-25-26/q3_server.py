import socket
import threading   # 🆕 THREADING: thêm để xử lý nhiều client

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Lab4 Q2 server)
HOST = "127.0.0.1"
PORT = 5000

# 🆕 THREADING: Tách toàn bộ logic Q2 vào hàm riêng
# Mỗi thread sẽ gọi hàm này để phục vụ 1 client độc lập
def handle_client(client_socket, client_add):
    client_ip   = client_add[0]
    client_port = client_add[1]

    try:
        # ✅ TÁI SỬ DỤNG: Nhận tên client + lưu IP/port (giống Lab4 Q2)
        client_name = client_socket.recv(1024).decode()
        print(f"Client connected: {client_name} from {client_ip}:{client_port}")

        # ✅ TÁI SỬ DỤNG: Vòng lặp nhận phép tính vô tận (giống Lab4 Q2)
        while True:
            data = client_socket.recv(1024).decode()
            if data in ["quit", "exit"]:
                break
            print(f"Received from {client_name}: {data}")

            # ✅ TÁI SỬ DỤNG: Tính toán bằng eval() + xử lý lỗi (giống Lab4 Q2)
            try:
                result = eval(data)                            # eval("12 + 42") → 54
                client_socket.sendall(str(result).encode())
            except ZeroDivisionError:                          # e.g. 6 / 0
                client_socket.sendall("Error: Division by zero".encode())
            except:
                client_socket.sendall("Error: Invalid expression".encode())

    except Exception as e:
        print(f"Error with {client_add}: {e}")
    finally:
        # ✅ TÁI SỬ DỤNG: Đóng socket client khi xong
        client_socket.close()
        print(f"[SERVER] Client {client_add} disconnected.")

# ✅ TÁI SỬ DỤNG: Setup TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)   # 🆕 THREADING: tăng lên 5 để chấp nhận nhiều client chờ
print(f"[SERVER] The server is listening ...")

try:
    # 🆕 THREADING: Vòng lặp vô tận — mỗi accept() tạo 1 thread mới
    while True:
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")

        # 🆕 THREADING: Tạo và start thread riêng cho mỗi client
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()   # server tiếp tục accept client mới ngay sau đây

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()

