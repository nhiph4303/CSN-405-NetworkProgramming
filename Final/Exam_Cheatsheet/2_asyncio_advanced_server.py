import asyncio
from datetime import datetime

# =====================================================================
# SƯỜN SERVER ASYNCIO NÂNG CAO (Ghi Log + Subprocess) (LAB 10)
# Thường được hỏi trong phần nâng cao: 
# - Lưu kết quả ra file `server.log`
# - Chạy script bash `.sh` sau khi ngắt kết nối
# =====================================================================

HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "server.log"

# [BẮT BUỘC] Hàm ghi file log (Dùng chung cho mọi bài)
def write_log(port, data_received, result):
    # Lấy giờ hiện tại định dạng YYYY-MM-DD HH:MM:SS
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Mở file chế độ append ("a" - ghi thêm vào cuối file)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {data_received} {result}\n")

# [BẮT BUỘC] Hàm chạy file Bash Script bằng Asyncio (Dùng chung cho mọi bài)
async def run_audit():
    # Sửa "audit.sh" thành tên file script mà đề bài yêu cầu
    process = await asyncio.create_subprocess_exec("bash", "audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Kết quả chạy Audit:")
    if stdout:
        print(stdout.decode())
    if stderr:
        print("[SERVER] Lỗi Audit: ", stderr.decode())

# Khối xử lý Client
async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    
    try:
        data = await reader.readline() # Đọc 1 dòng (dùng khi client gửi thông điệp có ký tự xuống dòng \n)
        if not data:
            return
            
        message = data.decode().strip()
        
        # =========================================================
        # [BẮT ĐẦU VÙNG CẦN SỬA KHI THI] - Xử lý logic nghiệp vụ
        # VD: Kiểm tra password, kiểm tra điểm số...
        # =========================================================
        
        # Ví dụ giả lập logic
        if message == "admin":
            result = "SUCCESS"
        else:
            result = "FAIL"
            
        # =========================================================
        # [KẾT THÚC VÙNG CẦN SỬA KHI THI]
        # =========================================================
        
        # Gọi hàm Ghi Log trước khi gửi trả Client
        write_log(client_port, message, result)
        
        # Trả kết quả cho Client
        writer.write((result + "\n").encode())
        await writer.drain()

    except Exception as e:
        print("[SERVER] Lỗi: ", e)

    finally:
        # Khi Client ngắt kết nối, chạy script Subprocess
        writer.close()
        await writer.wait_closed()
        
        # ĐỀ BÀI YÊU CẦU: "Chạy file audit.sh khi client thoát" -> Gọi hàm này
        await run_audit()
        print("[SERVER] Client đã thoát.")
        
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Đang chạy tại {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
