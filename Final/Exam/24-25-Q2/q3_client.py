import asyncio

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 8080
LOG_FILE = "log.txt"

async def main():
    # ==========================================
    # [LOGIC ĐỀ BÀI: ĐỌC NỘI DUNG FILE LOG]
    # ==========================================
    print(f"[CLIENT] Reading {LOG_FILE}...")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
    except Exception as e:
        print(f"[CLIENT] Error reading file: {e}")
        return

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"[CLIENT] Connected to server {HOST}:{PORT}")

    # Gửi toàn bộ file log lên server
    writer.write(log_content.encode())
    await writer.drain()
    print("[CLIENT] Log file sent successfully. Waiting for summary report...")

    # Nhận kết quả Report trả về từ Server
    # Vì report có nhiều dòng nên dùng read(4096) thay vì readline()
    data = await reader.read(4096)
    if data:
        print("\n[CLIENT] Server response (Summary Report):")
        print("========================================")
        print(data.decode().strip())
        print("========================================")

    writer.close()
    await writer.wait_closed()
    print("[CLIENT] Disconnected.")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC CLIENT]
# ==========================================
if __name__ == "__main__":
    asyncio.run(main())
