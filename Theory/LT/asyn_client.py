import asyncio

server_host = "localhost"
server_port = 31000

async def client():
    reader, writer = await asyncio.open_connection(server_host, server_port)
    print(f"Connected to server at {server_host}:{server_port}")

    try:
        while True:
            message = input("Enter message (or type 'exit' to quit): ")
            writer.write(message.encode())
            await writer.drain() # Đảm bảo dữ liệu được gửi
            
            if message.lower() == "exit":
                print("Disconnecting from server...")
                break

            response = await reader.read(1024) # Nhận phản hồi từ server
            if not response:
                print("Server closed the connection.")
                break

            print(f"From Server: {response.decode()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Connection closed.")

if __name__ == "__main__":
    asyncio.run(client())