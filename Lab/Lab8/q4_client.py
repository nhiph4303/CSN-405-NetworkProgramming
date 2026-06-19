import asyncio
import rsa
import base64
import json

HOST = "127.0.0.1"
PORT = 25000

def load_private_key():
    with open("client_private.pem", "rb") as f:
        return rsa.PrivateKey.load_pkcs1(f.read())
    
def sign_message(message, private_key):
    signature = rsa.sign(message.encode(), private_key, "SHA-256")

    signature_base64 = base64.b64encode(signature).decode()
    return signature_base64


async def send_signed_message():
    private_key = load_private_key()
    message = input("Enter a message: ")

    signature_text = sign_message(message, private_key)
    print("[CLIENT] signed message")
    tamper_choice = input("Do you want to tamper the message before sending? (y/n): ")
    if tamper_choice.lower() == "y":
        message += "[TAMPERED]"
        print(f"[CLIENT] Tempered message: {message}")

    packet = {
        "message" : message,
        "signature" : signature_text
    }

    data = json.dumps(packet) + "\n"

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

async def main():
    await send_signed_message()


if __name__ == "__main__":
    asyncio.run(main())