import socket
import multiprocessing
#import os

def handle_client(connection, address):
    """
    Function to handle individual client logic.
    Each call to this runs in a new process.
    """

    #print(f"[+] New process {os.getpid()} started for {address}")
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            
            # Example logic: Echo the data back
            message = data.decode('utf-8').strip()
            print(f"[{address}] says: {message}")
            connection.sendall(f"Echo: {message}\n".encode('utf-8'))

    except Exception as e:
        print(f"[!] Error handling {address}: {e}")
    finally:
        #print(f"[-] Closing connection for {address} (Process {os.getpid()})")
        connection.close()

def start_server(host='127.0.0.1', port=2027):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow immediate reuse of the port after stopping the server
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[*] Server listening on {host}:{port}")

        while True:
            # Wait for a connection
            client_conn, client_addr = server_socket.accept()
            print(f"[*] Accepted connection from {client_addr}")

            # Create a new process for the client
            process = multiprocessing.Process(
                target=handle_client, 
                args=(client_conn, client_addr)
            )

            # Deamonsize so processes exit if the main server exits
            process.daemon = True
            process.start()

            # Critical: Close the parent's reference to the client socket
            # The child process now owns this resource.
            client_conn.close()

    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
            