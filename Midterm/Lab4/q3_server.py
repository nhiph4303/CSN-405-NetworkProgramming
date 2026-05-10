import socket
import threading

HOST = "127.0.0.1"
PORT = 6002

# Hàm xử lý mỗi client — chạy trong thread riêng
def handle_client(client_socket, client_add):
    client_ip   = client_add[0]
    client_port = client_add[1]

    try:
        # Nhận tên client (identification)
        client_name = client_socket.recv(1024).decode()
        print(f"Client connected: {client_name} from {client_ip}:{client_port}")

        # Vòng lặp nhận và xử lý phép tính
        while True:
            data = client_socket.recv(1024).decode()
            if data in ["quit", "exit"]:
                break
            print(f"Received from {client_name}: {data}")

            # Tính toán và gửi kết quả
            try:
                result = eval(data)              # eval("13 + 7") → 20
                client_socket.sendall(str(result).encode())
            except ZeroDivisionError:
                client_socket.sendall("Error: Division by zero".encode())
            except:
                client_socket.sendall("Error: Invalid expression".encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()  # đóng socket client khi xong

# Setup server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)        # cho phép tối đa 5 client chờ kết nối
print(f"[SERVER] The server is listening ...")

try:
    while True:
        # Mỗi accept() tạo ra 1 socket mới cho client đó
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")

        # Tạo thread mới, giao cho handle_client xử lý
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()

except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()
