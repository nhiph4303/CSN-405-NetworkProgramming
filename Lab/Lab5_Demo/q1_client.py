import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("[CLIENT] connected to server")

    number = input("Enter a number: ")
    writer.write(number.encode())
    await writer.drain()

    print(f"[CLIENT] sent server: {number}")

    response = await reader.read(100)
    response = response.decode().strip() # Thêm strip() để loại bỏ ký tự xuống dòng dư thừa
    print(f"{response}")
    
    writer.close()
    await writer.wait_closed()
    print("[CLIENT] closed connection")

if __name__ == "__main__":
    asyncio.run(main())
