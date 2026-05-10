import socket

# ✅ TÁI SỬ DỤNG: Setup TCP client (giống Lab3/Lab4 client)
HOST = "127.0.0.1"
PORT = 5000

# ✅ TÁI SỬ DỤNG: try/except/finally
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"[CLIENT] Connected to {HOST}:{PORT}")

    # ✅ TÁI SỬ DỤNG: Vòng lặp gửi/nhận (giống Lab3/Lab4)
    while True:
        # 🆕 MỚI: Nhập lệnh SEND_DATE hoặc SEND_TIME
        request = input('Enter request ("SEND_DATE" or "SEND_TIME") or "quit" to exit: ').strip()

        # ✅ TÁI SỬ DỤNG: Xử lý quit/exit
        if request == "quit":
            client_socket.sendall("quit".encode())
            break

        # 🆕 MỚI: Validate — chỉ chấp nhận SEND_DATE hoặc SEND_TIME
        if request not in ["SEND_DATE", "SEND_TIME"]:
            print("[WARNING] Invalid request! Use SEND_DATE or SEND_TIME.")
            continue

        # Gửi request và nhận phản hồi
        client_socket.sendall(request.encode())
        response = client_socket.recv(1024).decode()
        print(f"[SERVER] {response}")

except Exception as e:
    print("Error:", e)
finally:
    # ✅ TÁI SỬ DỤNG: Đóng socket trong finally
    client_socket.close()
    print("Client closed.")
