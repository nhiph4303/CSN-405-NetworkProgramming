import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] connected to server")
        print("--- Available commands ---")
        print("  PRIME n      (e.g. PRIME 17)")
        print("  NEXT_PRIME n (e.g. NEXT_PRIME 20)")
        print("  FACT n       (e.g. FACT 10)")
        print("  QUIT")
        print("--------------------------")

        while True:
            command = input("Client: ")
            if not command:
                continue
                
            writer.write(command.encode())
            await writer.drain()

            print(f"[CLIENT] sent server: {command}")

            response = await reader.read(1024)
            if not response:
                print("[CLIENT] Server closed connection")
                break
                
            response_text = response.decode().strip()
            print(f"Server: {response_text}")
            
            if command.strip().upper() == "QUIT":
                break
                
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("[CLIENT] closing connection")
        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
