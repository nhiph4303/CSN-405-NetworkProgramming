import asyncio   # 🆕 ASYNCIO: thay thế threading — không cần tạo thread thủ công

HOST = "127.0.0.1"
PORT = 6000

# 🆕 ASYNCIO: Hàm xử lý client phải là async coroutine
# reader/writer thay thế client_socket
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')   # 🆕 ASYNCIO: lấy địa chỉ client
    client_ip   = addr[0]
    client_port = addr[1]

    try:
        # 🆕 ASYNCIO: await reader.read() thay vì client_socket.recv()
        data = await reader.read(1024)
        message = data.decode()

        # ✅ TÁI SỬ DỤNG: LOG nhận được (giống Q2)
        print(f"[LOG] Received from {client_ip}:{client_port} → {message}")

        # ✅ TÁI SỬ DỤNG: Đảo ngược + HOA + thêm IP:port (giống Q2)
        response = message[::-1].upper() + f" ({client_ip}:{client_port})"

        # 🆕 ASYNCIO: writer.write() + await drain() thay vì sendall()
        writer.write(response.encode())
        await writer.drain()   # đảm bảo data được gửi đi

        # ✅ TÁI SỬ DỤNG: LOG phản hồi đã gửi (giống Q2)
        print(f"[LOG] Sent to {client_ip}:{client_port} → {response}")

    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        # 🆕 ASYNCIO: writer.close() thay vì client_socket.close()
        writer.close()

# 🆕 ASYNCIO: Hàm main khởi động async server
async def main():
    # 🆕 ASYNCIO: asyncio.start_server() thay vì socket.bind() + listen()
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] The server is listening on {HOST}:{PORT} ...")

    async with server:
        await server.serve_forever()   # 🆕 ASYNCIO: xử lý tất cả client tự động

# 🆕 ASYNCIO: Khởi động event loop — thay thế while True: accept() + Thread
asyncio.run(main())

