import asyncio
from datetime import datetime

HOST = '0.0.0.0'
PORT = 8080
LOG_FILE = "connections.log"

# Biến global lưu danh sách tất cả các client đang kết nối
clients = set()

# =============== [PHẦN LOGIC RIÊNG: GHI LOG KẾT NỐI] ===============
def write_log(action, ip, port):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        # action sẽ là chữ "CONNECT" hoặc "DISCONNECT"
        f.write(f"[{time_str}] {action} {ip}:{port}\n")

# Hàm chạy script Bash không chặn tiến trình (Non-blocking)
async def run_monitor():
    process = await asyncio.create_subprocess_exec(
        "bash", "monitor.sh",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if stdout:
        print(stdout.decode())

# =============== [PHẦN SƯỜN BẮT BUỘC: HÀM XỬ LÝ CLIENT] ===============
async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    ip = add[0]
    port = add[1]
    
    # 1. Khi Client vừa kết nối: Thêm vào danh sách và Ghi log
    print(f"[SERVER] Client connected: {ip}:{port}")
    clients.add(writer)
    write_log("CONNECT", ip, port)
    await run_monitor() # CHẠY MONITOR KHI CONNECT
    
    try:
        while True:
            # Chờ nhận tin nhắn từ client này
            data = await reader.read(1024)
            
            # 2. Xử lý ngắt kết nối (Graceful disconnect)
            if not data:
                break # Client ngắt kết nối
            
            message = data.decode()
            print(f"[CHAT from {ip}:{port}] {message.strip()}")
            
            # Tính năng Chat: Broadcast (Gửi tin nhắn này cho tất cả mọi người khác)
            for c in clients:
                if c != writer: # Không gửi ngược lại cho chính người vừa nhắn
                    c.write(f"[{ip}:{port}] {message}".encode())
                    await c.drain()
                    
    except Exception as e:
        # Bắt lỗi nếu Client bị rớt mạng đột ngột
        pass 
        
    finally:
        # 3. Chạy khối finally để đảm bảo DÙ THẾ NÀO cũng xóa client khỏi set và ghi log
        clients.remove(writer)
        write_log("DISCONNECT", ip, port)
        print(f"[SERVER] Client disconnected: {ip}:{port}")
        await run_monitor() # CHẠY MONITOR KHI DISCONNECT
        
        writer.close()
        await writer.wait_closed()

# =============== [PHẦN SƯỜN BẮT BUỘC: KHỞI ĐỘNG SERVER] ===============
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[INFO] Chat server is running on port {PORT}...")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())

