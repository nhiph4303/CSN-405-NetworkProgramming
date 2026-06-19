#!/bin/bash
LOG_FILE="connections.log"

if [ ! -f "$LOG_FILE" ]; then
    exit 0
fi

awk '
BEGIN {
    total_today = 0
    active_now = 0
    print "=== Server Monitor ==="
}
{
    # Lưu lại toàn bộ các dòng để lát ở END in ra 5 dòng cuối
    lines[NR] = $0
    
    # Cột $3 là chữ CONNECT hoặc DISCONNECT
    if ($3 == "CONNECT") {
        total_today++
        active_now++
        
        # Cột $4 là IP:Port. Dùng hàm split để tách lấy IP
        split($4, arr, ":")
        ip = arr[1]
        ip_count[ip]++
    } else if ($3 == "DISCONNECT") {
        active_now--
    }
}
END {
    # 1 & 2. In tổng kết nối và kết nối đang Active
    printf "Total Today: %d | Active Now: %d\n\n", total_today, active_now
    
    # 3. Thuật toán tìm Top 3 IPs
    for (i = 1; i <= 3; i++) {
        max_val = -1
        max_ip = ""
        # Duyệt tìm thằng lớn nhất
        for (ip in ip_count) {
            if (ip_count[ip] > max_val) {
                max_val = ip_count[ip]
                max_ip = ip
            }
        }
        # Lưu thằng lớn nhất vào mảng top_ips
        if (max_ip != "") {
            top_ips[i] = max_ip
            top_vals[i] = max_val
            ip_count[max_ip] = -2 # Đánh dấu đã lấy để vòng lặp sau không chọn lại
        }
    }
    
    # In ra Top 3
    printf "Top IPs: "
    for (i = 1; i <= 3; i++) {
        if (top_ips[i] != "") {
            printf "%s(%d)", top_ips[i], top_vals[i]
            # Thêm dấu phẩy nếu không phải là phần tử cuối
            if (i < 3 && top_ips[i+1] != "") printf ", "
        }
    }
    print "\n\nLast 5 events:"
    
    # 4. In 5 sự kiện gần nhất (Lấy từ mảng lines đã lưu)
    start = NR - 4
    if (start < 1) start = 1
    for (i = start; i <= NR; i++) {
        print lines[i]
    }
    print "----------------------"
}
' "$LOG_FILE"
