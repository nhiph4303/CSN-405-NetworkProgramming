import asyncio

HOST = '127.0.0.1'
PORT = 5000

async def main():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] connected to server")
        
        while True:
            try:
                numbers = input("[CLIENT] Enter numbers: ")
            except EOFError:
                break
                
            if not numbers.strip():
                continue
                
            if numbers.strip().upper() == "QUIT":
                writer.write(b"QUIT")
                await writer.drain()
                response = await reader.read(1024)
                print(f"Server reply: {response.decode().strip()}")
                break
                
            writer.write(numbers.encode())
            await writer.drain()

            response = await reader.read(1024)
            if not response:
                print("[CLIENT] Server closed connection")
                break
                
            response_text = response.decode().strip()
            print(f"Server reply: {response_text}")
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        print("[CLIENT] closing connection")
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

if __name__ == "__main__":
    asyncio.run(main())
