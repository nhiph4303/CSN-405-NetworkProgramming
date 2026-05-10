# 📚 CSN405 — MIDTERM Q&A (Full English → Full Vietnamese)

---

# 🇬🇧 ENGLISH VERSION

---

## SECTION A: PROGRAMS, PROCESSES & THREADS

**Q: What is a program?**
A program is a static set of instructions (code) and data stored on disk. It does nothing by itself until it is executed.

**Q: What is a process? How is it different from a program?**
A process is a **program in execution**. When you run a program, the OS loads it into memory and creates a process. A program is passive (just a file); a process is active (running, using CPU, memory, etc.).
- Example: `python server.py` running → that is a process.
- A program has 2 parts: **code** and **data**.

**Q: What is a thread?**
A thread is the smallest unit of execution within a process. A process can have multiple threads that share the same memory space. Threads within a process run concurrently (take turns on one CPU core in Python due to GIL).

**Q: How is a thread different from a process?**
| | Thread | Process |
|--|--------|---------|
| Memory | Shared within same process | Independent memory space |
| Creation | Lightweight, fast | Heavier, slower |
| Communication | Easy (shared variables) | Hard (IPC: Queue, Pipe) |
| Failure impact | One crashed thread affects all | One crashed process doesn't affect others |

**Q: What is sequential programming?**
Sequential programming executes code **line by line**, one instruction at a time. Each step must finish before the next begins.

**Q: What is concurrency vs parallelism?**
- **Concurrency**: Multiple tasks are **in progress** at the same time, but not necessarily running at the exact same instant. They take turns (interleaving). Example: Python threads (GIL).
- **Parallelism**: Multiple tasks run at the **exact same moment** on multiple CPU cores. Example: Python multiprocessing.
- Key difference: Concurrency is about **dealing with** multiple tasks; parallelism is about **doing** multiple tasks simultaneously.

**Q: When to use threads vs processes?**
- **Threads** → I/O-bound tasks (network, file I/O) — lightweight, shared memory
- **Processes** → CPU-bound tasks (heavy computation) — bypasses GIL, truly parallel

**Q: What is Blocking? Why does it happen? Solutions?**
- **Blocking**: A function call that does not return until the operation completes (e.g., `accept()`, `recv()` wait indefinitely).
- **Why**: The OS pauses the thread/process until the I/O event finishes.
- **Solutions**:
  1. **Multithreading** — each client gets its own thread; one blocking call doesn't block others
  2. **Multiprocessing** — each client gets its own process
  3. **Async I/O** (asyncio) — non-blocking, event-loop based

**Q: Advantages/Disadvantages of Multithreading vs Multiprocessing?**
| | Multithreading | Multiprocessing |
|--|---------------|-----------------|
| Memory | Shared → less RAM | Independent → more RAM |
| Speed | Fast to create | Slower to create |
| Communication | Easy | Hard (IPC needed) |
| Crash isolation | No — one bad thread crashes all | Yes — independent |
| GIL | Limited by GIL (not truly parallel) | Bypasses GIL (truly parallel) |
| Best for | Network servers (I/O-bound) | CPU-heavy computation |

---

## SECTION B: SOCKET BASICS

**Q: What is a Socket?**
A socket is an **endpoint** for two-way communication between two programs over a network. It acts as the **bridge between the application layer and the transport layer**. A socket is identified by an IP address + port number.

**Q: What does `socket.AF_INET` mean?**
`AF_INET` = Address Family Internet → use **IPv4** addresses.

**Q: What does `socket.SOCK_STREAM` mean?**
`SOCK_STREAM` → use **TCP** (connection-oriented, reliable, ordered).

**Q: What does `socket.SOCK_DGRAM` mean?**
`SOCK_DGRAM` → use **UDP** (connectionless, unreliable, faster).

