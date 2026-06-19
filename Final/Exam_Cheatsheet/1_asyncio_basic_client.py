import asyncio

# =====================================================================
# SƯỜN CLIENT ASYNCIO CƠ BẢN (LAB 5, LAB 10)
# Dùng để kết nối lên Server, gửi request liên tục và in kết quả.
# =====================================================================

HOST = '127.0.0.1'
PORT = 5000

async def main():
    try:
        # 1. Kết nối tới Server
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] Đã kết nối tới Server")
        
        # [CÓ THỂ IN RA MENU CHO NGƯỜI DÙNG Ở ĐÂY]
        print("--- CÁC LỆNH HỖ TRỢ ---")
        print("  Nhập gì đó để gửi")
        print("  Nhập QUIT để thoát")
        print("-----------------------")

        # 2. Vòng lặp nhập và gửi dữ liệu
        while True:
            try:
                # Cho người dùng nhập từ bàn phím
                user_input = input("[CLIENT] Nhập lệnh: ")
            except EOFError: # Bắt lỗi nếu người dùng bấm Ctrl+D
                break
                
            # Bỏ qua nếu không nhập gì
            if not user_input.strip():
                continue
                
            # Gửi dữ liệu tới Server
            writer.write(user_input.encode())
            await writer.drain()

            # Nhận phản hồi từ Server
            response = await reader.read(1024)
            
            # Nếu Server đóng kết nối thì thoát
            if not response:
                print("[CLIENT] Server đã đóng kết nối")
                break
                
            # In phản hồi
            response_text = response.decode().strip()
            print(f"Server trả lời: {response_text}")
            
            # Nếu người dùng gõ QUIT thì thoát client
            if user_input.strip().upper() in ["QUIT", "EXIT"]:
                break
                
    except Exception as e:
        print(f"Lỗi kết nối: {e}")
    finally:
        # 3. Đóng kết nối gọn gàng
        print("[CLIENT] Đang đóng kết nối...")
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())
