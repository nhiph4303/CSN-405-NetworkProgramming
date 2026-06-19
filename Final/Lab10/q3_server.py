import asyncio
from datetime import datetime

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP VÀ LOG]
# ==========================================
HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "q3_server.log"

def write_log(port, score, result):
    # Lấy thời gian và ghi vào file log
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {score} {result}\n")

async def run_audit():
    # Gọi shell script phân tích log của câu 3
    process = await asyncio.create_subprocess_exec("bash", "q3_audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

# ==========================================
# [LOGIC ĐỀ BÀI: KIỂM TRA PHÂN LOẠI ĐIỂM]
# ==========================================
def check_score(score_str):
    try:
        # Ép kiểu dữ liệu sang số thực (float)
        score = float(score_str)
        # Yêu cầu: Score >= 8 -> EXCELLENT
        if score >= 8:
            return "EXCELLENT"
        # Yêu cầu: Score >= 6 -> GOOD
        elif score >= 6:
            return "GOOD"
        # Yêu cầu: Score >= 5 -> AVERAGE
        elif score >= 5:
            return "AVERAGE"
        # Yêu cầu: Score < 5 -> POOR
        else:
            return "POOR"
    except ValueError:
        # Yêu cầu: Nếu input không phải là số -> INVALID
        return "INVALID"

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        data = await reader.readline()
        score_str = data.decode().strip()

        if not score_str:
            result = "INVALID"
            score_str = "EMPTY"
        else:
            result = check_score(score_str)
        
        write_log(client_port, score_str, result)
        writer.write((result + "\n").encode())
        await writer.drain()

    except Exception as e:
        print("[SERVER] Error", e)

    finally:
        writer.close()
        await writer.wait_closed()
        # Chạy script sau khi đóng kết nối client
        await run_audit()
        print("[SERVER] Client disconnected")
        
# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print("[SERVER] Q3 Grade Classification is running")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
