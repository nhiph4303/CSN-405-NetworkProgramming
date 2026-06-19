#!/bin/bash

echo "=== MEMORY USAGE ==="
free -h
echo ""

echo "=== DISK SPACE USAGE ==="
df -h
echo ""

echo "=== TOP 5 PROCESSES BY CPU USAGE ==="
# ps command to get top processes.
# -e: all processes, -o: format, --sort=-%cpu: sort descending by cpu.
# Lấy 6 dòng đầu vì dòng đầu tiên là tiêu đề (header)
ps -eo pid,user,%cpu,%mem,comm --sort=-%cpu | head -n 6
