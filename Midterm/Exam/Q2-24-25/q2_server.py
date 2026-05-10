import socket
import threading   # ✅ TÁI SỬ DỤNG: multi-threading (giống Lab4 Q3)

HOST = "127.0.0.1"
PORT = 6000

# ✅ TÁI SỬ DỤNG: Hàm handle_client chạy trong thread riêng (giống Lab4 Q3)
def handle_client(client_socket, client_add):
    client_ip   = client_add[0]
    client_port = client_add[1]

    try:
        # ✅ TÁI SỬ DỤNG: Nhận tin nhắn từ client (giống Lab4 Q1)
        message = client_socket.recv(1024).decode()

        # 🆕 LOG: Ghi log nhận được (đề yêu cầu log)
        print(f"[LOG] Received from {client_ip}:{client_port} → {message}")

        # ✅ TÁI SỬ DỤNG: Đảo ngược + HOA + thêm IP:port (giống Lab4 Q1)
        response = message[::-1].upper() + f" ({client_ip}:{client_port})"

        client_socket.sendall(response.encode())

        # 🆕 LOG: Ghi log phản hồi đã gửi (đề yêu cầu log)
        print(f"[LOG] Sent to {client_ip}:{client_port} → {response}")

    except Exception as e:
        print(f"Error with {client_add}: {e}")
    finally:
        # ✅ TÁI SỬ DỤNG: Đóng socket khi xong
        client_socket.close()

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Lab3/Lab4)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)   # ✅ TÁI SỬ DỤNG: listen(5) giống Lab4 Q3
print(f"[SERVER] The server is listening on {HOST}:{PORT} ...")

try:
    # ✅ TÁI SỬ DỤNG: Vòng lặp accept → Thread → start (giống Lab4 Q3)
    while True:
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")

        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()
