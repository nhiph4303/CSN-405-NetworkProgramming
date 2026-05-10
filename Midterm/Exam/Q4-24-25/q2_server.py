import socket
import datetime   # 🆕 MỚI: lấy ngày/giờ hiện tại

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Lab3/Lab4 server)
HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[SERVER] The server is listening ...")

# ✅ TÁI SỬ DỤNG: try/except/finally (giống mọi bài lab)
try:
    # ✅ TÁI SỬ DỤNG: Accept connection
    client_socket, client_add = server_socket.accept()
    print(f"[SERVER] Client connected from {client_add}")

    # ✅ TÁI SỬ DỤNG: Vòng lặp vô tận nhận request (giống Lab3/Lab4)
    while True:
        request = client_socket.recv(1024).decode().strip()

        # ✅ TÁI SỬ DỤNG: Xử lý quit/exit (giống Lab3/Lab4)
        if request in ["quit", "exit"]:
            break

        # 🆕 MỚI: Kiểm tra loại request và trả về ngày/giờ tương ứng
        if request == "SEND_DATE":
            response = datetime.datetime.now().strftime("%Y-%m-%d")
        elif request == "SEND_TIME":
            response = datetime.datetime.now().strftime("%H:%M:%S")   # HH:MM:SS format
        else:
            response = "Invalid request. Use SEND_DATE or SEND_TIME."

        client_socket.sendall(response.encode())

except Exception as e:
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket trong finally
    client_socket.close()
    server_socket.close()
    print("Server closed.")
