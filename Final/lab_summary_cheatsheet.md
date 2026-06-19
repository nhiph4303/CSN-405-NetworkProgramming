# 🗺️ BẢN ĐỒ KHO BÁU: TỔNG HỢP CÁC DẠNG BÀI LAB (5 - 10) & ĐỀ THI

> [!TIP]
> Đi thi được dùng tài liệu, nên thay vì học thuộc lòng code, bạn chỉ cần nhớ **Dạng bài này lấy từ file nào** để mở ra copy/paste sườn cho nhanh. Dưới đây là bảng tổng hợp CHI TIẾT NHẤT!

---

## 🛠️ DẠNG 1: Linux Command Line & AWK (Lab 6 & Lab 9)
Đặc điểm: Đề bài yêu cầu dùng lệnh Linux (Terminal) để tìm kiếm, lọc dữ liệu từ file văn bản. Không viết Python.

* **Lab 6 (Linux Commands & Shell Scripts):** 
  * **Nội dung:** Lệnh `grep`, `sed`, `awk` cơ bản. Viết các file `.sh` nhỏ để đếm số dòng, lọc IP, thay thế chữ.
  * **Tài liệu nên mở:** `Lab6/Lab6_All_Commands.md` hoặc các file `question.sh`.
* **Lab 9 (AWK Nâng Cao):**
  * **Nội dung:** Lập trình mảng, vòng lặp, tính tổng và trung bình bằng lệnh `awk 'BEGIN{} {} END{}'`.
  * **Tài liệu nên mở:** `Exam_Cheatsheet/Lab9_AWK_Cheatsheet.md`.

---

## 🔒 DẠNG 2: Mật Mã Học - RSA & AES (Lab 8)
Đặc điểm: Đề bài nhắc đến `Encryption`, `Decryption`, `Digital Signature`, `Public/Private Key`, hoặc thư viện `cryptography`.

* **Tạo Khóa (Generate Keys):** 
  * **Chức năng:** Code tự động sinh ra file `public.pem` và `private.pem` (RSA) hoặc `aes.key` (AES).
  * **File mẫu:** `Lab8/q1_generate_key.py` (RSA) và `Lab8/q5_generate_aes_key.py` (AES).
* **Mã hóa Bất Đối Xứng (RSA Encryption & Signature):**
  * **Chức năng:** Client mã hóa tin nhắn bằng Public Key. Ký tên (Sign) bằng Private Key. Server giải mã và xác thực (Verify).
  * **File mẫu:** `Lab8/q4_client.py` và `Lab8/q4_server.py`.
* **Mã hóa Đối Xứng (AES Encryption):**
  * **Chức năng:** Client và Server dùng chung 1 khóa `aes.key` để mã hóa tốc độ cao.
  * **File mẫu:** `Lab8/q5_client.py` và `Lab8/q5_server.py`.
  * **Lấy sườn:** Code `Fernet(key)` siêu dễ nhớ.
* **Mã hóa Lai Tự Động (Hybrid Cryptography - Cực Khó):**
  * **Chức năng:** Server tự sinh khóa RSA lúc bật lên, gửi Public cho Client. Client tự sinh khóa AES và mã hóa bằng Public Key gửi lại.
  * **File mẫu đỉnh nhất:** `Exam/24-25-Q4/q3_client.py` và `Exam/24-25-Q4/q3_server.py`.

---

## ⚡ DẠNG 3: Asyncio (Server Bất Đồng Bộ tính toán)
Đặc điểm: Đề bài yêu cầu dùng `asyncio`, bắt buộc viết hàm có chữ `async def` và `await`.

* **Lab 5 - Câu 1 & 3 (Echo Server / Tính toán cơ bản):**
  * **Chức năng:** Gửi gì dội lại nấy, tính tổng. Dùng để lấy cái sườn gốc đơn giản nhất.
  * **File mẫu:** `Lab5/q1_server.py`
