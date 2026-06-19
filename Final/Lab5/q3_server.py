import asyncio
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

# =============== [PHẦN LOGIC RIÊNG: CẤU HÌNH LOG FILE] ===============
LOG_FILE = "server.log"

def log_request(port, numbers_str, result_str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {numbers_str} {result_str}\n")

# =============== [PHẦN SƯỜN BẮT BUỘC: HÀM XỬ LÝ CLIENT] ===============
async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    port = add[1]
    
    print(f"[SERVER] Client connected from port {port}")

    # Xử lý nhiều request trên cùng 1 kết nối -> BẮT BUỘC dùng while True
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode().strip()
            if not message:
                continue
                
            print(f"[SERVER] received: {message}")
            
            # =============== [PHẦN LOGIC RIÊNG: XỬ LÝ THOÁT] ===============
            if message.upper() == "QUIT":
                log_request(port, message, "BYE")
                writer.write(b"[SERVER] BYE\n")
                await writer.drain()
                break
            
            # =============== [PHẦN LOGIC RIÊNG: PHÂN TÍCH VÀ TÍNH TOÁN DÃY SỐ] ===============
            try:
                # Kỹ thuật ép kiểu danh sách (List Comprehension)
                # Tách chuỗi bằng khoảng trắng: "3 7 10 5" -> ["3", "7", "10", "5"]
                # Ép kiểu int() cho từng phần tử -> [3, 7, 10, 5]
                numbers = [int(x) for x in message.split()]
                
                if not numbers:
                    raise ValueError("No numbers provided")
                
                # Hàm sum() tính tổng mảng, hàm min() tìm phần tử nhỏ nhất
                total_sum = sum(numbers)
                min_val = min(numbers)
                
                # Nối chuỗi kết quả theo đúng định dạng đề yêu cầu: SUM=<sum> MIN=<min>
                result_str = f"SUM={total_sum} MIN={min_val}"
                
                # Nối chuỗi gửi đi theo định dạng: [SERVER] SUM=<sum> MIN=<min>
                response = f"[SERVER] {result_str}\n"
                
                # Gọi hàm Ghi log
                log_request(port, message, result_str)
                
            except ValueError:
                # Xử lý lỗi nếu gửi lên chữ cái thay vì số
                response = "[SERVER] ERROR: Invalid input. Please enter integers separated by spaces.\n"
                log_request(port, message, "ERROR")
                
            # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI TRẢ CLIENT] ===============
            writer.write(response.encode())
            await writer.drain()
            
        except Exception as e:
            print(f"[SERVER] Error handling client: {e}")
            break

    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    print(f"[SERVER] Client {port} disconnected")
    writer.close()
    await writer.wait_closed()

# =============== [PHẦN SƯỜN BẮT BUỘC: KHỞI ĐỘNG SERVER] ===============
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] server is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

