#!/bin/bash

LOG_FILE="q2_server.log"
echo "==Q2 AUDIT=="

if [ ! -f "$LOG_FILE" ]; then
    echo "1. q2_server.log does not exist."
    exit 1
fi

echo "1. q2_server.log exists"

awk '
BEGIN { total=0; strong=0; weak=0; total_len=0; max_len=0; longest="" }
{
    total++
    result = $NF
    password = $(NF-1)
    len = length(password)
    
    total_len += len
    if (len > max_len) {
        max_len = len
        longest = password
    }
    
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
        printf "6. Average password length: %.2f\n", total_len / total
    } else {
        print "6. Average password length: 0"
    }
}' "$LOG_FILE"
