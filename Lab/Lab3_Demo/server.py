import socket

HOST = "127.0.0.1"
PORT = 5002

questions = [("today is Sat", "true"), ("This is CSN405", "true")]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[Server] Server is running on {HOST}: {PORT}")
#accept
client_socket, client_add = server_socket.accept()
print(f"[SEVER] client is connected: ", client_add)

for question, c_answer in questions:
    #send
    client_socket.sendall((question +"(true/false): ").encode())
    #print("[SEVER] sent")
    
    #receive 
    answer = client_socket.recv(1024).decode().strip().lower()
    print("SERVER: client answered ", answer)
    if answer == "exit":
        reply = "Goodbye"
        client_socket.sendall(reply.encode())
        break
    if answer == c_answer:
        client_socket.sendall(b"Corrected")
    else:
        client_socket.sendall(b"Wrong")
        
client_socket.sendall(b"Quiz finished")
             
client_socket.close()  
server_socket.close()
print("[SERVER] server is closed")     
    
