# 📚 TỔNG ÔN TẬP THI CUỐI KỲ: NETWORK PROGRAMMING

Đây là tài liệu được tổng hợp bám sát 100% "hint" đề thi mà thầy giáo của bạn vừa tiết lộ. Bao gồm 1 câu Lý thuyết và 2 câu Thực hành.

---

## PHẦN 1: TỔNG QUAN CẤU TRÚC ĐỀ THI (3 CÂU CHUẨN XÁC)

Theo tiết lộ mới nhất của giảng viên, đề thi sẽ có định dạng chính xác 3 câu:

- **Câu 1 (Lý thuyết):** Tập trung vào các khái niệm Scale ứng dụng, Xử lý tiến trình/luồng, Bảo mật (Security - Mật mã học), và lệnh AWK. _(Xem đáp án học thuộc ở Phần 2)._
- **Câu 2 (Thực hành - Bất đồng bộ Async):** Yêu cầu viết một ứng dụng Server-Client đơn giản bằng thư viện `asyncio`. _(Vào phòng thi, hãy mở **DẠNG 3** hoặc **DẠNG 4** trong Bản Đồ Kho Báu ra để copy sườn Server)._
- **Câu 3 (Thực hành - Tự động hóa Audit / Lab 10):** Đỉnh cao của bài thi! Bắt buộc phải mở **DẠNG 5** trong Bản Đồ Kho Báu để copy hàm `run_audit()`. Nhiệm vụ là làm cho Server nhận file xong tự động móc nối với lệnh gọi file `.sh` hoặc `.awk` ẩn dưới nền để phân tích dữ liệu.

---

## PHẦN 2: TRẢ LỜI CÁC CÂU HỎI LÝ THUYẾT TRỌNG TÂM

### 1. Scale 1 ứng dụng: Chọn giải pháp nào? (Thread vs Process vs Asyncio)

- **Scale (Mở rộng) ứng dụng** là việc tăng khả năng chịu tải của Server để phục vụ nhiều Client cùng lúc.
- **Đa luồng (Multi-threading):** Dùng cho các tác vụ I/O-bound (đợi mạng, đọc file) nhẹ nhàng. Nhưng tốn RAM và chi phí Context Switching, dễ bị kẹt do GIL trong Python.
- **Đa tiến trình (Multi-processing):** Dùng cho tác vụ CPU-bound cực nặng (xử lý video, tính toán AI). Mỗi tiến trình độc lập hoàn toàn, tận dụng đa nhân CPU nhưng tốn rất nhiều RAM.
- **Bất đồng bộ (Asyncio):** Dùng 1 luồng duy nhất, dùng Event Loop để quản lý. **Đây là giải pháp tốt nhất (NÊN CHỌN) cho Network Server (Chat, Web)** vì siêu tiết kiệm RAM, xử lý hàng chục ngàn kết nối I/O cùng lúc mượt mà.
- **Xử lý Lock:** Khi dùng Thread, nếu 2 Thread cùng sửa 1 biến `count` sẽ gây lỗi. Phải dùng `Lock()` (Mutex) để khóa biến đó lại, 1 Thread sửa xong mới cho Thread kia vào.

### 2. Giao thức HTTP và Cấu trúc Gói tin

- **HTTP là gì?** Là giao thức Truyền tải Siêu văn bản (HyperText Transfer Protocol) chạy trên nền TCP, dùng để giao tiếp giữa Web Browser và Web Server.
- **Header trong gói tin là gì? Chứa gì?** Header là "phong bì thư". Nó chứa các thông tin meta điều khiển như: Loại dữ liệu (Content-Type), Chiều dài (Content-Length), User-Agent (trình duyệt gì), Cookie, và Mã trạng thái (200 OK, 404 Not Found).
- **Header và Data/Body:** Header là phần khai báo, Body là phần ruột (Nội dung thực sự, ví dụ như mã HTML, dữ liệu JSON). Phân cách bằng 1 dòng trống `\r\n\r\n`.

### 3. URL là gì? Gồm những thành phần nào?

