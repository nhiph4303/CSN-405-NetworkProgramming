import asyncio

HOST = '127.0.0.1'
PORT = 8080

# Hàm chạy ngầm để liên tục nhận tin nhắn từ những người khác
async def receive_messages(reader):
    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print("\n[CLIENT] Server closed connection.")
                break
            print(f"\n{data.decode()}", end="")
    except Exception as e:
        print(f"\n[CLIENT] Error: {e}")

async def main():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] Connected to chat server! Type your messages (Type QUIT to exit).")

        # Mở luồng nhận tin nhắn chạy ngầm (Không đợi)
        asyncio.create_task(receive_messages(reader))

        # Vòng lặp chính dùng để nhập chữ
        while True:
            # asyncio.to_thread giúp việc nhập input không làm treo tiến trình nhận tin nhắn
            message = await asyncio.to_thread(input, "")
            
            if message.strip().upper() == "QUIT":
                break
                
            writer.write(f"{message}\n".encode())
            await writer.drain()
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("[CLIENT] closing connection")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