**Q: What is a welcoming socket and a connection socket?**
- **Welcoming socket** (server socket): Created first. Listens for incoming connection requests via `listen()` and `accept()`. Stays open permanently.
- **Connection socket**: Created by `accept()` automatically for each new client. Used for actual data exchange with that specific client. Closed after the client session ends.
- TCP uses **2 sockets** on server side; UDP uses **1 socket**.

**Q: Which socket does the client connect to first?**
The client connects to the **welcoming socket**. During this connection, the **3-way handshake** takes place (SYN → SYN-ACK → ACK). After handshake, `accept()` returns the new **connection socket**.

**Q: What are the steps to create a TCP server?**
```
1. socket()   → create socket (AF_INET, SOCK_STREAM)
2. bind()     → bind to (IP, port)
3. listen()   → set to listening mode
4. accept()   → wait for client; returns (connection_socket, address)
5. recv()     → receive data
6. send()     → send response
7. close()    → close connection socket
```

**Q: What are the steps for a TCP client?**
```
1. socket()   → create socket
2. connect()  → connect to server (triggers 3-way handshake)
3. send()     → send data
4. recv()     → receive response
5. close()    → close socket
```

**Q: When `accept()` succeeds, what 2 values does it return?**
It returns a **tuple**: `(connection_socket, address)`
- `connection_socket`: new socket dedicated to this client
- `address`: tuple of `(client_ip, client_port)`

**Q: How does the server know the client's IP and port in TCP?**
Via the `addr` returned by `accept()`. The OS extracts the client's IP and port from the TCP connection handshake automatically — no need to send them manually.

**Q: What is the role of `addr` from `accept()` in TCP data transfer?**
In TCP, the `addr` (client address) is **not needed** for sending data — `connection_socket.send()` already knows where to send because the connection is established. It's only useful for logging.

**Q: Why can't the client run before the server in TCP?**
When the client calls `client_socket.connect((host, port))`, it initiates a TCP 3-way handshake. If the server is not yet listening, the OS rejects the SYN packet → **"Connection refused"** error at the `connect()` line.

**Q: Why does the server use a fixed port (e.g., 80 for HTTP) but the client doesn't specify one?**
- The server needs a **well-known, fixed port** so clients know where to connect.
- The client's port is assigned **randomly by the OS** (ephemeral port, e.g., 52341). Clients don't care which port they use locally.
- If you want to fix the client port: `client_socket.bind(('', 8888))` before `connect()`.
- The server can't use a random port — clients wouldn't know which port to connect to.

**Q: Why does `server_socket.send()` not need the client's IP/port in TCP?**
Because TCP is **connection-oriented**. After `connect()` + 3-way handshake, the OS maintains the connection state. The socket already knows the destination — no need to specify address each time.

**Q: `serverSocket.bind(('', serverPort))` — why empty string instead of '127.0.0.1'?**
- `''` (empty string) or `'0.0.0.0'` means **listen on ALL network interfaces** (localhost + LAN + any IP on this machine).
- `'127.0.0.1'` means listen only on loopback (localhost only — not accessible from other machines).
- `'0.0.0.0'` and `''` are equivalent in Python socket binding.

**Q: Can a UDP server and TCP server share the same port?**
**Yes!** UDP and TCP are different protocols — the OS distinguishes them. Port 80 for TCP and port 80 for UDP are separate endpoints. They can coexist without conflict.

---

## SECTION C: UDP SPECIFICS

**Q: Why does UDP not have `listen()` and `accept()`?**
UDP is **connectionless** — there is no connection to establish, no handshake. The server simply binds to a port and waits for datagrams. Any client can send at any time without prior setup.

**Q: Why can the UDP client run before the server without error?**
`sendto()` just sends a datagram into the network without checking if anyone is listening. The OS doesn't raise an error if no server is running — the packet is simply lost. *(Client will block on `recvfrom()` waiting for a reply that never comes.)*