- **Viết tắt của:** **U**niform **R**esource **L**ocator (Định vị tài nguyên thống nhất).
- **Các thành phần:** `scheme://domain:port/path?parameter#anchor`
  - `scheme`: Giao thức (http, https, ftp).
  - `domain name`: Tên miền (google.com).
  - `port`: Cổng (80, 443).
  - `path`: Đường dẫn tới file/thư mục.
  - `parameter` (Query String): Tham số truy vấn (biến=giá trị).
  - `anchor` (Fragment): Dấu `#`, neo cuộn trang đến vị trí cụ thể.

### 4. Giao thức Email

- **Gửi Email:** Dùng giao thức **SMTP** (Cổng 25 hoặc 587).
- **Nhận Email:** Dùng giao thức **IMAP** (Cổng 143/993 - đồng bộ máy chủ) hoặc **POP3** (Cổng 110/995 - tải hẳn về máy xóa trên server).

### 5. Mật mã & Tính toàn vẹn (Hash, AES, RSA)

- **Tại sao cần Hash data?** Để đảm bảo dữ liệu không bị ai lén lút sửa đổi trên đường truyền. Đặc tính của Hash là: Dữ liệu giống nhau băm ra y chang nhau, chỉ cần đổi 1 dấu phẩy băm ra mã khác biệt hoàn toàn, và KHÔNG thể giải mã ngược.
- **Làm sao băm giúp kiểm tra toàn vẹn?** Client gửi file đính kèm kèm mã Hash gốc. Server nhận file, tự băm file ra mã Hash mới. Nếu `Hash gốc == Hash mới` -> File toàn vẹn (MATCH). _(Chính là câu bài tập Integrity Check)_
- **Mật mã đối xứng (AES):** Cả 2 bên xài chung 1 chìa khóa để khóa và mở. Nhanh nhưng dễ lộ khóa.
- **Trao đổi khóa (RSA):** Dùng cặp khóa Public/Private. Server đưa Public Key cho Client. Client dùng nó khóa cái "Chìa khóa AES" lại rồi gửi cho Server. Server dùng Private Key để mở, thế là 2 bên có chung khóa AES an toàn tuyệt đối.

### 6. Làm sao server lưu trữ thông tin từ Client?

- **Tạm thời (Trong RAM):** Lưu vào biến (như `clients = set()` trong bài Chat), hoặc Session. Khi tắt server sẽ mất.
- **Vĩnh viễn (Trên đĩa cứng):** Ghi vào File Text/Log (như ghi vào `server_log.txt`), hoặc lưu vào Cơ sở dữ liệu (Database như SQLite, MySQL).

---

## PHẦN 3: THỰC HÀNH CẤP TỐC (CÂU URL PARSER)

Đây là đoạn code **Tuyệt đối không dùng thư viện** để bóc tách URL đúng như thầy dặn. Bạn hãy học thuộc logic cắt chuỗi `.split()` này!

```python
def parse_url(url):
    # Khởi tạo kết quả rỗng
    result = {"scheme": "", "domain name": "", "port": "", "parameter": "", "anchor": ""}

    # 1. Tìm Anchor (#) từ dưới lên
    if "#" in url:
        url, result["anchor"] = url.split("#", 1)

    # 2. Tìm Parameter (?) từ dưới lên
    if "?" in url:
        url, result["parameter"] = url.split("?", 1)

    # 3. Tìm Scheme (://) từ đầu chuỗi
    if "://" in url:
        result["scheme"], url = url.split("://", 1)

    # 4. Loại bỏ Path (/) để lấy được Domain gốc (Chỉ lấy phần trước dấu / đầu tiên)
    if "/" in url:
        url, path = url.split("/", 1)

    # 5. Tìm Port (:) nằm trong cụm Domain còn lại
    if ":" in url:
        result["domain name"], result["port"] = url.split(":", 1)
    else:
        result["domain name"] = url

    return result

# --- TEST THỬ ---
test_url = "https://www.abc.com:8080/folder/page.html?search=python#section1"
print(parse_url(test_url))

# Kết quả in ra:
# {'scheme': 'https', 'domain name': 'www.abc.com', 'port': '8080', 'parameter': 'search=python', 'anchor': 'section1'}
```
