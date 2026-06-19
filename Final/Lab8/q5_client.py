import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

# ==========================================
# [LOGIC ĐỀ BÀI: TẢI KHÓA AES & RSA]
# ==========================================
def load_private_key():
    # Yêu cầu 2.2: Load the RSA private key from client_private.pem.
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def load_aes_key():
    # Yêu cầu 2.1: Load the AES key from aes.key.
    with open("aes.key", "rb") as f:
        return f.read()
    
# ==========================================
# [LOGIC ĐỀ BÀI: MÃ HÓA AES-GCM VÀ KÝ RSA]
# ==========================================
def encrypt_aes_gcm(message, aes_key):
    # Yêu cầu 2.4: Encrypt the message using AES-GCM.
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    # GCM trả về 3 thành phần: nonce (muối), ciphertext (dữ liệu mã hóa), tag (mã xác thực)
    return cipher.nonce, ciphertext, tag

def sign_data(data, private_key):
    # Yêu cầu 2.5: Sign the encrypted data using the RSA private key.
    signature = rsa.sign(data, private_key, "SHA-256")
    return signature

async def send_encrypted_signed_message():
    private_key = load_private_key()
    aes_key = load_aes_key()
    
    # Yêu cầu 2.3: Enter the message from the keyboard.
    message = input("Enter a message: ")

    nonce, ciphertext, tag = encrypt_aes_gcm(message, aes_key)
    print("[CLIENT] Message encrypted with AES-GCM.")

    signature = sign_data(ciphertext, private_key)
    print("[CLIENT] Ciphertext signed with RSA.")

    # Cho phép user phá hoại dữ liệu để test tính bảo mật của RSA
    tamper_choice = input("Do you want to tamper the ciphertext before sending? (y/n): ")
    if tamper_choice.lower() == "y":
        ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
        print("[CLIENT] Ciphertext tampered!")

    # Yêu cầu 2.6: Send the nonce, ciphertext, and signature to the server.
    # Phải encode b64 toàn bộ các chuỗi byte để gửi bằng định dạng chuỗi JSON
    nonce_b64 = base64.b64encode(nonce).decode()
    ciphertext_b64 = base64.b64encode(ciphertext).decode()
    tag_b64 = base64.b64encode(tag).decode() 
    signature_b64 = base64.b64encode(signature).decode()

    packet = {
        "nonce": nonce_b64,
        "ciphertext": ciphertext_b64,
        "tag": tag_b64,
        "signature": signature_b64
    }

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader, writer = await asyncio.open_connection(HOST, PORT)
    print("[CLIENT] Connected to server.")

    data = json.dumps(packet) + "\n"
    writer.write(data.encode())
    await writer.drain()
    print("[CLIENT] Sent encrypted data and signature to server.")

    response = await reader.readline()
    print(f"[CLIENT] Server replied: {response.decode().strip()}")
    
    writer.close()
    await writer.wait_closed()
    print("[CLIENT] Disconnected.")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC CLIENT]
# ==========================================
async def main():
    await send_encrypted_signed_message()

if __name__ == "__main__":
    asyncio.run(main())
