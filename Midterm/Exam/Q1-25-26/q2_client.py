import socket

# ✅ TÁI SỬ DỤNG: Setup TCP client (giống Lab4 Q2 client)
HOST = "127.0.0.1"
PORT = 5000

# ✅ TÁI SỬ DỤNG: Hàm kiểm tra format (giống Lab4 Q2)
def is_valid(expr):
    parts = expr.split()
    if len(parts) != 3:          # must have exactly 3 parts
        return False
    try:
        float(parts[0])          # first must be a number
        float(parts[2])          # third must be a number
    except:
        return False
    if parts[1] not in ["+", "-", "*", "/"]:   # second must be an operator
        return False
    return True

# ✅ TÁI SỬ DỤNG: try/except/finally
try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # ✅ TÁI SỬ DỤNG: Gửi tên client đến server (giống Lab4 Q2)
    name = input("Enter your name: ")
    client_socket.sendall(name.encode())

    # ✅ TÁI SỬ DỤNG: Vòng lặp nhập và gửi phép tính (giống Lab4 Q2)
    while True:
        expr = input('Enter arithmetic expression (e.g., "12 + 42") or "quit" to exit: ')

        if expr == "quit":
            client_socket.sendall("quit".encode())
            break

        # ✅ TÁI SỬ DỤNG: Validate format trước khi gửi (giống Lab4 Q2)
        if not is_valid(expr):
            print("[WARNING] Invalid format! Use: number operator number")
            continue    # ask again, don't send to server

        # Gửi và nhận kết quả
        client_socket.sendall(expr.encode())
        result = client_socket.recv(1024).decode()
        print(f"Result: {result}")

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")
