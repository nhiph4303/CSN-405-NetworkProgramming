import asyncio
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

LOG_FILE = "server.log"

def log_request(port, numbers_str, result_str):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {numbers_str} {result_str}\n")

async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    port = add[1]
    
    print(f"[SERVER] Client connected from port {port}")

    while True:
        try:
            data = await reader.read(1024)
            if not data:
                break
            
            message = data.decode().strip()
            if not message:
                continue
                
            print(f"[SERVER] received: {message}")
            
            if message.upper() == "QUIT":
                log_request(port, message, "BYE")
                writer.write(b"[SERVER] BYE\n")
                await writer.drain()
                break
            
            try:
                numbers = [int(x) for x in message.split()]
                if not numbers:
                    raise ValueError("No numbers provided")
                
                total_sum = sum(numbers)
                min_val = min(numbers)
                
                result_str = f"SUM={total_sum} MIN={min_val}"
                response = f"[SERVER] {result_str}\n"
                
                log_request(port, message, result_str)
                
            except ValueError:
                response = "[SERVER] ERROR: Invalid input. Please enter integers separated by spaces.\n"
                log_request(port, message, "ERROR")
                
            writer.write(response.encode())
            await writer.drain()
            
        except Exception as e:
            print(f"[SERVER] Error handling client: {e}")
            break

    print(f"[SERVER] Client {port} disconnected")
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] server is running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
