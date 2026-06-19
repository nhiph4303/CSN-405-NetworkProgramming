import socket

HOST = "127.0.0.1"
PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[Server] Server is running on {HOST}: {PORT}")

questions = [
    ("Port 443 is used for HTTP.", False),
    ("TCP is a connection-oriented protocol.", True),
    ("UDP guarantees delivery of packets.", False),
    ("The send() method is used to receive data from a socket.", False),
    ("The bind() method is used to connect a client to a server.", False),
]

try:
#accept
    client_socket, client_add = server_socket.accept()
    print(f"[SEVER] client is connected: ", client_add)

    for question, correct_answer in questions:
        # Gửi câu hỏi
        client_socket.sendall((question + " (true/false): ").encode())
        
        # Nhận trả lời
        answer = client_socket.recv(1024).decode().strip().lower()
        print("SERVER: client answered:", answer)
        
        # Kiểm tra exit/quit
        if answer in ["exit", "quit"]:
            client_socket.sendall("Goodbye".encode())
            break
        
        # Kiểm tra đúng/sai
        if (answer == "true") == correct_answer:
            client_socket.sendall("Yes, it's correct!".encode())
        else:
            client_socket.sendall("No, it's wrong!".encode())
    
    # Ngoài for — hết câu hỏi
    client_socket.sendall("Quiz finished!".encode())

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
    server_socket.close()
