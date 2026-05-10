import asyncio

server_port = 31000


async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    print(f"Client connected: {add}")
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"Client {add} disconnected")
                break

            message = data.decode().upper()
            if message.lower() == "exit":
                print(f"Client {add} Disconnected by exit command.")
                break

            print(f"From Client {add}: {message}")

            writer.write(message.encode())
            await writer.drain()
    except Exception as e:
        print(f"Error with {add}: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Connection with {add} closed!")


async def main():
    server = await asyncio.start_server(handle_client, "localhost", server_port)
    addr = server.sockets[0].getsockname()
    print(f"Server started on {addr}")

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
