import asyncio
import math
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000

LOG_FILE = "server.log"

def log_request(port, request, result):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time}] {port} {request} {result}\n")

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def get_next_prime(n):
    if n <= 2:
        return 2
    p = n
    while True:
        if is_prime(p):
            return p
        p += 1

def get_fact(n):
    if n < 0 or n > 100:
        return "ERROR"
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

async def handle_client(reader, writer):
    add = writer.get_extra_info("peername")
    port = add[1]
    
    print(f"[SERVER] Client connected from port {port}")

    while True:
        data = await reader.read(1024)
        if not data:
            break
        
        message = data.decode().strip()
        if not message:
            continue
            
        print(f"[SERVER] received: {message}")
        
        parts = message.split()
        command = parts[0].upper()
        
        if command == "QUIT":
            log_request(port, command, "BYE")
            writer.write(b"[SERVER] BYE\n")
            await writer.drain()
            break
            
        if len(parts) < 2:
            results = "ERROR"
            log_request(port, message, results)
            writer.write(f"[SERVER] {results}\n".encode())
            await writer.drain()
            continue
            
        try:
            n = int(parts[1])
            if command == "PRIME":
                results = "YES" if is_prime(n) else "NO"
            elif command == "NEXT_PRIME":
                results = str(get_next_prime(n))
            elif command == "FACT":
                results = str(get_fact(n))
            else:
                results = "ERROR"
        except ValueError:
            results = "ERROR"
            
        log_request(port, message, results)
        writer.write(f"[SERVER] {results}\n".encode())
        await writer.drain()

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
