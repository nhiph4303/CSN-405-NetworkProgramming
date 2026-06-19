import asyncio

HOST = "127.0.0.1"
PORT = 8888

async def main():
    username = input("Enter username: ")
    password = input("Enter password: ")

    reader, writer = await asyncio.open_connection(HOST, PORT)

    message = f"{username} {password}\n"
    writer.write(message.encode())
    await writer.drain()

    data = await reader.readline()
    print(f"Server response: {data.decode().strip()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(main())