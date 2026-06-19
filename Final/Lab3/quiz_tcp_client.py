import socket

HOST = "127.0.0.1"
PORT = 5050

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"[CLIENT] connected {HOST}: {PORT}")

    while True:
    # Nhận câu hỏi từ server
        question = client_socket.recv(1024).decode()
        print("\n[QUIZ]", question)

        if not question:
            print("Server closed")
            break
        if "Quiz finished" in question or "Goodbye" in question:
            break
    
        answer = input("Enter an answer (true/false): ")
        client_socket.sendall(answer.encode())
    
    # Nếu quit/exit thì thoát
        if answer in ["quit", "exit"]:
            break
        s_reply = client_socket.recv(1024).decode()
        print("[CLIENT] server replied: ", s_reply)
    
        if "Quiz finished" in s_reply or "Goodbye" in s_reply:
            break

except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()