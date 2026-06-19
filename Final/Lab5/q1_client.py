import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    # =============== [PHẦN SƯỜN BẮT BUỘC: KẾT NỐI] ===============
    # Mở kết nối tới Server
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("[CLIENT] connected to server")

    # =============== [PHẦN LOGIC ĐỀ BÀI YÊU CẦU] ===============
    # Đề yêu cầu nhập 1 số từ bàn phím
    number = input("Enter a number: ")
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI DỮ LIỆU] ===============
    # Dữ liệu gửi đi qua mạng BẮT BUỘC phải chuyển thành dạng byte (.encode())
    writer.write(number.encode())
    await writer.drain() # Hàm drain() đảm bảo dữ liệu thực sự được đẩy đi qua mạng

    print(f"[CLIENT] sent server: {number}")

    # =============== [PHẦN SƯỜN BẮT BUỘC: NHẬN PHẢN HỒI] ===============
    # Nhận dữ liệu phản hồi (chờ đọc tối đa 100 bytes)
    response = await reader.read(100)
    # Dữ liệu nhận về đang là byte, BẮT BUỘC phải chuyển lại thành chuỗi (.decode())
    # .strip() để xóa bớt dấu cách hoặc ký tự xuống dòng dư thừa
    response = response.decode().strip()
    
    # In ra kết quả
    print(f"{response}")
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    # Vì đề bài chỉ yêu cầu gửi 1 lần rồi thôi nên đóng luôn kết nối
    writer.close()
    await writer.wait_closed()
    print("[CLIENT] closed connection")

if __name__ == "__main__":
    asyncio.run(main())

