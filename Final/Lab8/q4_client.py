import asyncio
import rsa
import base64
import json

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ TCP CLIENT]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

# ==========================================
# [LOGIC ĐỀ BÀI: KÝ ĐIỆN TỬ BẰNG PRIVATE KEY]
# ==========================================
def load_private_key():
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())
    
def sign_message(message, private_key):
    # Ký bằng SHA-256
    signature = rsa.sign(message.encode(), private_key, "SHA-256")
    # Encode Base64 để gửi qua mạng
    signature_base64 = base64.b64encode(signature).decode()
    return signature_base64


async def send_signed_message():
    private_key = load_private_key()
    message = input("Enter a message: ")

    # Yêu cầu 6: Sign the original message (Phải ký chữ ký lúc message còn nguyên vẹn)
    signature_text = sign_message(message, private_key)
    print("[CLIENT] signed message")
    
    # ==========================================
    # [LOGIC ĐỀ BÀI: TAMPERED MESSAGE TEST]
    # ==========================================
    # Yêu cầu 3: Do you want to tamper the message before sending? y/n:
    tamper_choice = input("Do you want to tamper the message before sending? (y/n): ")
    
    # Yêu cầu 5 & 7: If the user selects y, then tamper with the message
    if tamper_choice.lower() == "y":
        message += "[TAMPERED]"
        print(f"[CLIENT] Tempered message: {message}")
    # Yêu cầu 4: Nếu n thì giữ nguyên message ban đầu.

    # Yêu cầu 8: Send the tampered message along with the original message's signature.
    # Đóng gói dữ liệu json. Lúc này nếu bị tamper thì message đã thay đổi, nhưng signature vẫn là của message cũ.
    packet = {
        "message" : message,
        "signature" : signature_text
    }

    data = json.dumps(packet) + "\n"

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP VỚI SERVER]
    # ==========================================
    reader , writer = await asyncio.open_connection(HOST,PORT)
    print("[CLIENT] connected to server")

    writer.write(data.encode())
    await writer.drain()
    print("[CLIENT] sent data")

    response = await reader.readline()
    print(f"[CLIENT] server replied: {response.decode().strip()}")
    
    writer.close()
    await writer.wait_closed()
    print("[CLIENT] client disconnection")

# ==========================================
# [SƯỜN BẮT BUỘC: CHẠY ASYNC CLIENT]
# ==========================================
async def main():
    await send_signed_message()

if __name__ == "__main__":
    asyncio.run(main())