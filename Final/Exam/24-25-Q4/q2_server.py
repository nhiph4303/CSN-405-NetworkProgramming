import asyncio
from datetime import datetime

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "0.0.0.0"
PORT = 8080
LOG_FILE = "server_log.txt"

# ==========================================
# [LOGIC ĐỀ BÀI: GHI FILE LOG]
# ==========================================
def write_log(ip, port, message):
    # Lấy thời gian hiện tại theo định dạng chuẩn
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ghi log vào file (chế độ append 'a')
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] Client {ip}:{port} sent:\n")
        f.write(message)
        f.write("\n" + "="*50 + "\n")

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_ip = address[0]
    client_port = address[1]
    
    print(f"[SERVER] Client connected from {client_ip}:{client_port}")
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        # Đọc 4096 bytes vì thông báo hệ thống khá dài
        data = await reader.read(4096)
        if data:
            message = data.decode()
            print(f"[SERVER] Received system report from {client_ip}:{client_port}")

            # ==========================================
            # [LOGIC ĐỀ BÀI: GHI LOG]
            # ==========================================
            write_log(client_ip, client_port, message)
            print(f"[SERVER] Data saved to {LOG_FILE}")
            
            # Gửi phản hồi cho Client (Tùy chọn, đề không yêu cầu nhưng nên có)
            writer.write("System report received successfully.\n".encode())
            await writer.drain()

    except Exception as e:
        print("[SERVER] Error", e)

    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[SERVER] Client disconnected: {client_ip}:{client_port}")
        
# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