**Q: If the client sends UDP data before the server starts, will the server receive it?**
**No.** The datagram is sent and immediately lost because no socket is bound to that port yet. UDP does not buffer or queue packets for late-arriving servers.

**Q: Why must `sendto()` include the destination address every time?**
UDP has no persistent connection — each datagram is **independent**. The socket has no memory of previous recipients. Therefore, every call must explicitly state where to send: `sendto(data, (host, port))`.
- If you omit the address, `sendto()` raises a `TypeError` — it is a required argument.
- TCP uses `send()` without address because the connection already stores the destination.

**Q: UDP server has only 1 socket — explain.**
UDP has no concept of connections. The single `server_socket` handles **all clients**: it receives datagrams from any client via `recvfrom()` and sends replies back using `sendto(data, client_address)`. No new socket is ever created.

---

## SECTION D: TCP CODE ANALYSIS

**Q: In this code, why can Client 1 connect but Client 2 cannot interact?**
```python
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    connectionSocket.send(sentence.upper().encode())
    connectionSocket.close()
```
**Answer**: This is a **single-threaded** server. After `accept()`, the server handles Client 1 completely (recv → send → close) before looping back to `accept()` again. Client 2 connects to the welcoming socket and is queued, but cannot interact until Client 1 finishes. **Fix**: use multithreading — spawn a new thread per client.

---

## SECTION E: EMAIL PROTOCOLS & PORT NUMBERS

**Q: What protocols are needed to send an email?**
- **SMTP** (Simple Mail Transfer Protocol) — for **sending** email (port 25 / 587)
- **IMAP** or **POP3** — for **receiving** email

**Q: What is the difference between IMAP and POP3?**
| | IMAP | POP3 |
|--|------|------|
| Sync | Keeps emails on server, syncs across devices | Downloads emails to local device, removes from server |
| Multiple devices | Yes | No (designed for one device) |
| Port | 143 (993 SSL) | 110 (995 SSL) |

**Q: Well-known port numbers to memorize:**
| Protocol | Port |
|----------|------|
| HTTP | 80 |
| HTTPS | 443 |
| SSH | 22 |
| SMTP | 25 / 587 |
| IMAP | 143 |
| POP3 | 110 |
| DNS | 53 |
| FTP | 21 |

---

## SECTION F: TCP/IP PROTOCOL

**Q: Describe the TCP/IP model.**
The TCP/IP model has 4 layers:
1. **Application Layer** — HTTP, FTP, DNS, SMTP (user-facing protocols)
2. **Transport Layer** — TCP, UDP (end-to-end communication, ports)
3. **Internet Layer** — IP (routing, IP addresses)
4. **Network Access Layer** — Ethernet, WiFi (physical transmission)

Sockets are the **interface between Application Layer and Transport Layer**.

---

# 🇻🇳 PHIÊN BẢN TIẾNG VIỆT

---

## PHẦN A: CHƯƠNG TRÌNH, TIẾN TRÌNH & LUỒNG

**H: Chương trình là gì?**
Chương trình là tập hợp **tĩnh** các lệnh (code) và dữ liệu được lưu trên đĩa. Chương trình không tự làm gì cho đến khi được thực thi. Chương trình có 2 phần: **code** và **data**.

**H: Tiến trình là gì? Khác chương trình như thế nào?**
Tiến trình là **chương trình đang chạy**. Khi chạy một chương trình, hệ điều hành tải nó vào bộ nhớ và tạo ra tiến trình. Chương trình là thụ động (chỉ là file); tiến trình là chủ động (đang sử dụng CPU, bộ nhớ,...).
- Ví dụ: `python server.py` đang chạy → đó là một tiến trình.

**H: Luồng (thread) là gì?**
Luồng là đơn vị thực thi nhỏ nhất trong một tiến trình. Một tiến trình có thể có nhiều luồng dùng chung vùng nhớ. Trong Python, các luồng **luân phiên** thực thi (do GIL).

