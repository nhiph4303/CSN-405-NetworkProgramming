import socket
import time 

HOST = "127.0.0.1"
PORT = 5050 

questions = [
    ("Port 443 is used for HTTP.", "false"),
    ("TCP is a connection-oriented protocol.", "true"),
    ("UDP guarantees delivery of packets.", "false"),
    ("The send() method is used to receive data from a socket.", "false"),
    ("The bind() method is used to connect a client to a server.", "false")
]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[Server] Server is running on {HOST}: {PORT}")
#accept
client_socket, client_add = server_socket.accept()
print(f"[SEVER] client is connected: ", client_add)

for question, c_answer in questions:
    #send
    client_socket.sendall((question).encode())
    
    #receive 
    answer = client_socket.recv(1024).decode().strip().lower()
    print("SERVER: client answered ", answer)
    
    if answer == "exit" or answer == "quit":
        break
        
    if answer == c_answer:
        client_socket.sendall(b"Yes, it's correct!") 
    else:
        client_socket.sendall(b"No, it's wrong!") 
        
    time.sleep(0.1) 
        
client_socket.sendall(b"Quiz finished!")
             
client_socket.close()  
server_socket.close()
print("[SERVER] server is closed")