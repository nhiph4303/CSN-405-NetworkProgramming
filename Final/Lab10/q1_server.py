import asyncio
from datetime import datetime

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "server.log"

# ==========================================
# [LOGIC ĐỀ BÀI: DỮ LIỆU NGƯỜI DÙNG]
# ==========================================
users = {
    "Hanh_Nhi": "123456",
    "user2": "network",
    "user3": "python"
}

# ==========================================
# [LOGIC ĐỀ BÀI: GHI FILE LOG VÀ CHẠY AWK SCRIPT]
# ==========================================
def write_log(port, username, result):
    # Lấy thời gian hiện tại theo định dạng chuẩn
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ghi log vào file (chế độ append 'a')
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {username} {result}\n")

async def run_audit():
    # Sử dụng module asyncio.subprocess để chạy file bash (ở đây là q1_audit.sh)
    process = await asyncio.create_subprocess_exec("bash", "q1_audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        data = await reader.readline()
        message = data.decode().strip()
        parts = message.split()

        # ==========================================
        # [LOGIC ĐỀ BÀI: KIỂM TRA ĐĂNG NHẬP]
        # ==========================================
        if len(parts) != 2:
            username = "UNKNOWN"
            password = "LOGIN_FAIL"
        else:
            username = parts[0]
            password = parts[1]

            if username in users and users[username] == password:
                result = "LOGIN_SUCCESS"
            else:
                result = "LOGIN_FAIL"
        
        write_log(client_port, username, result)
        
        # Gửi kết quả cho Client
        writer.write((result + "\n").encode())
        await writer.drain()

    except Exception as e:
        print("[SERVER] Error", e)

    finally:
        writer.close()
        await writer.wait_closed()
        
        # Sau khi ngắt kết nối thì tự động chạy script Audit
        await run_audit()
        print("[SERVER] Client disconnected")
        
# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print("[SERVER] is running")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())