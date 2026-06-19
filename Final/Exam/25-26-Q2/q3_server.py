import asyncio
from datetime import datetime

HOST = '0.0.0.0'
PORT = 2026

# =============== [PHẦN LOGIC RIÊNG: CẤU HÌNH LOG FILE] ===============
LOG_FILE = "server.log"

def write_log(ip_add, index, result):
    # Lấy thời gian hiện tại định dạng: Năm-Tháng-Ngày Giờ:Phút:Giây
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Mở file chế độ "a" (append - ghi nối tiếp vào cuối file)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {ip_add} {index} {result}\n")

async def run_audit():
    # Gọi shell script phân tích log của câu 2
    process = await asyncio.create_subprocess_exec("bash", "audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

# ==========================================
# [LOGIC ĐỀ BÀI: KIỂM TRA ĐỘ MẠNH MẬT KHẨU]
# ==========================================
def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)

async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    ip_address = add[0] # add[0] là IP
    port = add[1]       # add[1] là Port
    
    # In ra log theo yêu cầu đề bài
    print(f"[INFO] New connection from {ip_address}:{port}")

    # Chờ nhận dữ liệu từ Client (tối đa 100 bytes)
    data = await reader.read(100)
    # Chuyển từ dạng byte sang string
    data = data.decode().strip()

    # =============== [PHẦN LOGIC RIÊNG: XỬ LÝ YÊU CẦU ĐỀ BÀI] ===============
    try:
        # Do input qua mạng luôn là chuỗi string, phải ép về số nguyên (int)
        number = int(data)
        # Gọi hàm tính Fibonacci
        results = fibonacci(number)
    except ValueError:
        # Nếu Client gửi không phải là số (vd gửi chữ "abc")
        number = data 
        results = "ERROR_INVALID_INPUT"

  # Thực hiện ghi Log trước khi gửi trả kết quả
    write_log(ip_address, number, results)
    
    # =============== [PHẦN SƯỜN BẮT BUỘC: GỬI KẾT QUẢ VỀ] ===============
    # Gửi trả kết quả (Nhớ phải encode sang dạng byte)
    writer.write(f"{results}\n".encode())
    await writer.drain() # Đảm bảo gửi xong

    # =============== [PHẦN SƯỜN BẮT BUỘC: ĐÓNG KẾT NỐI] ===============
    writer.close()
    await writer.wait_closed()
    await run_audit()

        
# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
# =============== [PHẦN SƯỜN BẮT BUỘC: KHỞI ĐỘNG SERVER] ===============
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[INFO] Server started on port {PORT}...")

    # Giữ server chạy vô hạn
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