**H: Luồng khác tiến trình thế nào?**
| | Luồng | Tiến trình |
|--|-------|------------|
| Bộ nhớ | Dùng chung trong cùng tiến trình | Bộ nhớ độc lập |
| Tạo | Nhẹ, nhanh | Nặng hơn, chậm hơn |
| Giao tiếp | Dễ (biến dùng chung) | Khó (cần IPC: Queue, Pipe) |
| Lỗi | 1 luồng lỗi ảnh hưởng tất cả | 1 tiến trình lỗi không ảnh hưởng tiến trình khác |

**H: Lập trình tuần tự là gì?**
Lập trình tuần tự thực hiện code **từng dòng một**, lệnh này xong mới đến lệnh tiếp theo.

**H: Concurrency vs Parallelism khác nhau thế nào?**
- **Concurrency (Đồng thời)**: Nhiều tác vụ **đang tiến hành** cùng lúc nhưng không nhất thiết chạy đúng cùng một thời điểm. Chúng luân phiên nhau. Ví dụ: Python threads (GIL).
- **Parallelism (Song song)**: Nhiều tác vụ chạy **đúng cùng một lúc** trên nhiều lõi CPU. Ví dụ: Python multiprocessing.
- Điểm khác: Concurrency là **xử lý** nhiều việc; Parallelism là **thực hiện** nhiều việc cùng lúc thật sự.

**H: Khi nào dùng tiến trình, khi nào dùng luồng?**
- **Luồng** → Tác vụ I/O-bound (mạng, file) — nhẹ, bộ nhớ chung
- **Tiến trình** → Tác vụ CPU-bound (tính toán nặng) — thoát GIL, song song thật sự

**H: Blocking là gì? Tại sao? Giải pháp?**
- **Blocking**: Lời gọi hàm không trả về cho đến khi thao tác hoàn thành (vd: `accept()`, `recv()` chờ mãi).
- **Tại sao**: Hệ điều hành tạm dừng tiến trình/luồng cho đến khi sự kiện I/O hoàn thành.
- **Giải pháp**:
  1. **Đa luồng** — mỗi client có luồng riêng; một client bị block không ảnh hưởng client khác
  2. **Đa tiến trình** — mỗi client có tiến trình riêng
  3. **Async I/O** (asyncio) — không blocking, dựa trên event loop

**H: Ưu/nhược điểm của đa luồng và đa tiến trình?**
| | Đa luồng | Đa tiến trình |
|--|---------|--------------|
| Bộ nhớ | Dùng chung → ít RAM | Độc lập → nhiều RAM hơn |
| Tốc độ tạo | Nhanh | Chậm hơn |
| Giao tiếp | Dễ | Khó (cần IPC) |
| Cô lập lỗi | Không — 1 luồng lỗi ảnh hưởng tất cả | Có — độc lập |
| GIL | Bị giới hạn (không song song thật) | Thoát GIL (song song thật) |
| Phù hợp | Server mạng (I/O-bound) | Tính toán nặng (CPU-bound) |

---

## PHẦN B: CƠ BẢN VỀ SOCKET

**H: Socket là gì?**
Socket là **điểm cuối** cho giao tiếp hai chiều giữa hai chương trình qua mạng. Nó là **cầu nối giữa tầng ứng dụng và tầng vận chuyển**. Socket được xác định bởi địa chỉ IP + số port.

**H: `socket.AF_INET` có nghĩa gì?**
`AF_INET` = Address Family Internet → dùng địa chỉ **IPv4**.

**H: `socket.SOCK_STREAM` có nghĩa gì?**
`SOCK_STREAM` → dùng **TCP** (hướng kết nối, đáng tin cậy, có thứ tự).

**H: `socket.SOCK_DGRAM` có nghĩa gì?**
`SOCK_DGRAM` → dùng **UDP** (không kết nối, không đảm bảo, nhanh hơn).

