import asyncio
import rsa
import json
import base64
from datetime import datetime
from Crypto.Cipher import AES

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "0.0.0.0"
PORT = 8080
LOG_FILE = "secure_server_log.txt"

# ==========================================
# [LOGIC ĐỀ BÀI: TẠO KHÓA RSA LÚC KHỞI ĐỘNG]
# ==========================================
print("[SERVER] Generating RSA key pair (2048-bit)...")
public_key, private_key = rsa.newkeys(2048)

def write_log(ip, port, message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] Client {ip}:{port} securely sent:\n")
        f.write(message)
        f.write("\n" + "="*50 + "\n")

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_ip = address[0]
    client_port = address[1]
    
    print(f"[SERVER] Client connected from {client_ip}:{client_port}")
    
    try:
        # ==========================================
        # [LOGIC ĐỀ BÀI: TRAO ĐỔI KHÓA]
        # ==========================================
        # 1. Gửi Public Key cho Client
        pub_key_pem = public_key.save_pkcs1()
        writer.write(pub_key_pem + b"\n---END_PUB---\n")
        await writer.drain()
        print(f"[SERVER] Sent RSA Public Key to {client_ip}:{client_port}")

        # 2. Nhận AES Key (đã được mã hóa bằng RSA Public Key) từ Client
        enc_aes_b64 = await reader.readline()
        enc_aes = base64.b64decode(enc_aes_b64.strip())
        
        # 3. Giải mã lấy AES Key bằng RSA Private Key
        aes_key = rsa.decrypt(enc_aes, private_key)
        print(f"[SERVER] Successfully decrypted AES key from {client_ip}:{client_port}")

        # ==========================================
        # [LOGIC ĐỀ BÀI: NHẬN VÀ GIẢI MÃ DỮ LIỆU AES]
        # ==========================================
        data = await reader.readline()
        if data:
            # Code mẫu Lab 8: Bóc tách gói tin JSON
            packet = json.loads(data.decode().strip())
            nonce = base64.b64decode(packet["nonce"])
            ciphertext = base64.b64decode(packet["ciphertext"])
            tag = base64.b64decode(packet["tag"])

            # Giải mã bằng AES-GCM
            cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
            message_bytes = cipher.decrypt_and_verify(ciphertext, tag)
            message = message_bytes.decode()

            print(f"[SERVER] Received and decrypted system report from {client_ip}:{client_port}")
            
            # Ghi log file
            write_log(client_ip, client_port, message)
            
            writer.write("Secure system report received successfully.\n".encode())
            await writer.drain()

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
