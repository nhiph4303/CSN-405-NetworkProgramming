import socket

HOST = "127.0.0.1"
PORT = 6001

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

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # Send client name to server (identification)
    name = input("Enter your name: ")
    client_socket.sendall(name.encode())

    while True:
        expr = input('Enter arithmetic expression (e.g., "12 + 42") or "quit" to exit: ')

        if expr == "quit":
            client_socket.sendall("quit".encode())
            break

        # Validate format before sending
        if not is_valid(expr):
            print("[WARNING] Invalid format! Use: number operator number")
            continue    # ask again, don't send to server

        # Send valid expression to server and receive result
        client_socket.sendall(expr.encode())
        result = client_socket.recv(1024).decode()
        print(f"Result: {result}")

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")