**H: Welcoming socket và connection socket là gì?**
- **Welcoming socket**: Tạo đầu tiên. Lắng nghe kết nối đến qua `listen()` và `accept()`. Mở suốt vòng đời server.
- **Connection socket**: Được `accept()` tạo tự động cho mỗi client mới. Dùng để trao đổi dữ liệu thực với client đó. Đóng sau khi phiên kết thúc.
- TCP dùng **2 socket** phía server; UDP dùng **1 socket**.

**H: Client kết nối với socket nào trước?**
Client kết nối với **welcoming socket**. Trong lúc này diễn ra **bắt tay 3 bước** (SYN → SYN-ACK → ACK). Sau bắt tay, `accept()` trả về **connection socket** mới.

**H: Các bước tạo TCP server?**
```
1. socket()   → tạo socket (AF_INET, SOCK_STREAM)
2. bind()     → gán (IP, port)
3. listen()   → đặt chế độ lắng nghe
4. accept()   → chờ client; trả về (connection_socket, address)
5. recv()     → nhận dữ liệu
6. send()     → gửi phản hồi
7. close()    → đóng connection socket
```

**H: Khi `accept()` thành công trả về 2 giá trị nào?**
Trả về **tuple**: `(connection_socket, address)`
- `connection_socket`: socket mới dành riêng cho client này
- `address`: tuple gồm `(client_ip, client_port)`

**H: Server biết IP và port của client bằng cách nào trong TCP?**
Qua `addr` được trả về từ `accept()`. Hệ điều hành tự động trích xuất IP và port của client từ quá trình bắt tay TCP — không cần client tự gửi thông tin này.

**H: `addr` từ `accept()` có vai trò gì trong việc gửi dữ liệu TCP?**
Trong TCP, `addr` **không cần** để gửi dữ liệu — `connection_socket.send()` đã biết gửi đi đâu vì kết nối đã được thiết lập. Chỉ hữu ích cho việc ghi log.

**H: Tại sao client không thể chạy trước server trong TCP?**
Khi client gọi `client_socket.connect((host, port))`, nó khởi tạo bắt tay TCP 3 bước. Nếu server chưa lắng nghe, hệ điều hành từ chối gói SYN → lỗi **"Connection refused"** tại dòng `connect()`.

**H: Tại sao server dùng port cố định (vd: 80 cho HTTP) còn client thì không?**
- Server cần **port cố định, nổi tiếng** để client biết kết nối vào đâu.
- Port của client được **hệ điều hành gán ngẫu nhiên** (ephemeral port, vd: 52341).
- Muốn cố định port client: `client_socket.bind(('', 8888))` trước `connect()`.
- Server không dùng port ngẫu nhiên vì client sẽ không biết kết nối vào đâu.

**H: Tại sao `server_socket.send()` không cần IP/port client trong TCP?**
Vì TCP **hướng kết nối**. Sau `connect()` + bắt tay 3 bước, hệ điều hành lưu trạng thái kết nối. Socket đã biết đích đến — không cần chỉ định lại mỗi lần.

**H: `serverSocket.bind(('', serverPort))` — tại sao để chuỗi rỗng thay vì '127.0.0.1'?**
- `''` hoặc `'0.0.0.0'` = lắng nghe trên **TẤT CẢ** giao diện mạng (localhost + LAN + mọi IP trên máy).
- `'127.0.0.1'` = chỉ lắng nghe trên loopback (chỉ truy cập được từ máy đó, không từ máy khác).
- `'0.0.0.0'` và `''` tương đương nhau trong Python socket binding.

**H: UDP server và TCP server có thể dùng chung port không?**
**Có!** UDP và TCP là các giao thức khác nhau — hệ điều hành phân biệt chúng. Port 80 TCP và port 80 UDP là 2 endpoint riêng biệt, có thể cùng tồn tại.

---

## PHẦN C: UDP ĐẶC THÙ

