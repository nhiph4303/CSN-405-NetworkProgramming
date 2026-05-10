import socket

HOST = "127.0.0.1"
PORT = 5002

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)
    print(f"[CLIENT] UDP Quiz connected to {HOST}:{PORT}")

    # Gửi tin đầu tiên để server biết địa chỉ client
    client_socket.sendto("start".encode(), (HOST, PORT))

    while True:
        # Nhận câu hỏi từ server
        question, _ = client_socket.recvfrom(1024)
        question = question.decode()
        print("\n[QUIZ]", question)

        if "Quiz finished" in question or "Goodbye" in question:
            break

        # Nhập câu trả lời
        answer = input("Your answer: ")
        client_socket.sendto(answer.encode(), (HOST, PORT))

        if answer in ["quit", "exit"]:
            break

        # Nhận kết quả
        result, _ = client_socket.recvfrom(1024)
        print("[RESULT]", result.decode())

except socket.timeout:
    print("Timeout!")
except Exception as e:
    print("Error:", e)
finally:
    client_socket.close()
