import asyncio
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8888
LOG_FILE = "q3_server.log"

def write_log(port, score, result):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{current_time}] {port} {score} {result}\n")

async def run_audit():
    process = await asyncio.create_subprocess_exec("bash", "q3_audit.sh",
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE                                               
    )

    stdout, stderr = await process.communicate()
    print("[SERVER] Audit result")
    print(stdout.decode())

    if stderr:
        print("[SERVER] Audit error: ", stderr.decode())

def check_score(score_str):
    try:
        score = float(score_str)
        if score >= 8:
            return "EXCELLENT"
        elif score >= 6:
            return "GOOD"
        elif score >= 5:
            return "AVERAGE"
        else:
            return "POOR"
    except ValueError:
        return "INVALID"

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    client_port = address[1]
    try:
        data = await reader.readline()
        score_str = data.decode().strip()

        if not score_str:
            result = "INVALID"
            score_str = "EMPTY"
        else:
            result = check_score(score_str)
        
        write_log(client_port, score_str, result)
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
    print("[SERVER] Q3 Grade Classification is running")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
