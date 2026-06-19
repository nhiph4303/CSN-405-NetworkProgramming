import asyncio
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "server.log"

users = {
    "Hanh_Nhi": "123456",
    "user2": "network",
    "user3": "python"
}

def write_log(port, username, result):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {username} {result}\n")

async def run_audit():
    process = await asyncio.create_subprocess_exec("bash", "audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    try:
        data = await reader.readline()
        message = data.decode().strip()
        parts = message.split()

        if len(parts) != 2:
            username = "UNKNOWN"
            password = "LOGIN_FAIL"
        else:
            username = parts[0]
            password = parts[1]

            if username in users and users[username] == password:
                result = "LOGIN_SUCCESS"
            else:
                result = "LOGIN_FAIL"
        
        write_log(client_port, username, result)
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
    print("[SERVER] is running")

    async with server:
        await server.serve_forever()

asyncio.run(main())