**H: Tại sao UDP không có `listen()` và `accept()`?**
UDP là giao thức **không kết nối** — không có handshake, không có kết nối cần thiết lập. Server chỉ cần bind vào port và chờ datagram. Client nào cũng có thể gửi bất kỳ lúc nào.

**H: Tại sao UDP client chạy trước server không bị lỗi?**
`sendto()` chỉ gửi datagram vào mạng mà không kiểm tra có ai đang lắng nghe không. Hệ điều hành không báo lỗi nếu không có server — gói tin đơn giản bị mất. *(Client sẽ bị block ở `recvfrom()` chờ phản hồi mãi.)*

**H: Nếu client gửi dữ liệu UDP trước khi server chạy, server có nhận được không?**
**Không.** Datagram được gửi đi và mất ngay vì chưa có socket nào bind vào port đó. UDP không buffer hay queue gói tin cho server đến muộn.

**H: Tại sao `sendto()` phải có địa chỉ đích mỗi lần gọi?**
UDP không có kết nối liên tục — mỗi datagram **độc lập**. Socket không lưu thông tin người nhận trước đó. Mỗi lần gọi phải chỉ rõ: `sendto(data, (host, port))`.
- Bỏ địa chỉ → `TypeError` — địa chỉ là tham số bắt buộc.
- TCP dùng `send()` không cần địa chỉ vì kết nối đã lưu đích đến.

**H: UDP server chỉ có 1 socket — giải thích.**
UDP không có khái niệm kết nối. Socket duy nhất xử lý **tất cả client**: nhận datagram từ bất kỳ client nào qua `recvfrom()` và gửi lại qua `sendto(data, client_address)`. Không bao giờ tạo thêm socket.

---

## PHẦN D: PHÂN TÍCH CODE TCP

**H: Code này tại sao client 1 kết nối được nhưng client 2 không tương tác được?**
```python
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    connectionSocket.send(sentence.upper().encode())
    connectionSocket.close()
```
**Trả lời**: Đây là server **đơn luồng**. Sau `accept()`, server xử lý client 1 hoàn toàn (recv → send → close) mới quay lại `accept()`. Client 2 kết nối được vào welcoming socket và bị xếp hàng, nhưng không tương tác được cho đến khi client 1 xong. **Sửa**: dùng đa luồng — tạo thread riêng cho mỗi client.

---

## PHẦN E: GIAO THỨC EMAIL & PORT

**H: Gửi email cần các giao thức nào?**
- **SMTP** — để **gửi** email (port 25 / 587)
- **IMAP** hoặc **POP3** — để **nhận** email

**H: IMAP và POP3 khác nhau thế nào?**
| | IMAP | POP3 |
|--|------|------|
| Đồng bộ | Giữ email trên server, đồng bộ nhiều thiết bị | Tải email về thiết bị, xóa khỏi server |
| Nhiều thiết bị | Có | Không (chỉ 1 thiết bị) |
| Port | 143 (993 SSL) | 110 (995 SSL) |

**H: Số port cần nhớ:**
| Giao thức | Port |
|-----------|------|
| HTTP | 80 |
| HTTPS | 443 |
| SSH | 22 |
| SMTP | 25 / 587 |
| IMAP | 143 |
| POP3 | 110 |
| DNS | 53 |
| FTP | 21 |

---

## PHẦN F: MÔ HÌNH TCP/IP

**H: Trình bày giao thức TCP/IP.**
Mô hình TCP/IP có 4 tầng:
1. **Tầng Ứng dụng** — HTTP, FTP, DNS, SMTP (giao thức người dùng)
2. **Tầng Vận chuyển** — TCP, UDP (giao tiếp đầu-cuối, cổng)
3. **Tầng Internet** — IP (định tuyến, địa chỉ IP)
4. **Tầng Truy cập mạng** — Ethernet, WiFi (truyền vật lý)

Socket là **giao diện giữa Tầng Ứng dụng và Tầng Vận chuyển**.
