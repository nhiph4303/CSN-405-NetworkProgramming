# LAB 7 – Security (Bảo mật với OpenSSL)
**Sinh viên:** Phan Ngọc Hạnh Nhi
**MSSV:** 2131209002

*File này tổng hợp toàn bộ các câu lệnh thực hành `openssl` từ cơ bản đến nâng cao dùng trong Lab 7. Đi thi bạn chỉ việc copy paste và sửa tên file là xong!*

---

## Question 1: AES File Encryption with OpenSSL (Mã hóa đối xứng AES)

**1. Tạo file dữ liệu:**
```bash
echo "This is a confidential message for CSN405." > message.txt
```

**2. Mã hóa file message.txt bằng thuật toán AES-256-CBC:**
*(Lệnh sẽ yêu cầu bạn nhập mật khẩu 2 lần)*
```bash
openssl enc -aes-256-cbc -in message.txt -out message.enc -pbkdf2
```

**3. Giải mã file message.enc về lại dạng text:**
*(Cần nhập đúng mật khẩu đã thiết lập ở bước trên)*
```bash
openssl enc -aes-256-cbc -d -in message.enc -out message_decrypted.txt -pbkdf2
```

**4. So sánh 2 file (Nếu không hiện ra gì tức là giống nhau 100%):**
```bash
diff message.txt message_decrypted.txt
```

**5. Giải thích lý do file mã hóa không thể đọc trực tiếp (Điểm lý thuyết):**
> - **Chuyển hóa thành Ciphertext:** Thuật toán AES đã biến đổi các chữ cái thành chuỗi nhị phân ngẫu nhiên bằng toán học dựa trên mật khẩu bí mật.
> - **Lỗi định dạng:** Các Text Editor (như Notepad, cat) cố gắng đọc nó theo chuẩn ASCII/UTF-8 nên chỉ thấy các ký tự rác.
> - **Thiếu khóa giải mã:** Nếu không có Key (mật khẩu) để đảo ngược quá trình, việc đọc hiểu dữ liệu gốc là bất khả thi.

---

## Question 2: RSA Key Pair Generation (Tạo cặp khóa Bất đối xứng RSA)

**1. Tạo khóa bí mật (Private Key) - Độ dài 2048 bit:**
```bash
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
```

