import asyncio

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "0.0.0.0"
PORT = 8080
LOG_FILE = "server_log.txt"

# ==========================================
# [LOGIC ĐỀ BÀI: GỌI BASH & AWK SCRIPT NHƯ LAB 10]
# ==========================================
async def process_logs():
    # 1. Chạy bash script (giống hàm run_audit của Lab 10)
    process_bash = await asyncio.create_subprocess_exec("bash", "count_logs.sh", LOG_FILE,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )
    stdout_bash, _ = await process_bash.communicate()
    bash_result = stdout_bash.decode().strip()

    # 2. Chạy AWK script (cũng dùng asyncio subprocess như Lab 10)
    process_awk = await asyncio.create_subprocess_exec("awk", "-f", "extract_errors.awk", LOG_FILE,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )
    stdout_awk, _ = await process_awk.communicate()
    awk_result = stdout_awk.decode().strip()
    
    # 3. Ghép 2 kết quả lại theo format đề yêu cầu
    summary_report = "Log Level Summary:\n" + bash_result + "\nError Timestamps:\n" + awk_result
    return summary_report

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_ip = address[0]
    client_port = address[1]
    
    print(f"[SERVER] Client connected from {client_ip}:{client_port}")
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        # Đọc 8192 bytes (dư sức chứa file log.txt)
        data = await reader.read(8192)
        if data:
            log_content = data.decode()
            print(f"[SERVER] Received log file from {client_ip}:{client_port}")

            # Lưu vào server_log.txt
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                f.write(log_content)
                
            # Phân tích log bằng Bash & AWK
            print("[SERVER] Processing logs using Bash and AWK...")
            summary_report = await process_logs()
            
            # Gửi báo cáo tổng hợp lại cho Client
            writer.write(summary_report.encode())
            await writer.drain()
            print(f"[SERVER] Sent summary report to {client_ip}:{client_port}")

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
