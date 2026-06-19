import asyncio

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 8888

async def main():
    # ==========================================
    # [LOGIC ĐỀ BÀI: NHẬP THÔNG TIN ĐĂNG NHẬP]
    # ==========================================
    username = input("Enter username: ")
    password = input("Enter password: ")

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Gửi username và password cách nhau bởi khoảng trắng
    message = f"{username} {password}\n"
    writer.write(message.encode())
    await writer.drain()

    # Nhận kết quả trả về từ Server
    data = await reader.readline()
    print(f"Server response: {data.decode().strip()}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())