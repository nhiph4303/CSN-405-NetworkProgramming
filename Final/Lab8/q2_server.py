import asyncio
import json

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    client_id = addr[0]
    print(f"[SERVER] Client connected from {client_id}")
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        data = await reader.readline()
        data = data.decode().strip()
        
        # ==========================================
        # [LOGIC ĐỀ BÀI: XỬ LÝ MESSAGE]
        # ==========================================
        # Lẽ ra ở đây phải kiểm tra chữ ký RSA, nhưng theo code hiện tại chỉ in ra tin nhắn
        packet = json.loads(data)
        print(f"[SERVER] received message: {packet['message']}")
        result = "Valid"
    
    except Exception as e:
        print(f"[ERROR] {e}")
        result = "Invalid"

    print(f"[SERVER] verified result: {result}")
    
    # ==========================================
    # [SƯỜN BẮT BUỘC: TRẢ KẾT QUẢ VÀ ĐÓNG KẾT NỐI]
    # ==========================================
    writer.write((result + "\n").encode())
    await writer.drain()
    
    writer.close()
    await writer.wait_closed()
    print(f"[SERVER] Closed connection from {client_id}")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Server is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
