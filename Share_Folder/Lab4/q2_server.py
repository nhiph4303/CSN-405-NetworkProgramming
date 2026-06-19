import socket

HOST = "127.0.0.1"
PORT = 6001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"[SERVER] The server is listening ...")

try:
    client_socket, client_add = server_socket.accept()
    client_ip   = client_add[0]
    client_port = client_add[1]

    client_name = client_socket.recv(1024).decode()
    print(f"Client connected: {client_name} from {client_ip}:{client_port}")

    while True:
        data = client_socket.recv(1024).decode()
        if data in ["quit", "exit"]:
            break
        print(f"Received from {client_name}: {data}")

        try:
            result = eval(data)                            
            client_socket.sendall(str(result).encode())
        except ZeroDivisionError:                          
            client_socket.sendall("Error: Division by zero".encode())
        except:
            client_socket.sendall("Error: Invalid expression".encode())

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    server_socket.close()
    print("Server closed.")
