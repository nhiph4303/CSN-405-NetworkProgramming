import asyncio
import math
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

# =============== [PHẦN LOGIC RIÊNG: CẤU HÌNH LOG FILE] ===============
LOG_FILE = "server.log"

def log_request(port, number, result):
    # Lấy thời gian hiện tại định dạng: Năm-Tháng-Ngày Giờ:Phút:Giây
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Mở file chế độ "a" (append - ghi nối tiếp vào cuối file)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {number} {result}\n")

# =============== [PHẦN LOGIC RIÊNG: KIỂM TRA NGUYÊN TỐ] ===============
def is_prime(n):
    if n <= 1:
        return False
    # Kiểm tra từ 2 đến căn bậc 2 của n là cách nhanh nhất
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# =============== [PHẦN SƯỜN BẮT BUỘC: HÀM XỬ LÝ CLIENT] ===============
async def handle_client(reader, writer):
    # Lấy thông tin kết nối của Client (ví dụ để ghi log)
    add = writer.get_extra_info("peername")
    port = add[1] # add[0] là IP, add[1] là Port

    # Chờ nhận dữ liệu từ Client (tối đa 100 bytes)
    data = await reader.read(100)
    # Chuyển từ dạng byte sang string
    data = data.decode().strip()

    print(f"[SERVER] received: {data}")

    # =============== [PHẦN LOGIC RIÊNG: XỬ LÝ YÊU CẦU ĐỀ BÀI] ===============
    try:
        # Do input qua mạng luôn là chuỗi string, phải ép về số nguyên (int)
        number = int(data)
        # Gọi hàm kiểm tra nguyên tố
        if is_prime(number):
            results = "TRUE"
        else:
            results = "FALSE"
    except ValueError:
        # Nếu Client gửi không phải là số (vd gửi chữ "abc")
        print("ERROR, input invalid")
        number = data 
        results = "ERROR"
    
    # Thực hiện ghi Log trước khi gửi trả kết quả
    log_request(port, number, results)
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI KẾT QUẢ VỀ] ===============
    # Gửi trả kết quả (Nhớ phải encode sang dạng byte)
    writer.write(f"[SERVER] {results}\n".encode())
    await writer.drain() # Đảm bảo gửi xong

    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    writer.close()
    await writer.wait_closed()

# =============== [PHẦN SƯỜN BẮT BUỘC: KHỞI ĐỘNG SERVER] ===============
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] server is running on {HOST}:{PORT}")

    # Giữ server chạy vô hạn
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

