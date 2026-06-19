import asyncio
import math
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

# =============== [PHẦN LOGIC RIÊNG: CẤU HÌNH LOG FILE] ===============
LOG_FILE = "server.log"

def log_request(port, request, result):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {request} {result}\n")

# =============== [PHẦN LOGIC RIÊNG: CÁC HÀM TÍNH TOÁN THEO YÊU CẦU ĐỀ BÀI] ===============
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_next_prime(n):
    if n <= 2:
        return 2
    p = n
    while True:
        if is_prime(p):
            return p
        p += 1

def get_fact(n):
    # Đề yêu cầu limit: n <= 100, else ERROR
    if n < 0 or n > 100:
        return "ERROR"
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# =============== [PHẦN SƯỜN BẮT BUỘC: HÀM XỬ LÝ CLIENT] ===============
async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    port = add[1]
    
    print(f"[SERVER] Client connected from port {port}")

    # Câu 2 yêu cầu xử lý liên tục nhiều requests
    # BẮT BUỘC sử dụng vòng lặp `while True:`
    while True:
        # Đọc dữ liệu
        data = await reader.read(1024)
        
        # Nếu Client đóng kết nối thì data rỗng -> Thoát vòng lặp
        if not data:
            break
        
        message = data.decode().strip()
        if not message:
            continue
            
        print(f"[SERVER] received: {message}")
        
        # =============== [PHẦN LOGIC RIÊNG: KIỂM TRA ĐỊNH DẠNG TIN NHẮN GỬI LÊN] ===============
        # Tách tin nhắn thành 2 phần: Lệnh và Tham số (Ví dụ: "PRIME" và "17")
        parts = message.split()
        command = parts[0].upper()
        
        # Đề yêu cầu xử lý lệnh QUIT
        if command == "QUIT":
            log_request(port, command, "BYE")
            writer.write(b"[SERVER] BYE\n")
            await writer.drain()
            break # Phải ngắt vòng lặp ở đây
            
        # Kiểm tra xem client có truyền đủ số phía sau lệnh không (Ví dụ gửi "PRIME" mà không có số)
        if len(parts) < 2:
            results = "ERROR"
            log_request(port, message, results)
            writer.write(f"[SERVER] {results}\n".encode())
            await writer.drain()
            continue
            
        # =============== [PHẦN LOGIC RIÊNG: PHÂN RẼ NHÁNH IF-ELIF-ELSE THEO LỆNH ĐỀ BÀI] ===============
        try:
            n = int(parts[1]) # Ép kiểu phần tham số sang số nguyên
            
            if command == "PRIME":
                results = "YES" if is_prime(n) else "NO"
            elif command == "NEXT_PRIME":
                results = str(get_next_prime(n))
            elif command == "FACT":
                results = str(get_fact(n))
            else:
                # Lệnh không tồn tại
                results = "ERROR"
        except ValueError:
            # Bắt lỗi nhập chữ thay vì số
            results = "ERROR"
            
        # =============== [PHẦN SƯỜN: GHI LOG VÀ TRẢ KẾT QUẢ VỀ CLIENT] ===============
        log_request(port, message, results)
        
        writer.write(f"[SERVER] {results}\n".encode())
        await writer.drain()

    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    # Khi vòng lặp while bị break (vì client QUIT hoặc ngắt kết nối)
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

