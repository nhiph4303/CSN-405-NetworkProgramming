#!/bin/bash
# Nhận tên file từ tham số đầu tiên
file=$1

# Dùng grep -c để đếm số dòng chứa từng từ khóa
info_count=$(grep -c "INFO" "$file")
error_count=$(grep -c "ERROR" "$file")
warning_count=$(grep -c "WARNING" "$file")

# In ra màn hình theo đúng định dạng đề yêu cầu
echo "INFO: $info_count"
echo "ERROR: $error_count"
echo "WARNING: $warning_count"
