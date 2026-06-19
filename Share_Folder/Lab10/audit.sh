#!/bin/bash

LOG_FILE="server.log"
echo "==AUDIT=="

if [ ! -f "$LOG_FILE" ]; then
    echo "server.log does not exist."
    exit 1
fi

echo "1. server.log exists"

awk '
BEGIN { total=0; success=0; fail=0 }
{
    total++
    result = $NF
    user = $(NF-1)

    if (result == "LOGIN_SUCCESS") {
        success++
    } else if (result == "LOGIN_FAIL") {
        fail++
        failed_attempts[user]++
    }
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