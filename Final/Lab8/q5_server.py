import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ SERVER TCP]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

# ==========================================
# [LOGIC ĐỀ BÀI: TẢI KHÓA AES & RSA]
# ==========================================
def load_public_key():
    # Yêu cầu 3.3: Load the RSA public key from client_public.pem.
    with open("client_public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def load_aes_key():
    # Yêu cầu 3.2: Load the AES key from aes.key.
    with open("aes.key", "rb") as f:
        return f.read()

# ==========================================
# [LOGIC ĐỀ BÀI: GIẢI MÃ VÀ XÁC MINH (VERIFY)]
# ==========================================
def verify_signature(data, signature, public_key):
    try:
        rsa.verify(data, signature, public_key)
        return True
    except Exception:
        return False

def decrypt_aes_gcm(nonce, ciphertext, tag, aes_key):
    try:
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except Exception as e:
        return None

async def handle_client(reader, writer):
    public_key = handle_client.public_key
    aes_key = handle_client.aes_key
    
    try:
        # ==========================================
        # [SƯỜN BẮT BUỘC: NHẬN DỮ LIỆU TỪ CLIENT]
        # ==========================================
        data = await reader.readline()
        data = data.decode().strip()
        
        # Yêu cầu 3.4: Receive JSON from the client.
        packet = json.loads(data)
        
        # Chuyển đổi ngược từ Base64 về dạng byte
        nonce = base64.b64decode(packet["nonce"])
        ciphertext = base64.b64decode(packet["ciphertext"])
        tag = base64.b64decode(packet["tag"])
        signature = base64.b64decode(packet["signature"])

        # Yêu cầu 3.5: Verify the signature first.
        is_valid = verify_signature(ciphertext, signature, public_key)

        if is_valid:
            # Yêu cầu 3.6: If the signature is valid, decrypt the ciphertext.
            print("[SERVER] Signature result: VALID")
            
            plaintext = decrypt_aes_gcm(nonce, ciphertext, tag, aes_key)
            if plaintext:
                print(f"[SERVER] Decrypted message: {plaintext}")
            else:
                print("[SERVER] Message rejected. (Tag mismatch)")
                
            writer.write(b"VALID\n")
        else:
            # Yêu cầu 3.7: If the signature is invalid, do not decrypt the message.
            print("[SERVER] Signature result: INVALID")
            print("[SERVER] Message rejected.")
            writer.write(b"INVALID\n")
            
    except Exception as e:
        print("[SERVER] Signature result: INVALID")
        print("[SERVER] Message rejected.")
        writer.write(b"INVALID\n")

    # ==========================================
    # [SƯỜN BẮT BUỘC: TRẢ KẾT QUẢ VÀ ĐÓNG KẾT NỐI]
    # ==========================================
    await writer.drain()
    writer.close()
    await writer.wait_closed()

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC SERVER]
# ==========================================
async def main():
    # Yêu cầu 3.1: The AES server needs: Load AES key and RSA public key
    public_key = load_public_key()
    aes_key = load_aes_key()
    handle_client.public_key = public_key
    handle_client.aes_key = aes_key
    
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
