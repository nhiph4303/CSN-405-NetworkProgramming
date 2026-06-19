import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    try:
        # =============== [PHẦN SƯỜN BẮT BUỘC: KẾT NỐI] ===============
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] connected to server")
        
        # =============== [PHẦN SƯỜN BẮT BUỘC: VÒNG LẶP LIÊN TỤC] ===============
        while True:
            try:
                # =============== [PHẦN LOGIC ĐỀ BÀI: YÊU CẦU NHẬP NHIỀU SỐ] ===============
                numbers = input("[CLIENT] Enter numbers: ")
            except EOFError:
                break
                
            # Xử lý bỏ qua nếu bấm enter rỗng
            if not numbers.strip():
                continue
                
            # =============== [PHẦN LOGIC ĐỀ BÀI: KIỂM TRA LỆNH THOÁT] ===============
            if numbers.strip().upper() == "QUIT":
                writer.write(b"QUIT")
                await writer.drain()
                response = await reader.read(1024)
                print(f"Server reply: {response.decode().strip()}")
                break
                
            # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI LÊN SERVER] ===============
            writer.write(numbers.encode())
            await writer.drain()

            # =============== [PHẦN SƯỜN BẮT BUỘC: NHẬN PHẢN HỒI] ===============
            response = await reader.read(1024)
            if not response:
                print("[CLIENT] Server closed connection")
                break
                
            response_text = response.decode().strip()
            print(f"Server reply: {response_text}")
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
        print("[CLIENT] closing connection")
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())

