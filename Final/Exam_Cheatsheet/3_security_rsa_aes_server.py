import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

# =====================================================================
# SƯỜN BẢO MẬT SERVER (RSA, AES, CHỮ KÝ) (LAB 8)
# Dùng khi đề yêu cầu: 
# 1. Nhận chuỗi JSON chứa Ciphertext, Nonce, Tag, Signature
# 2. Kiểm tra chữ ký bằng Public Key (Xác thực)
# 3. Giải mã dữ liệu bằng AES-GCM (Bảo mật)
# =====================================================================

HOST = "127.0.0.1"
PORT = 25000

# Hàm Load Public Key của Client để kiểm tra chữ ký
def load_public_key():
    with open("client_public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

# Hàm Load AES Key để giải mã
def load_aes_key():
    with open("aes.key", "rb") as f:
        return f.read()

# Hàm Kiểm tra chữ ký RSA
def verify_signature(data, signature, public_key):
    try:
        # Nếu hàm chạy thành công tức là chữ ký chuẩn
        rsa.verify(data, signature, public_key)
        return True
    except Exception:
        return False

# Hàm Giải mã AES-GCM
def decrypt_aes_gcm(nonce, ciphertext, tag, aes_key):
    try:
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except Exception as e:
        return None # Trả về None nếu Tag sai (Dữ liệu bị sửa đổi)

async def handle_client(reader, writer):
    # Lấy key từ biến toàn cục của hàm
    public_key = handle_client.public_key
    aes_key = handle_client.aes_key
    
    try:
        # 1. NHẬN VÀ PHÂN TÍCH CHUỖI JSON
        data = await reader.readline()
        if not data:
            return
            
        data = data.decode().strip()
        packet = json.loads(data)
        
        # 2. GIẢI MÃ BASE64 VỀ LẠI ĐỊNH DẠNG BYTE
        nonce = base64.b64decode(packet["nonce"])
        ciphertext = base64.b64decode(packet["ciphertext"])
        tag = base64.b64decode(packet["tag"])
        signature = base64.b64decode(packet["signature"])

        # 3. KIỂM TRA CHỮ KÝ (Xác thực)
        is_valid = verify_signature(ciphertext, signature, public_key)

        if is_valid:
            print("[SERVER] Chữ ký HỢP LỆ (Gói tin từ đúng người)")
            
            # 4. GIẢI MÃ DỮ LIỆU CHÍNH (Bảo mật & Toàn vẹn)
            plaintext = decrypt_aes_gcm(nonce, ciphertext, tag, aes_key)
            if plaintext:
                print(f"[SERVER] Nội dung đã giải mã: {plaintext}")
                # [SỬA TẠI ĐÂY NẾU CẦN XỬ LÝ LOGIC TRÊN PLAINTEXT VÀ TRẢ KẾT QUẢ KHÁC]
                writer.write(b"VALID\n")
            else:
                print("[SERVER] Giải mã thất bại (Dữ liệu bị can thiệp - Lỗi Tag)")
                writer.write(b"INVALID\n")
        else:
            print("[SERVER] Chữ ký KHÔNG HỢP LỆ (Gói tin giả mạo)")
            writer.write(b"INVALID\n")
            
    except Exception as e:
        print("[SERVER] Lỗi xử lý dữ liệu.")
        writer.write(b"ERROR\n")

    finally:
        await writer.drain()
        writer.close()
        await writer.wait_closed()


async def main():
    # Load Key 1 lần duy nhất khi Server khởi động
    public_key = load_public_key()
    aes_key = load_aes_key()
    
    # Mẹo truyền key vào hàm handle_client mà không xài biến global
    handle_client.public_key = public_key
    handle_client.aes_key = aes_key
    
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Đang chờ kết nối Security tại {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
