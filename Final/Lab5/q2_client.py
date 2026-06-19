import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    try:
        # =============== [PHẦN SƯỜN BẮT BUỘC: KẾT NỐI] ===============
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] connected to server")
        
        # =============== [PHẦN LOGIC ĐỀ BÀI: IN MENU] ===============
        print("--- Available commands ---")
        print("  PRIME n      (e.g. PRIME 17)")
        print("  NEXT_PRIME n (e.g. NEXT_PRIME 20)")
        print("  FACT n       (e.g. FACT 10)")
        print("  QUIT")
        print("--------------------------")

        # =============== [PHẦN SƯỜN BẮT BUỘC: VÒNG LẶP LIÊN TỤC] ===============
        # Câu 2 yêu cầu "supports many requests in the same connection"
        # nên BẮT BUỘC phải bọc toàn bộ khối Gửi/Nhận trong `while True:`
        while True:
            # Lấy input
            command = input("Client: ")
            
            # Xử lý ngoại lệ nếu bấm enter trống
            if not command:
                continue
                
            # Gửi lên Server
            writer.write(command.encode())
            await writer.drain()

            print(f"[CLIENT] sent server: {command}")

            # Đợi phản hồi
            response = await reader.read(1024)
            
            # Nếu Server đóng kết nối thì thoát vòng lặp
            if not response:
                print("[CLIENT] Server closed connection")
                break
                
            # Xử lý và in kết quả trả về
            response_text = response.decode().strip()
            print(f"Server: {response_text}")
            
            # =============== [PHẦN LOGIC ĐỀ BÀI: KIỂM TRA LỆNH THOÁT] ===============
            # Nếu client gõ lệnh QUIT thì thoát vòng lặp
            if command.strip().upper() == "QUIT":
                break
                
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
        # Bọc trong khối finally để đảm bảo dù lỗi hay không thì vẫn đóng kết nối sạch sẽ
        print("[CLIENT] closing connection")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

