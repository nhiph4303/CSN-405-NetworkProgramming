import asyncio
import json

HOST = "127.0.0.1"
PORT = 25000

async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    client_id = addr[0]
    print(f"[SERVER] Client connected from {client_id}")
    try:
        data = await reader.readline()
        data = data.decode().strip()
        
        packet = json.loads(data)
        print(f"[SERVER] received message: {packet['message']}")
        result = "Valid"
    
    except Exception as e:
        print(f"[ERROR] {e}")
        result = "Invalid"

    print(f"[SERVER] verified result: {result}")
    
    writer.write((result + "\n").encode())
    await writer.drain()
    
    writer.close()
    await writer.wait_closed()
    print(f"[SERVER] Closed connection from {client_id}")


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Server is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
