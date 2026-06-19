import socket

HOST = "127.0.0.1"
PORT = 6002        

def is_valid(expr):
    parts = expr.split()
    if len(parts) != 3:          
        return False
    try:
        float(parts[0])          
        float(parts[2])          
    except:
        return False
    if parts[1] not in ["+", "-", "*", "/"]:   
        return False
    return True

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    name = input("Enter your name: ")
    client_socket.sendall(name.encode())

    while True:
        expr = input('Enter arithmetic expression (e.g., "12 + 42") or "quit" to exit: ')

        if expr == "quit":
            client_socket.sendall("quit".encode())
            break
        if not is_valid(expr):
            print("[WARNING] Invalid format! Use: number operator number")
            continue

        client_socket.sendall(expr.encode())
        result = client_socket.recv(1024).decode()
        print(f"Result: {result}")

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    print("Client closed.")
