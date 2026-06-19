import asyncio
import rsa
import base64
import json

# ==========================================
# [SƯỜN BẮT BUỘC: THÔNG SỐ KẾT NỐI TCP]
# ==========================================
HOST = "127.0.0.1"
PORT = 25000

# ==========================================
# [LOGIC ĐỀ BÀI: TẢI KHÓA VÀ KÝ XÁC THỰC]
# ==========================================
def load_private_key():
    # Yêu cầu 1: Load the private key from the client_private.pem file.
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())
    
def sign_message(message, private_key):
    # Yêu cầu 3 & 4: Sign the message using the RSA private key & Use SHA-256
    signature = rsa.sign(message.encode(), private_key, "SHA-256")

    # Yêu cầu 5: Encode the signature using Base64 (để dễ truyền qua mạng)
    signature_base64 = base64.b64encode(signature).decode()
    return signature_base64

async def send_signed_message():
    private_key = load_private_key()
    
    # Yêu cầu 2: Allow the user to input a message from the keyboard.
    message = input("Enter a message: ")

    signature_text = sign_message(message, private_key)
    print("[CLIENT] signed message")
    
    # Đóng gói dữ liệu thành chuẩn JSON (từ điển Python)
    packet = {
        "message" : message,
        "signature" : signature_text
    }

    # ==========================================
    # [SƯỜN BẮT BUỘC: GIAO TIẾP CLIENT SOCKET]
    # ==========================================
    reader , writer = await asyncio.open_connection(HOST,PORT)
    print("[CLIENT] connected to server")

    # Yêu cầu 6: Send the message and signature to the server via TCP socket.
    data = json.dumps(packet) + "\n"
    writer.write(data.encode())
    await writer.drain()
    print("[CLIENT] sent data to server")

    # Yêu cầu 7: Receive the response from the server and print it on the screen.
    response = await reader.readline()
    print(f"[CLIENT] server replied: {response.decode().strip()}")
    
    writer.close()
    await writer.wait_closed()
    print("[CLIENT] Disconnection")

async def main():
    await send_signed_message()

if __name__ == "__main__":
    asyncio.run(main())