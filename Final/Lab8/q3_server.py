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
    # Yêu cầu 1: Load the public key from the client_public.pem file.
    with open("client_public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def verify_message(message, signature_base64, public_key):
    try:
        # Yêu cầu 6: Decode the signature from Base64 to bytes.
        signature = base64.b64decode(signature_base64)
        # Yêu cầu 7: Verify the signature using the RSA public key.
        rsa.verify(message.encode(), signature, public_key)
        return True
    except Exception:
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
        # Yêu cầu 3: Wait for the client to connect.
        # Yêu cầu 4: Receive JSON data from the client.
        data = await reader.readline()
        data = data.decode().strip()
        
        # Yêu cầu 5: Extract the message and signature.
        packet = json.loads(data)
        print(f"[SERVER] Received message: {packet['message']}")

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
    # Yêu cầu 8: Return the result to the client.
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
    
    # Yêu cầu 2: Open the TCP server at 127.0.0.1:25000.
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())