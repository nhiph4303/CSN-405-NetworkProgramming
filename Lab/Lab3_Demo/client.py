import socket

HOST = "127.0.0.1"
PORT = 5002

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"[CLIENT] connected {HOST}: {PORT}")

while True:
    data = client_socket.recv(1024).decode()
    print("Question: ", data)
    
    if not data:
        print("Server closed")
        break
    if "Quiz finished" in data or "Goodbye" in data:
        break
    
    answer = input("Enter an answer (true/false): ")
    client_socket.sendall(answer.encode())
    
    s_reply = client_socket.recv(1024).decode()
    print("[CLIENT] server replied: ", s_reply)
    
    if "Quiz finished" in s_reply or "Goodbye" in s_reply:
        break
client_socket.close()
print("client Closed")