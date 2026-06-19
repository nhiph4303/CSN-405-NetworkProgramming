import asyncio

# =====================================================================
# SƯỜN SERVER ASYNCIO CƠ BẢN (LAB 5)
# Sử dụng cho các bài tập: tính toán (Prime, Fact), tính tổng, chuỗi...
# =====================================================================

HOST = '127.0.0.1'
PORT = 5000

# [HÀM XỬ LÝ LÔ-GIC RIÊNG CỦA BÀI TOÁN - ĐỀ YÊU CẦU GÌ THÌ VIẾT HÀM Ở ĐÂY]
# Ví dụ: def is_prime(n): ... hoặc def check_score(score): ...

async def handle_client(reader, writer):
    # 1. Lấy thông tin IP, Port của Client
    addr = writer.get_extra_info("peername")
    client_port = addr[1]
    print(f"[SERVER] Client đã kết nối từ port {client_port}")

    # 2. Vòng lặp nhận dữ liệu liên tục từ Client
    while True:
        try:
            # Nhận dữ liệu (đọc tối đa 1024 bytes)
            data = await reader.read(1024)
            
            # NẾU không có data -> Client ngắt kết nối đột ngột
            if not data:
                break
            
            # Giải mã dữ liệu từ byte sang string và xóa khoảng trắng 2 đầu
            message = data.decode().strip()
            
            # Bỏ qua nếu client gửi chuỗi rỗng (bấm Enter mà ko nhập gì)
            if not message:
                continue
                
            print(f"[SERVER] Đã nhận từ {client_port}: {message}")
            
            # Kiểm tra xem Client có muốn thoát không
            if message.upper() in ["QUIT", "EXIT"]:
                # Phản hồi lại và thoát vòng lặp
                writer.write(b"[SERVER] BYE\n")
                await writer.drain()
                break
            
            # =========================================================
            # [BẮT ĐẦU VÙNG CẦN SỬA KHI THI]
            # XỬ LÝ LOGIC CHÍNH CỦA ĐỀ BÀI SẼ NẰM TRONG KHỐI TRY-EXCEPT NÀY
            # =========================================================
            try:
                # Phân tích cú pháp tin nhắn (Ví dụ client gửi "PRIME 5" hoặc "5 6 7")
                # parts = message.split() 
                
                # Tính toán logic...
                # Kết quả phải chuyển về chuỗi để gửi đi
                result_str = f"Ket qua cua ban la: {message}" 
                
                # Gán nội dung phản hồi
                response = f"[SERVER] {result_str}\n"
                
            except ValueError:
                # Bắt lỗi nếu người dùng nhập linh tinh (chữ thay vì số)
                response = "[SERVER] ERROR: Vui long nhap dung dinh dang.\n"
            # =========================================================
            # [KẾT THÚC VÙNG CẦN SỬA KHI THI]
            # =========================================================

            # 3. Gửi kết quả lại cho Client
            writer.write(response.encode()) # Chuyển chuỗi thành byte
            await writer.drain()            # Đảm bảo dữ liệu đã được đẩy đi
            
        except Exception as e:
            print(f"[SERVER] Lỗi xử lý client: {e}")
            break

    # 4. Đóng kết nối khi vòng lặp kết thúc
    print(f"[SERVER] Client {client_port} đã ngắt kết nối")
    writer.close()
    await writer.wait_closed()

async def main():
    # Khởi động Server
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")

    # Giữ Server chạy mãi mãi
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
