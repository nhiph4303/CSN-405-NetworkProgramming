import socket

HOST = "127.0.0.1"
PORT = 5000

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    print(f"[CLIENT] connected {HOST}: {PORT}")

    while True:
    #read from keyboard
        message = input("Enter a message (exit to close): ")
    
    #send to server
        client_socket.sendall(message.encode()) 
        if message == "exit":   
            break           
        
    #receive the result from the server and display it.
        data = client_socket.recv(1024)
        if not data:
            print("Server closed")
            break
        
        print("[CLIENT] Letter 'n' count:", data.decode())

except Exception as e:
    print("Error:", e)

finally:
    client_socket.close()