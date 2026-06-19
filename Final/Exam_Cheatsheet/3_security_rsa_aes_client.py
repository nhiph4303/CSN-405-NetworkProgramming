import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

# =====================================================================
# SƯỜN BẢO MẬT CLIENT (RSA, AES, CHỮ KÝ) (LAB 8)
# Dùng khi đề yêu cầu: 
# 1. Mã hóa dữ liệu bằng AES-GCM
# 2. Ký dữ liệu bằng Private Key (RSA)
# 3. Gửi chuỗi JSON sang Server
# =====================================================================

HOST = "127.0.0.1"
PORT = 25000

# Hàm Load Private Key để ký (Thường tạo sẵn file pem hoặc đề cho)
def load_private_key():
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

# Hàm Load AES Key để mã hóa
def load_aes_key():
    with open("aes.key", "rb") as f:
        return f.read()
    
# Hàm mã hóa AES-GCM (Bắt buộc dùng AES.MODE_GCM)
def encrypt_aes_gcm(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, ciphertext, tag

# Hàm ký điện tử RSA (Băm SHA-256)
def sign_data(data, private_key):
    # data ở đây có thể là chuỗi hoặc ciphertext (byte)
    # Hàm rsa.sign nhận bytes.
    if isinstance(data, str):
        data = data.encode()
    signature = rsa.sign(data, private_key, "SHA-256")
    return signature

async def main():
    private_key = load_private_key()
    aes_key = load_aes_key()
    
    # [VÙNG CẦN SỬA KHI THI] - Đề yêu cầu lấy dữ liệu gì thì lấy ở đây
    message = input("Nhập thông điệp bảo mật: ")

    # 1. MÃ HÓA
    nonce, ciphertext, tag = encrypt_aes_gcm(message, aes_key)
    
    # 2. KÝ ĐIỆN TỬ (Ký trên bản mã ciphertext)
    signature = sign_data(ciphertext, private_key)
    
    # (Tùy chọn đề bài: Có thể sửa đổi ciphertext để demo việc giả mạo gói tin)
    # ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])

    # 3. MÃ HÓA BASE64 để có thể đưa vào chuỗi JSON (Vì byte không gửi bằng JSON được)
    nonce_b64 = base64.b64encode(nonce).decode()
    ciphertext_b64 = base64.b64encode(ciphertext).decode()
    tag_b64 = base64.b64encode(tag).decode() 
    signature_b64 = base64.b64encode(signature).decode()

    # 4. ĐÓNG GÓI JSON
    packet = {
        "nonce": nonce_b64,
        "ciphertext": ciphertext_b64,
        "tag": tag_b64,
        "signature": signature_b64
    }
    
    # Chuyển JSON Dict thành chuỗi và thêm ký tự xuống dòng \n
    data_to_send = json.dumps(packet) + "\n"

    # GỬI ĐI BẰNG ASYNCIO
    reader, writer = await asyncio.open_connection(HOST, PORT)
    writer.write(data_to_send.encode())
    await writer.drain()

    # Nhận kết quả
    response = await reader.readline()
    print(f"[CLIENT] Server trả lời: {response.decode().strip()}")
    
    writer.close()
    await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
