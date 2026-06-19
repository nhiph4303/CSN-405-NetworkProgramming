import asyncio
import subprocess
import rsa
import json
import base64
import os
from Crypto.Cipher import AES

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 8080

# ==========================================
# [LOGIC ĐỀ BÀI: MÃ HÓA AES-GCM VÀ RSA]
# ==========================================
def encrypt_aes_gcm(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, ciphertext, tag

async def send_encrypted_system_info():
    print("[CLIENT] Running system_monitor.sh...")
    try:
        result = subprocess.run(["bash", "system_monitor.sh"], capture_output=True, text=True)
        message = result.stdout
        if not message:
            message = "[WARNING] No system information retrieved. Are you running on Windows?"
    except Exception as e:
        message = f"[ERROR] Failed to run bash script: {e}"

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print(f"[CLIENT] Connected to Server {HOST}:{PORT}")

    # 1. Nhận RSA Public Key từ Server
    pub_key_data = await reader.readuntil(b"---END_PUB---\n")
    pub_key_pem = pub_key_data.replace(b"---END_PUB---\n", b"").strip()
    server_public_key = rsa.PublicKey.load_pkcs1(pub_key_pem)
    print("[CLIENT] Received RSA Public Key from server.")

    # 2. Sinh khóa AES
    aes_key = os.urandom(32)
    
    # 3. Mã hóa khóa AES bằng RSA Public Key
    enc_aes_key = rsa.encrypt(aes_key, server_public_key)
    writer.write(base64.b64encode(enc_aes_key) + b"\n")
    await writer.drain()

    # 4. Mã hóa nội dung bằng AES-GCM (Dùng hàm chuẩn Lab 8)
    nonce, ciphertext, tag = encrypt_aes_gcm(message, aes_key)

    packet = {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }
    
    writer.write((json.dumps(packet) + "\n").encode())
    await writer.drain()
    print("[CLIENT] Sent encrypted data to server.")

    response = await reader.readline()
    print(f"[CLIENT] Server replied: {response.decode().strip()}")

    writer.close()
    await writer.wait_closed()
    print("[CLIENT] Disconnected.")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC CLIENT]
# ==========================================
async def main():
    await send_encrypted_system_info()

if __name__ == "__main__":
    asyncio.run(main())
