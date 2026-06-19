import asyncio

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = '127.0.0.1'
PORT = 30000

# ==========================================
# [HÀM XỬ LÝ CLIENT]
# ==========================================
async def handle_client(reader, writer):
    address = writer.get_extra_info('peername')
    print(f"[SERVER] Client connected from {address}")
    
    try:
        # Nhận mã Hash do Client gửi lên
        data = await reader.read(1024)
        if data:
            received_hash = data.decode('utf-8').strip()
            print(f"[SERVER] Received Hash from Client: {received_hash}")
            
            # Ghi chú: Trong thực tế Server sẽ tự băm file gốc trên máy nó rồi so sánh.
            # Ở đây ta giả lập Server luôn xác nhận là khớp để Client dễ test UI.
            result = "MATCH"
            
            # Trả kết quả về cho Client
            writer.write(result.encode('utf-8'))
            await writer.drain()
            print(f"[SERVER] Sent result '{result}' to {address}")
            
    except Exception as e:
        print(f"[SERVER] Error handling client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"[SERVER] Client disconnected.")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] is listening on {HOST}:{PORT}")
    
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
