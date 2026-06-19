# 📘 TỔNG HỢP LÝ THUYẾT TỪ 7 FILE SLIDE BÀI GIẢNG

Để bạn không phải tốn thời gian mở từng file Slide hay PDF lên dò tìm trong lúc làm bài, mình đã "vắt kiệt" tất cả những khái niệm trọng tâm nhất từ 7 file Slide của thầy giáo và tóm gọn lại tại đây. Bạn chỉ cần đọc file này là đủ!

---

## 1. LECTURE 1 & WEB, MAIL, DNS (Kiến thức Mạng Cơ Bản)
*   **Giao thức (Protocol):** Định nghĩa định dạng (format), thứ tự gửi nhận tin nhắn và các hành động khi nhận được tin nhắn trên mạng.
*   **Mô hình OSI (7 Lớp):** Application -> Presentation -> Session -> Transport -> Network -> Link -> Physical. Khi truyền dữ liệu, data sẽ được bọc lại (Encapsulation) như búp bê Nga từ trên xuống dưới.
*   **Giao thức HTTP:** Chạy trên TCP. Dùng để truyền nội dung Web.
    *   **Header:** Chứa meta-data như `Content-Type` (loại dữ liệu), `Content-Length`, `User-Agent`.
    *   **Body/Data:** Nội dung thực sự của trang web (HTML, JSON). Phân cách với Header bằng một dòng trống (`\r\n\r\n`).
*   **Cấu trúc URL:** `scheme://domain:port/path?parameter#anchor`
*   **Email Protocols:** 
    *   **SMTP:** Gửi mail đi (Port 25/587).
    *   **IMAP:** Nhận mail và đồng bộ với Server (Port 143/993).
    *   **POP3:** Nhận mail bằng cách tải về máy tính và xóa trên Server (Port 110/995).
*   **DNS:** Hệ thống phân giải tên miền (VD: `google.com`) thành địa chỉ IP (`142.250.191.46`).

---

## 2. LECTURE 2: SOCKET PROGRAMMING (Lập trình Mạng)
*   **Socket là gì?** Được ví như "cánh cửa" giao tiếp giữa Ứng dụng (Application) và Mạng (Transport Layer).
*   **Địa chỉ Socket:** Gồm `IP Address` (Định danh máy tính) + `Port Number` (Định danh tiến trình/phần mềm chạy trên máy đó).
*   **TCP (Transmission Control Protocol):** Kết nối an toàn, đảm bảo dữ liệu tới nơi và đúng thứ tự (byte-stream). Chậm hơn nhưng đáng tin cậy. Dùng cho Web, Email.
    *   *Quy trình Server TCP:* `socket()` -> `bind()` -> `listen()` -> `accept()` -> `recv()/send()` -> `close()`
    *   *Quy trình Client TCP:* `socket()` -> `connect()` -> `send()/recv()` -> `close()`
*   **UDP (User Datagram Protocol):** Phi kết nối, gửi dữ liệu đi nhanh nhưng không đảm bảo tới nơi hoặc đúng thứ tự. Dùng cho Video Streaming, Game Online.
    *   *Quy trình:* Dùng `sendto()` và `recvfrom()` (không cần `connect()` hay `accept()`).

---

## 3. LECTURE 3 & ASYNC PDF: ADVANCED SOCKET (Mở rộng ứng dụng)
Khi ứng dụng có nhiều người dùng (Scale), ta phải chọn giải pháp xử lý đồng thời (Concurrency).
*   **Global Interpreter Lock (GIL) trong Python:** Khóa chặn không cho phép nhiều Thread chạy mã Python cùng một lúc, gây thắt cổ chai.
*   **Multi-threading (Đa luồng):**
    *   Nhiều luồng chia sẻ chung 1 bộ nhớ. Phải dùng `Lock()` (Mutex) để tránh xung đột dữ liệu.
    *   *Nhược điểm:* Tốn RAM, chi phí chuyển đổi cao (Context Switching), bị ảnh hưởng nặng bởi GIL. Chỉ tốt cho tác vụ I/O nhẹ.
*   **Multi-processing (Đa tiến trình):**
    *   Tạo ra nhiều tiến trình độc lập, không chia sẻ bộ nhớ, không bị dính GIL, tận dụng 100% CPU.
    *   *Nhược điểm:* Tốn RẤT NHIỀU RAM. Chỉ nên dùng cho tác vụ nặng CPU (Tính toán AI, nén Video).
*   **Asyncio (Bất đồng bộ) - Giải pháp tối ưu nhất:**
    *   Chạy duy nhất trên 1 Thread (không tốn RAM tạo Thread mới). Dùng cơ chế **Event Loop** để tự động chuyển việc khác khi gặp độ trễ I/O (chờ mạng).
    *   *Từ khóa:* `async def`, `await`. Thích hợp nhất làm Chat Server, Web Server.

---

## 4. LECTURE 4: SECURING SOCKET LAYER (Bảo mật mạng)
*   **Tính toàn vẹn dữ liệu (Data Integrity - Hashing):** 
    *   Dùng hàm băm (MD5, SHA-256) biến dữ liệu thành một chuỗi ký tự cố định. Băm 1 chiều không thể dịch ngược.
    *   *Mục đích:* Dùng để kiểm tra xem file gửi đi có bị kẻ gian sửa đổi ở giữa đường hay không.
*   **Mật mã đối xứng (Symmetric - AES):**
    *   Hai bên dùng CHUNG 1 khóa bí mật để vừa mã hóa vừa giải mã.
    *   Tốc độ cực nhanh, nhưng rủi ro cao nếu chìa khóa bị lộ khi gửi qua mạng.
*   **Mật mã bất đối xứng (Asymmetric - RSA):**
    *   Dùng 2 khóa: `Public Key` (Khóa công khai - Gửi cho tất cả mọi người) và `Private Key` (Khóa bí mật - Giữ cho riêng mình).
    *   Ai cũng có thể dùng `Public Key` để mã hóa, nhưng chỉ ai cầm `Private Key` mới giải mã được.
*   **Cơ chế lai (Hybrid Cryptography):** Sự kết hợp hoàn hảo.
    *   Dùng RSA (Bất đối xứng) để gửi cái "chìa khóa AES" một cách an toàn qua mạng.
    *   Sau đó dùng khóa AES (Đối xứng) đó để mã hóa toàn bộ dữ liệu vì AES chạy nhanh hơn rất nhiều.

---

## 5. WEEK 8: AWK & BASH SCRIPT (Xử lý chuỗi)
*   AWK là ngôn ngữ xử lý văn bản mạnh mẽ trên Linux. Cấu trúc chuẩn: `awk 'BEGIN{...} {thực thi từng dòng} END{...}' file.txt`
*   `$1, $2, $3`: Lấy giá trị của cột số 1, 2, 3 trong một dòng.
*   `grep`: Lệnh tìm kiếm chuỗi trong file (thường kết hợp với tham số `-c` để đếm số dòng).
