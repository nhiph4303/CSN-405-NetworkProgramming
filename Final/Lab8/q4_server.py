import asyncio
import rsa
import base64
import json

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

# ==========================================
# [LOGIC ĐỀ BÀI: TẢI KHÓA VÀ XÁC MINH CHỮ KÝ]
# ==========================================
def load_public_key():
    with open("client_public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def verify_message(message, signature_base64, public_key):
    try:
        signature = base64.b64decode(signature_base64)
        rsa.verify(message.encode(), signature, public_key)
        return True
    except Exception:
        # Nếu message bị tamper (bị đổi nội dung), rsa.verify sẽ ném lỗi và trả về False
        return False

async def handle_client(reader, writer):
    public_key = handle_client.public_key
    addr = writer.get_extra_info("peername")
    client_id = addr[0]
    print(f"[SERVER] New connection from {client_id}")
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        data = await reader.readline()
        data = data.decode().strip()
        
        packet = json.loads(data)
        print(f"[SERVER] Received message: {packet['message']}")

        # Server tự động dùng chữ ký cũ đối chiếu với gói tin mới
        # Nếu Client gửi message bị gắn thêm "[TAMPERED]", hàm này chắc chắn ra False
        is_valid = verify_message(packet["message"], packet['signature'], public_key)

        if is_valid:
            result = "VALID"
        else: 
            result = "INVALID"
    
    except Exception as e:
        print(f"[ERROR] {e}")
        result = "INVALID"

    print(f"[SERVER] Verification result: {result}")

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
    public_key = load_public_key()
    handle_client.public_key = public_key
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())