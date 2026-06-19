import asyncio
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "q2_server.log"

def write_log(port, password, result):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {password} {result}\n")

async def run_audit():
    process = await asyncio.create_subprocess_exec("bash", "q2_audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

def check_strength(password):
    if len(password) < 8:
        return "WEAK"
    if not any(c.isupper() for c in password):
        return "WEAK"
    if not any(c.islower() for c in password):
        return "WEAK"
    if not any(c.isdigit() for c in password):
        return "WEAK"
    return "STRONG"

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    try:
        data = await reader.readline()
        password = data.decode().strip()

        if not password:
            result = "WEAK"
            password = "EMPTY_PASSWORD"
        else:
            result = check_strength(password)
        
        write_log(client_port, password, result)
        writer.write((result + "\n").encode())
        await writer.drain()

    except Exception as e:
        print("[SERVER] Error", e)

    finally:
        writer.close()
        await writer.wait_closed()
        await run_audit()
        print("[SERVER] Client disconnected")
        
async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print("[SERVER] Q2 Password Checker is running")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
