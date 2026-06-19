import asyncio
import subprocess

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 8080

async def main():
    # ==========================================
    # [LOGIC ĐỀ BÀI: LẤY THÔNG TIN TỪ BASH SCRIPT]
    # ==========================================
    print("[CLIENT] Running system_monitor.sh...")
    try:
        result = subprocess.run(["bash", "system_monitor.sh"], capture_output=True, text=True)
        system_info = result.stdout
        
        # Phòng hờ trường hợp chạy trên Windows không gọi được bash script
        if not system_info:
            system_info = "[WARNING] No system information retrieved. Are you running on Windows?"
    except Exception as e:
        system_info = f"[ERROR] Failed to run bash script: {e}"

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"[CLIENT] Connected to Server {HOST}:{PORT}")

    # Gửi cấu hình hệ thống
    writer.write(system_info.encode())
    await writer.drain()
    print("[CLIENT] System information sent successfully.")

    # Nhận kết quả trả về từ Server (Nếu Server có gửi)
    data = await reader.readline()
    if data:
        print(f"Server response: {data.decode().strip()}")

    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