* **Lab 5 - Câu 2 (Math Menu):**
  * **Chức năng:** Bài có Menu (PRIME, NEXT_PRIME, FACT). Phân nhánh tính toán.
  * **File mẫu:** `Lab5/q2_server.py` (Sườn `if-elif-else`).
* **Đề thi 25-26 Q2 (Fibonacci):**
  * **Chức năng:** Tính Fibonacci qua mạng.
  * **File mẫu:** `Exam/25-26-Q2/q2_server.py`.

---

## 💬 DẠNG 4: Chat Room (Server Nhắn tin nhiều người)
Đặc điểm: Đề bài nói "Chat server", "Real-time communication", "Broadcast". Khi 1 người nhắn thì tất cả người khác phải thấy. (Dạng mở rộng rất hay ra thi).

* **Đề thi 25-26 Q1:**
  * **Chức năng:** Có biến `clients = set()` lưu mọi người. Khối vòng lặp `for c in clients` để gửi tin nhắn đi.
  * **File mẫu:** `Exam/25-26-Q1/q2_server.py` (SƯỜN GỐC TỐT NHẤT CHO BÀI CHAT).
  * **File Client Chat Realtime:** `Exam/25-26-Q1/q2_client.py` (Dùng `asyncio.to_thread(input)`).

---

## 📊 DẠNG 5: Nhúng Bash/AWK vào Python Server (Lab 10 & Đề Thi)
Đặc điểm: Đề bài bảo viết file `.sh` (audit.sh, monitor.sh) đọc file `.log` để đếm tổng số, tìm Top IP. Sau đó chạy tự động bằng Python.

* **Viết Script AWK (Tìm Top, Tính Trung Bình):**
  * **Nội dung:** File script Bash bọc lệnh AWK để in ra báo cáo thống kê.
  * **File mẫu học thuật:** `Lab10/q2_audit.sh` (Đếm mật khẩu mạnh/yếu).
  * **File mẫu thi cử (Khó hơn):** `Exam/25-26-Q1/monitor.sh` (Đếm IP, mảng trượt), `Exam/24-25-Q2/count_logs.sh` (grep đếm dòng) và `Exam/24-25-Q2/extract_errors.awk`.
* **Nhúng vào Python:**
  * **Chức năng:** Python tự động gọi file Shell lên in báo cáo khi Client Disconnect.
  * **File mẫu:** `Exam/25-26-Q1/q3_server.py` hoặc `Exam/25-26-Q2/q3_server.py`.
  * **Lấy sườn:** Copy nguyên hàm `async def run_monitor():` dùng lệnh `asyncio.create_subprocess_exec`.

---

## 🖥️ DẠNG 6: Lập Trình Giao Diện (Tkinter GUI)
Đặc điểm: Đề bài xuất hiện hình chụp một cái cửa sổ phần mềm máy tính (Có Nút bấm, Ô nhập chữ).

* **Giao diện Client tích hợp Socket & Mã hóa:**
  * **Chức năng:** Vẽ khung, bắt sự kiện click nút. Đọc nội dung Textbox, mã hóa (nếu có), gửi qua mạng và nhận Popup trả về.
  * **File mẫu (Chuẩn mực thi cử):** `Exam/24-25-Q2/q2_client.py` (Có nút Select File, Integrity Check).
  * **Mẹo:** Đi thi nếu có vẽ giao diện, hãy mở file này copy nguyên hàm `root = tk.Tk()`, đổi tên biến và gắn lệnh kết nối Server vào bên trong hàm của Button là ăn điểm!

---
> [!IMPORTANT]
> **Quy trình "Sống sót" trong phòng thi:** 
> 1. Đọc lướt yêu cầu bài thi và so sánh với **Đặc điểm** của 5 Dạng trên.
> 2. Mở File mẫu tương ứng được gợi ý.
> 3. Save as (Copy) sang thư mục nộp bài.
> 4. Chỉ cần tập trung sửa Logic cốt lõi (Port, tên File, các phép toán cộng trừ nhân chia). TUYỆT ĐỐI KHÔNG GÕ LẠI TỪ ĐẦU!
