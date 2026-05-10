import asyncio    # 🆕 ASYNCIO: thay thế threading — xử lý nhiều client bất đồng bộ
import datetime   # ✅ TÁI SỬ DỤNG: lấy ngày/giờ (từ Q2)

HOST = "127.0.0.1"
PORT = 5000

# 🆕 ASYNCIO: Hàm xử lý client phải là async coroutine
# reader: nhận data | writer: gửi data (thay thế client_socket)
async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')   # 🆕 ASYNCIO: lấy địa chỉ client
    print(f"[SERVER] Client connected from {addr}")

    try:
        # ✅ TÁI SỬ DỤNG: Vòng lặp xử lý request (logic giống Q2)
        while True:
            # 🆕 ASYNCIO: await reader.read() thay vì client_socket.recv()
            data = await reader.read(1024)
            if not data:
                break

            request = data.decode().strip()

            # ✅ TÁI SỬ DỤNG: Xử lý quit/exit (giống Q2)
            if request in ["quit", "exit"]:
                break

            # ✅ TÁI SỬ DỤNG: Logic SEND_DATE / SEND_TIME (giống Q2)
            if request == "SEND_DATE":
                response = datetime.datetime.now().strftime("%Y-%m-%d")
            elif request == "SEND_TIME":
                response = datetime.datetime.now().strftime("%H:%M:%S")
            else:
                response = "Invalid request. Use SEND_DATE or SEND_TIME."

            # 🆕 ASYNCIO: writer.write() + await drain() thay vì sendall()
            writer.write(response.encode())
            await writer.drain()   # đảm bảo data được gửi đi

    except Exception as e:
        print(f"Error with {addr}: {e}")
    finally:
        # 🆕 ASYNCIO: writer.close() thay vì client_socket.close()
        writer.close()
        print(f"[SERVER] Client {addr} disconnected.")

# 🆕 ASYNCIO: Hàm main khởi động async server
async def main():
    # 🆕 ASYNCIO: asyncio.start_server() thay vì socket.bind() + listen()
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] The server is listening on {HOST}:{PORT} ...")

    async with server:
        await server.serve_forever()   # 🆕 ASYNCIO: chạy mãi mãi

# 🆕 ASYNCIO: Khởi động event loop — thay thế while True: accept()
asyncio.run(main())

