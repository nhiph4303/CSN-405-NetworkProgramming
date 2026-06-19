#!/bin/bash

# ==========================================
# [SƯỜN BẮT BUỘC: TÊN FILE LOG VÀ KIỂM TRA]
# ==========================================
LOG_FILE="q2_server.log"
echo "==Q2 AUDIT=="

if [ ! -f "$LOG_FILE" ]; then
    echo "1. q2_server.log does not exist."
    exit 1
fi

echo "1. q2_server.log exists"

# ==========================================
# [LOGIC ĐỀ BÀI: XỬ LÝ LOG BẰNG AWK ĐẾM ĐỘ MẠNH MẬT KHẨU]
# ==========================================
awk '
BEGIN { total=0; strong=0; weak=0; total_len=0; max_len=0; longest="" }
{
    total++
    # Cấu trúc log: [YYYY-MM-DD HH:MM:SS] port password result
    result = $NF
    password = $(NF-1)
    len = length(password)
    
    # Yêu cầu 6. Average password length: Tính tổng độ dài
    total_len += len
    
    # Yêu cầu 5. Longest password received: Lưu mật khẩu dài nhất
    if (len > max_len) {
        max_len = len
        longest = password
    }
    
    # Yêu cầu 3 & 4. Đếm số lượng STRONG/WEAK
    if (result == "STRONG") {
        strong++
    } else if (result == "WEAK") {
        weak++
    }
}
END {
    print "2. Total password checks: " total
    print "3. Number of STRONG passwords: " strong
    print "4. Number of WEAK passwords: " weak
    print "5. Longest password received: " longest " (length " max_len ")"
    if (total > 0) {
        # Tính trung bình cộng độ dài mật khẩu (%.2f để in ra 2 chữ số thập phân)
        printf "6. Average password length: %.2f\n", total_len / total
    } else {
        print "6. Average password length: 0"
    }
}' "$LOG_FILE"
