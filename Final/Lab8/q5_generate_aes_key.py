import os

# ==========================================
# [SƯỜN BẮT BUỘC: TẠO KHÓA AES]
# ==========================================
def generate_aes_key():
    # Yêu cầu 1: Generate AES Key (Tạo khóa ngẫu nhiên 32 bytes = 256 bits)
    key = os.urandom(32)
    
    # ==========================================
    # [LOGIC ĐỀ BÀI: LƯU FILE KHÓA AES]
    # ==========================================
    with open("aes.key", "wb") as f:
        f.write(key)
        
    print("AES key (256-bit) generated successfully and saved to 'aes.key'")

if __name__ == "__main__":
    generate_aes_key()
