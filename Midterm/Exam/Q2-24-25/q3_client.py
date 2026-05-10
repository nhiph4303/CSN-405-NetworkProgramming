import socket

# ✅ TÁI SỬ DỤNG: Setup TCP client (giống Lab4 Q1 client)
HOST = "127.0.0.1"
PORT = 6000

# ✅ TÁI SỬ DỤNG: try/except/finally
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # ✅ TÁI SỬ DỤNG: Nhập và gửi 1 tin nhắn (giống Lab4 Q1 client)
    message = input("Enter message: ")
    client_socket.sendall(message.encode())

    # ✅ TÁI SỬ DỤNG: Nhận và hiển thị phản hồi
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

except Exception as e:
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket — exit gracefully (giống Lab4 Q1)
    client_socket.close()
    print("Client closed.")
