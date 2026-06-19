# LAB 9 – AWK (Xử lý dữ liệu văn bản với AWK)
**Sinh viên:** Phan Ngọc Hạnh Nhi
**MSSV:** 2131209002

*Ghi chú: AWK là một ngôn ngữ lập trình chuyên dùng để xử lý dữ liệu theo dạng cột (Field). Mặc định AWK sẽ dùng khoảng trắng (Space/Tab) làm dấu phân cách cột. Cột 1 là `$1`, cột 2 là `$2`, toàn bộ dòng là `$0`.*

---

## Question 1: Student Performance Processing (`course_score.txt`)
*Mặc định file này cách nhau bằng khoảng trắng.*

**1. Print only student ID and student name.**
```bash
awk '{print $1, $2}' course_score.txt
```

**2. Print student name, group, and final score.**
```bash
awk '{print $2, $3, $6}' course_score.txt
```

**3. Print students whose final score is at least 8.0.**
```bash
awk '$6 >= 8.0 {print $0}' course_score.txt
```

**4. Print students whose quiz score is below 6.0 or final score is below 6.0.**
```bash
awk '$4 < 6.0 || $6 < 6.0 {print $0}' course_score.txt
```

**5. Print each student with a serial number added as the first output column.**
*(`NR` là biến có sẵn của awk, lưu số thứ tự của dòng hiện tại)*
```bash
awk '{print NR, $0}' course_score.txt
```

**6. Calculate each student’s total score using: quiz 20%, midterm 30%, final 50% then print name and total score with 2 decimal places.**
```bash
awk '{total = $4*0.2 + $5*0.3 + $6*0.5; printf "%s %.2f\n", $2, total}' course_score.txt
```

**7. Calculate the average final score of all students.**
```bash
awk '{sum += $6} END {print "Average final score:", sum/NR}' course_score.txt
```

**8. Find the student with the highest total score.**
```bash
awk '{total = $4*0.2 + $5*0.3 + $6*0.5; if(total > max) {max = total; name = $2}} END {print "Highest score student:", name, "with score:", max}' course_score.txt
```

**9. Count how many students belong to each group.**
```bash
awk '{count[$3]++} END {for(g in count) print "Group", g, ":", count[g]}' course_score.txt
```

**10. Print a formatted table with columns: ID, Name, Group, Quiz, Midterm, Final**
```bash
awk 'BEGIN {printf "%-10s %-10s %-10s %-10s %-10s %-10s\n", "ID", "Name", "Group", "Quiz", "Midterm", "Final"} {printf "%-10s %-10s %-10s %-10s %-10s %-10s\n", $1, $2, $3, $4, $5, $6}' course_score.txt
```

---

## Question 2: CSV Data Processing with Field Separator (`library_loans.csv`)
*File CSV phân cách nhau bằng dấu phẩy `,`. Phải dùng `-F','` để báo cho awk biết.*

**1. Print student_id, department, and fine_vnd. Skip the header row.**
*(`NR > 1` dùng để bỏ qua dòng tiêu đề)*
```bash
awk -F',' 'NR > 1 {print $2, $3, $6}' library_loans.csv
```

**2. Print only overdue records where days_late > 0.**
```bash
awk -F',' 'NR > 1 && $5 > 0 {print $0}' library_loans.csv
```

**3. Calculate the total fine collected and the average days_late for overdue records.**
```bash
awk -F',' 'NR > 1 && $5 > 0 {fine += $6; days += $5; count++} END {if(count > 0) print "Total fine:", fine, "| Average days late:", days/count}' library_loans.csv
```

**4. Count how many loan records each department has.**
```bash
awk -F',' 'NR > 1 {count[$3]++} END {for(d in count) print "Department", d, ":", count[d]}' library_loans.csv
```

**5. Find the student with the highest fine_vnd.**
```bash
awk -F',' 'NR > 1 {if($6 > max) {max = $6; student = $2}} END {print "Highest fine student:", student, "with", max, "VND"}' library_loans.csv
```

---

## Question 3: Authentication Event Audit (`auth_events.log`)

**1. Print date, time, user, IP, and result.**
```bash
awk '{print $1, $2, $3, $4, $6}' auth_events.log | column -t
```

**2. Count the total number of authentication events.**
```bash
awk 'END {print "Total auth events:", NR}' auth_events.log
```

**3. Count successful LOGIN events and failed LOGIN events separately.**
```bash
awk '
$5 == "LOGIN" && $6 == "SUCCESS" { success++ }
$5 == "LOGIN" && $6 == "FAIL"    { fail++ }
END {
    print "Successful LOGINs:", success
    print "Failed LOGINs:", fail
}
' auth_events.log
```

**4. Count failed LOGIN events per user and print suspicious users who have at least 3 failed LOGIN events.**
```bash
awk '
$5 == "LOGIN" && $6 == "FAIL" { failed_count[$3]++ }
END {
    print "Suspicious Users (>= 3 failed LOGINs):"
    for (u in failed_count) {
        if (failed_count[u] >= 3) print "User:", u, "-> Failed:", failed_count[u], "times"
    }
}
' auth_events.log
```

**5. Print unique IP addresses that produced failed LOGIN events.**
```bash
awk '
$5 == "LOGIN" && $6 == "FAIL" { unique_ips[$4]++ }
END {
    print "Unique IPs with failed LOGINs:"
    for (ip in unique_ips) print ip
}
' auth_events.log
```

---

## Question 4: Advanced Network Log Audit (`network_audit.log`)

**1. Print date, time, IP, endpoint, status, and latency_ms.**
```bash
awk '{print $1, $2, $3, $5, $6, $8}' network_audit.log | column -t
```

**2. Count the total number of log records.**
```bash
awk 'END {print "Total log records:", NR}' network_audit.log
```

**3. Count the total number of requests per day.**
```bash
awk '
{ req_per_day[$1]++ }
END { for (day in req_per_day) print day, "Total Requests:", req_per_day[day] }
' network_audit.log
```

**4. Count the number of successful requests per day.**
```bash
awk '
$6 == 200 || $6 == 201 || $6 == 204 { success[$1]++ }
END { for (day in success) print day, "Success Requests:", success[day] }
' network_audit.log
```

**5. Count the number of failed requests per day.**
```bash
awk '
$6 >= 400 || $6 == "INVALID" { failed[$1]++ }
END { for (day in failed) print day, "Failed Requests:", failed[day] }
' network_audit.log
```

**6. Calculate the average latency per day. Only use records where status is numeric.**
```bash
awk '
$6 ~ /^[0-9]+$/ { total_latency[$1] += $8; count[$1]++ }
END {
    for (day in total_latency)
        print day, "Avg Latency:", total_latency[day] / count[day], "ms"
}
' network_audit.log
```
