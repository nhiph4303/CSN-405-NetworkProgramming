import rsa

# ==========================================
# [SƯỜN BẮT BUỘC: TẠO CẶP KHÓA RSA]
# ==========================================
# Lệnh rsa.newkeys(2048) là bắt buộc để sinh ra cặp khóa theo chuẩn RSA 2048-bit.
public_key, private_key = rsa.newkeys(2048)

# ==========================================
# [LOGIC ĐỀ BÀI: LƯU FILE VÀ IN THÔNG BÁO]
# ==========================================
# Yêu cầu: Save the private and public keys in PEM format.
# - Mở file ở chế độ 'wb' (write binary) vì hàm save_pkcs1 trả về dữ liệu byte.
# - Hàm save_pkcs1("PEM") dùng để lưu khóa dưới định dạng chuẩn PEM.

# 1. Lưu Private Key
with open("client_private.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))

# 2. Lưu Public Key
with open("client_public.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

# Yêu cầu: print a message indicating successful key generation.
print("RSA key pair generated successfully")