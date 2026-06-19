import asyncio

HOST = '127.0.0.1'
PORT = 2026

async def main():
    # =============== [PHẦN SƯỜN BẮT BUỘC: KẾT NỐI] ===============
    # Mở kết nối tới Server
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # =============== [PHẦN LOGIC ĐỀ BÀI YÊU CẦU] ===============
    # Đề yêu cầu nhập chỉ số n từ bàn phím
    number = input("Enter Fibonacci index: ")
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI DỮ LIỆU] ===============
    writer.write(number.encode())
    await writer.drain()

    # =============== [PHẦN SƯỜN BẮT BUỘC: NHẬN PHẢN HỒI] ===============
    response = await reader.read(100)
    response = response.decode().strip()
    
    # In ra kết quả y hệt format đề thi
    print(f"Result: {response}")
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    writer.close()
    await writer.wait_closed()
    
    print("Connection closed by foreign host.")

if __name__ == "__main__":
    asyncio.run(main())

