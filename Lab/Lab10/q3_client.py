import asyncio

HOST = "127.0.0.1"
PORT = 8888

async def main():
    score = input("Enter student score: ")

    reader, writer = await asyncio.open_connection(HOST, PORT)

    message = f"{score}\n"
    writer.write(message.encode())
    await writer.drain()

    data = await reader.readline()
    print(f"Server response: {data.decode().strip()}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
