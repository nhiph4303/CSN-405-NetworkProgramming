import asyncio
import math
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

LOG_FILE = "server.log"

def log_request(port, number, result):
    # Lấy thời gian hiện tại theo format yêu cầu
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {number} {result}\n")

# Hoàn thiện hàm kiểm tra số nguyên tố
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    port = add[1]

    data = await reader.read(100)
    data = data.decode().strip()

    print(f"[SERVER] received: {data}")

    try:
        number = int(data)
        if is_prime(number):
            results = "TRUE"
        else:
            results = "FALSE"
    except ValueError:
        print("ERROR, input invalid")
        number = data  # Lưu lại giá trị text nếu không phải là số
        results = "ERROR"
    
    # Ghi log yêu cầu
    log_request(port, number, results)
    
    # Phản hồi lại cho client
    writer.write(f"[SERVER] {results}\n".encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

# Đưa hàm main ra ngoài (xóa thụt lề sai)
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] server is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