**2. Trích xuất khóa công khai (Public Key) từ Private Key:**
```bash
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

**3. Hiển thị nội dung 2 file khóa:**
```bash
cat private_key.pem
cat public_key.pem
```

**4. Giải thích về cặp khóa (Điểm lý thuyết):**
> - **Khóa nào phải được giữ bí mật?** `private_key.pem`. Khóa này dùng để giải mã và ký xác thực. Nếu lộ khóa này, hacker có thể đọc trộm tin nhắn hoặc mạo danh bạn để ký kết.
> - **Khóa nào có thể chia sẻ công khai?** `public_key.pem`. Khóa này được chia sẻ cho người khác để họ mã hóa tin nhắn gửi cho bạn (chỉ bạn có private key mới mở được), hoặc dùng để kiểm tra chữ ký của bạn.

---

## Question 3: RSA Encrypt and Decrypt a Small Message (Mã hóa tin nhắn ngắn bằng RSA)

**1. Tạo file bí mật nhỏ:**
```bash
echo "AES key: 1234567890abcdef" > small_secret.txt
```

**2. Mã hóa bằng RSA Public Key (Khóa Công Khai):**
```bash
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in small_secret.txt -out small_secret.enc
```

**3. Giải mã bằng RSA Private Key (Khóa Bí Mật):**
```bash
openssl pkeyutl -decrypt -inkey private_key.pem -in small_secret.enc -out small_secret_decrypted.txt
```

**4. So sánh:**
```bash
diff small_secret.txt small_secret_decrypted.txt
```

**5. Tại sao RSA chỉ dùng để mã hóa dữ liệu ngắn? (Điểm lý thuyết):**
> - **Giới hạn kích thước:** RSA 2048-bit chỉ mã hóa được tối đa 245 bytes. File lớn hơn sẽ báo lỗi.
> - **Tốc độ cực chậm:** Toán học của RSA phức tạp và chậm hơn AES gấp hàng nghìn lần. Mã hóa file lớn bằng RSA sẽ gây treo CPU.

---

## Question 4: Hybrid Encryption with AES and RSA (Mã hóa Kết hợp)
*Ngữ cảnh: RSA thì chậm và giới hạn độ dài, AES thì nhanh nhưng khó trao đổi mật khẩu an toàn. Vậy nên ta dùng AES để mã hóa File lớn, sau đó dùng RSA để mã hóa cái mật khẩu AES.*

**1. Tạo file điểm số của sinh viên (Sửa tên theo tên bạn):**
```bash
echo "Student score data: Phan_Ngoc_Hanh_Nhi=9.0" > score.txt
```

**2. Tạo một mật khẩu ngẫu nhiên cho AES (AES Key):**
```bash
openssl rand -hex 32 > aes_key.txt
```

**3. Dùng mật khẩu AES đó để mã hóa file điểm (AES Encryption):**
```bash
openssl enc -aes-256-cbc -in score.txt -out score.enc -pass file:aes_key.txt -pbkdf2
```

**4. Dùng RSA Public Key để mã hóa cái mật khẩu AES (Gửi an toàn cho Server):**
```bash
openssl pkeyutl -encrypt -pubin -inkey public_key.pem -in aes_key.txt -out aes_key.enc
```

**5. Ở phía Server: Server dùng RSA Private Key để giải mã lấy lại mật khẩu AES:**
```bash
openssl pkeyutl -decrypt -inkey private_key.pem -in aes_key.enc -out recovered_aes_key.txt
```

**6. Server dùng mật khẩu AES vừa lấy lại được để giải mã file điểm:**
```bash
openssl enc -aes-256-cbc -d -in score.enc -out score_decrypted.txt -pass file:recovered_aes_key.txt -pbkdf2
```

**7. Kiểm tra:**
```bash
diff score.txt score_decrypted.txt
```

---

## Question 5: Digital Signature with RSA (Chữ ký điện tử / Chống chối bỏ)
*Dùng Private Key để "Ký" xác nhận file này do chính mình làm ra, và đảm bảo file chưa bị chỉnh sửa trên đường truyền.*

**1. Tạo file báo cáo:**
```bash
echo "Final project report submitted by student A." > report.txt
```

**2. Ký xác thực file bằng Private Key (Băm SHA256 rồi Ký):**
```bash
openssl dgst -sha256 -sign private_key.pem -out report.sig report.txt
```

**3. Ở phía Server: Xác minh chữ ký bằng Public Key của sinh viên:**
```bash
openssl dgst -sha256 -verify public_key.pem -signature report.sig report.txt
# Kết quả mong đợi: Verified OK
```

**4. Thử giả mạo: Sửa file báo cáo từ Student A thành Student B:**
```bash
sed -i 's/student A/student B/' report.txt
```

**5. Xác minh lại file đã bị chỉnh sửa:**
```bash
openssl dgst -sha256 -verify public_key.pem -signature report.sig report.txt
# Kết quả mong đợi: Verification Failure
```

**6. Giải thích vì sao việc xác minh thất bại sau khi chỉnh sửa? (Điểm lý thuyết):**
> - **Sai lệch mã Hash:** Chữ ký số gắn chặt với mã băm (Hash SHA-256) của file gốc. Đổi dù chỉ 1 ký tự (từ A sang B) cũng làm toàn bộ mã Hash thay đổi hoàn toàn.
> - **Phát hiện gian lận (Tamper Detection):** OpenSSL dùng Public Key để giải mã chữ ký (lấy lại mã Hash gốc), sau đó băm thử lại file hiện tại. Nếu 2 mã Hash lệch nhau -> Chắc chắn file đã bị sửa đổi trái phép -> Báo lỗi `Verification Failure`.
