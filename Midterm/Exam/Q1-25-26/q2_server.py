import socket

# ✅ TÁI SỬ DỤNG: Setup TCP socket (giống Lab4 Q2 server)
HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[SERVER] The server is listening ...")

# ✅ TÁI SỬ DỤNG: try/except/finally (giống mọi bài lab)
try:
    # ✅ TÁI SỬ DỤNG: Accept connection (giống Lab4 Q2)
    client_socket, client_add = server_socket.accept()
    client_ip   = client_add[0]
    client_port = client_add[1]

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
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket trong finally
    client_socket.close()
    server_socket.close()
    print("Server closed.")
