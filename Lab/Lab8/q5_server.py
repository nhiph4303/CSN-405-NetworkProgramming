import asyncio
import rsa
import base64
import json
from Crypto.Cipher import AES

HOST = "127.0.0.1"
PORT = 25000

def load_public_key():
    with open("client_public.pem", "rb") as f:
        return rsa.PublicKey.load_pkcs1(f.read())

def load_aes_key():
    with open("aes.key", "rb") as f:
        return f.read()

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
        data = await reader.readline()
        data = data.decode().strip()
        packet = json.loads(data)
        
        nonce = base64.b64decode(packet["nonce"])
        ciphertext = base64.b64decode(packet["ciphertext"])
        tag = base64.b64decode(packet["tag"])
        signature = base64.b64decode(packet["signature"])

        is_valid = verify_signature(ciphertext, signature, public_key)

        if is_valid:
            print("[SERVER] Signature result: VALID")
            
            plaintext = decrypt_aes_gcm(nonce, ciphertext, tag, aes_key)
            if plaintext:
                print(f"[SERVER] Decrypted message: {plaintext}")
            else:
                print("[SERVER] Message rejected. (Tag mismatch)")
                
            writer.write(b"VALID\n")
        else:
            print("[SERVER] Signature result: INVALID")
            print("[SERVER] Message rejected.")
            writer.write(b"INVALID\n")
            
    except Exception as e:
        print("[SERVER] Signature result: INVALID")
        print("[SERVER] Message rejected.")
        writer.write(b"INVALID\n")

    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
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
