#!/bin/bash

# ==========================================
# [SƯỜN BẮT BUỘC: TÊN FILE LOG VÀ KIỂM TRA]
# ==========================================
LOG_FILE="server.log"
echo "==AUDIT=="

if [ ! -f "$LOG_FILE" ]; then
    echo "server.log does not exist."
    exit 1
fi

echo "1. server.log exists"

# ==========================================
# [LOGIC ĐỀ BÀI: XỬ LÝ LOG BẰNG AWK]
# ==========================================
# Giải thích ý nghĩa của các lệnh AWK:
# BEGIN { ... } -> Khởi tạo biến đếm
# { ... } -> Block chạy lặp qua từng dòng của file log
# END { ... } -> In ra kết quả sau khi duyệt xong

awk '
BEGIN { total=0; success=0; fail=0 }
{
    total++
    # Cấu trúc log: [YYYY-MM-DD HH:MM:SS] port username result
    # $NF là cột cuối cùng (result: LOGIN_SUCCESS/LOGIN_FAIL)
    result = $NF
    # $(NF-1) là cột áp chót (username)
    user = $(NF-1)

    if (result == "LOGIN_SUCCESS") {
        success++
    } else if (result == "LOGIN_FAIL") {
        fail++
        # Lưu lại số lần fail của từng user
        failed_attempts[user]++
    }
    # Mảng lưu username để đếm số user duy nhất
    unique_users[user] = 1
}
END {
    print "2. Total login requests: " total
    print "3. Number of successful logins: " success
    print "4. Number of failed logins: " fail

    print "5. Unique usernames: "
    for (u in unique_users) {
        print "   - " u
    }

    print "6. Usernames with >= 3 failed attempts: "
    for (u in failed_attempts) {
        if (failed_attempts[u] >= 3) {
            print "   - " u
        }
    }
}' "$LOG_FILE"