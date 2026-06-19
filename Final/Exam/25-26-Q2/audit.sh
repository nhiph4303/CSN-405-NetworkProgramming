#!/bin/bash

# Đổi lại đúng tên file log mà q3_server.py đang ghi ra
LOG_FILE="server.log"
echo "== AUDIT RESULTS =="

# Kiểm tra xem file log đã tồn tại chưa
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file does not exist yet."
    exit 1
fi

awk '
BEGIN { 
    total_req = 0; 
    sum_index = 0; 
}
{
    # Mỗi dòng đọc được, tăng biến đếm tổng request lên 1
    total_req++
    
    # Cột $4 là REQUESTED_INDEX (số Fibonacci client nhập)
    # Cộng dồn cột $4 vào biến sum_index để tính trung bình
    sum_index += $4
    
    # Cột $3 là IP_ADDRESS
    # Mảng ips lưu lại số lần xuất hiện của từng IP
    ips[$3]++
}
END {
    # 1. In tổng số requests
    print "1. Total requests today: " total_req
    
    # 2. In trung bình Index
    if (total_req > 0) {
        printf "2. Average Fibonacci index: %.2f\n", (sum_index / total_req)
    } else {
        print "2. Average Fibonacci index: 0"
    }
    
    # 3. In danh sách IP duy nhất (Dùng vòng lặp for-in)
    print "3. Unique IP addresses:"
    for (ip in ips) {
        print "   - " ip
    }
    
    # 4. Tìm các IP có số lần request > 5
    print "4. IPs with more than 5 requests:"
    count_ip_over_5 = 0
    for (ip in ips) {
        if (ips[ip] > 5) {
            print "   - " ip " (made " ips[ip] " requests)"
            count_ip_over_5++
        }
    }
    # Nếu không có ai lặp lại > 5 lần thì in ra chữ None
    if (count_ip_over_5 == 0) {
        print "   - None"
    }
}' "$LOG_FILE"
