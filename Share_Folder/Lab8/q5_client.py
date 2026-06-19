import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

HOST = "127.0.0.1"
PORT = 25000

def load_private_key():
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())

def load_aes_key():
    with open("aes.key", "rb") as f:
        return f.read()
    
def encrypt_aes_gcm(message, aes_key):
    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, ciphertext, tag

def sign_data(data, private_key):
    signature = rsa.sign(data, private_key, "SHA-256")
    return signature

async def send_encrypted_signed_message():
    private_key = load_private_key()
    aes_key = load_aes_key()
    
    message = input("Enter a message: ")

    nonce, ciphertext, tag = encrypt_aes_gcm(message, aes_key)
    print("[CLIENT] Message encrypted with AES-GCM.")

    signature = sign_data(ciphertext, private_key)
    print("[CLIENT] Ciphertext signed with RSA.")

    tamper_choice = input("Do you want to tamper the ciphertext before sending? (y/n): ")
    if tamper_choice.lower() == "y":
        ciphertext = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
        print("[CLIENT] Ciphertext tampered!")

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

async def main():
    await send_encrypted_signed_message()

if __name__ == "__main__":
    asyncio.run(main())
