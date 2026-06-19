import socket

HOST = "127.0.0.1"
PORT = 5002

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"[Server] UDP Quiz server running on {HOST}:{PORT}")

questions = [
    ("Port 443 is used for HTTP.", False),
    ("TCP is a connection-oriented protocol.", True),
    ("UDP guarantees delivery of packets.", False),
    ("The send() method is used to receive data from a socket.", False),
    ("The bind() method is used to connect a client to a server.", False),
]

try:
    # Chờ client gửi tin đầu tiên để biết địa chỉ client
    data, client_add = server_socket.recvfrom(1024)
    print("[SERVER] Client connected:", client_add)

    for question, correct_answer in questions:
        # Gửi câu hỏi
        server_socket.sendto((question + " (true/false): ").encode(), client_add)

        # Nhận trả lời
        answer, client_add = server_socket.recvfrom(1024)
        answer = answer.decode().strip().lower()
        print("SERVER: client answered:", answer)

        # Kiểm tra exit/quit
        if answer in ["exit", "quit"]:
            server_socket.sendto("Goodbye".encode(), client_add)
            break

        # Kiểm tra đúng/sai
        if (answer == "true") == correct_answer:
            server_socket.sendto("Yes, it's correct!".encode(), client_add)
        else:
            server_socket.sendto("No, it's wrong!".encode(), client_add)

    # Hết câu hỏi
    server_socket.sendto("Quiz finished!".encode(), client_add)

except Exception as e:
    print("Error:", e)
finally:
    server_socket.close()
    print("Server closed.")
