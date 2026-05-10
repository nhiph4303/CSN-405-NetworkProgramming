import asyncio

server_port = 31000

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connected by {addr}")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Client {addr} Disconnected.")
                break

            message = data.decode().upper()
            if message.lower() == "exit":
                print(f"Client {addr} Disconnected by exit command.")
                break
            
            print(f"From Client:{addr}: {message}")

            writer.write(message.encode())
            await writer.drain()
    except Exception as e:
        print(f"Error with {addr}: {str(e)}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection with {addr} closed!")

async def main():
    server = await asyncio.start_server(handle_client, "localhost", server_port)
    addr = server.sockets[0].getsockname()
    print(f"Server is listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())