import socket
import threading

HOST = "127.0.0.1"
PORT = 5050

questions = [
    ("Port 80 is used for HTTP.", True),
    ("TCP is a connection-oriented protocol.", True),
    ("UDP guarantees delivery of packets.", False),
    ("Socket needs a tuple HOST and PORT", True),
    ("IPv4 is the only IP can be assigned for computer", False),
]


def handle_client(client_socket, client_add):
    client_ip = client_add[0]
    client_port = client_add[1]

    try:
        print(f"[SERVER] Client connected from {client_ip}:{client_port}")

        first_question = questions[0][0] + " (true/false): "
        client_socket.sendall(first_question.encode())

        for i in range(len(questions)):
            question, correct_answer = questions[i]

            answer = client_socket.recv(1024).decode().strip().lower()
            print(f"[SERVER] Received from {client_ip}:{client_port}: {answer}")

            if answer in ["quit", "exit"]:
                client_socket.sendall("Goodbye".encode())
                return

            if (answer == "true") == correct_answer:
                result = "Yes, it's correct!"
            else:
                result = "No, it's wrong!"

            if i < len(questions) - 1:
                next_question = questions[i + 1][0] + " (true/false): "
                response = f"{result}\n[QUIZ] {next_question}"
                client_socket.sendall(response.encode())
            else:
                response = f"{result}\nQuiz finished!"
                client_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print(f"[SERVER] Client {client_ip}:{client_port} disconnected.")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"[SERVER] The server is listening on {HOST}:{PORT} ...")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"New thread created for client at {addr}")
        t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        t.start()
except KeyboardInterrupt:
    print("Server shutting down.")
finally:
    server_socket.close()