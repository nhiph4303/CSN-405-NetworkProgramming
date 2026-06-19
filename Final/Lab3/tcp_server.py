import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"[Server] Server is running on {HOST}: {PORT}")

try:
#accept
    client_socket, client_add = server_socket.accept()
    print(f"[SEVER] client is connected: ", client_add)
    print(client_socket)

    while True: 
        #Receive a line of text from the client
        data = client_socket.recv(1024)
        data = data.decode()
        print("[SEVER] received: ", data)
    
        if data == "exit":
            print("[SEVER] client is closed")
            break
        
    # reply = data.upper().encode()
    # client_socket.sendall(reply)

    #Count how many times the letter 'n' appears in the text.
    #Send the count back to the client.
        count = data.count('n')
        client_socket.sendall(str(count).encode())

except Exception as e:
    print("Error:", e)

finally:
    client_socket.close()
    server_socket.close()
    print("Server closed.")