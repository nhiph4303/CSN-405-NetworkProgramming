# LAB 6 – Linux Command Line and Log File Processing
**Sinh viên:** Phan Ngọc Hạnh Nhi
**MSSV:** 2131209002

---

## Part A: Basic Command Line

**1. Print hello world.**
```bash
echo "hello world"
```

**2. Show the current working directory.**
```bash
pwd
```

**3. List files and directories, one per line.**
```bash
ls -1
```

**4. Create an empty file named CSN405_file.txt**
```bash
touch CSN405_file.txt
```

**5. Create the directory tmp/files.**
```bash
mkdir -p tmp/files
```

**6. Copy CSN405_file.txt into tmp/files.**
```bash
cp CSN405_file.txt tmp/files/
```

**7. Move CSN405_file.txt into tmp/files.**
```bash
mv CSN405_file.txt tmp/files/
```

**8. List files at the current working directory**
```bash
ls
```

**9. Create a symbolic link to tmp/files/CSN405_file.txt**
```bash
ln -s tmp/files/CSN405_file.txt my_link
```
*(Giải thích sự khác biệt giữa Soft Link và Hard Link như trong file Word của bạn)*
- **Soft Link (Symbolic Link):** Là shortcut trỏ đến đường dẫn của file gốc. Nếu xóa file gốc, link sẽ bị hỏng (dangling). Có thể trỏ khác phân vùng ổ cứng, có thể trỏ tới thư mục. Lệnh tạo: `ln -s`
- **Hard Link:** Trỏ thẳng tới vùng nhớ (inode) của file gốc trên ổ cứng. Xóa file gốc thì Hard Link vẫn xài được bình thường cho đến khi tất cả các hard link bị xóa hết. Không thể trỏ khác phân vùng, không thể trỏ tới thư mục. Lệnh tạo: `ln`

---

## Part B: Working with Text Files

**1. Display the full content of access.log.**
```bash
cat access.log
```

**2. Display the last 5 lines of access.log.**
```bash
tail -n 5 access.log
```

**3. Sort the content of access.log and print the result**
```bash
sort access.log
```

---

## Part C: Searching and Counting

**1. Print all lines in access.log that contain GET.**
```bash
grep "GET" access.log
```

**2. Count how many lines in access.log contain GET.**
```bash
grep -c "GET" access.log
```

**3. Extract all IP addresses from access.log.**
```bash
# Dùng grep với Regex (Biểu thức chính quy) để tìm đúng định dạng của địa chỉ IP
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' access.log
```

**4. Count the number of regular files in the current directory.**
```bash
# Lọc ra các file (-type f) trong thư mục hiện tại không đi sâu vào thư mục con (-maxdepth 1) và đếm số dòng (wc -l)
find . -maxdepth 1 -type f | wc -l
```

---

## Part D: Bash Script

**1. Write a Bash script that prints numbers from 1 to 50 on one line, separated by spaces.**
```bash
#!/bin/bash
for i in {1..50}
do 
    echo -n "$i "
done
```

**2. Write a script to calculate the sum of two numbers entered by a user. (two ways)**
**Way 1:** (Dùng lệnh `read` để nhập từ bàn phím lúc đang chạy)
```bash
#!/bin/bash
echo "Enter first number: "
read num1
echo "Enter second number: "
read num2

sum=$((num1 + num2))
echo "Way 1: $num1 + $num2 = $sum"
```

**Way 2:** (Truyền tham số trực tiếp lúc gọi lệnh, VD: `bash script.sh 5 2`)
```bash
#!/bin/bash
# Kiểm tra xem người dùng có truyền đúng 2 tham số không ($# là số lượng tham số)
if [ $# -ne 2 ]; then
    echo "Usage: $0 num1 num2"
    exit 1
fi

sum=$(($1 + $2))
echo "SUM = $sum"
```

**3. Write a script that takes a number n as input and then prints the sum of its digits from 1 to n.**
```bash
#!/bin/bash
echo -n "Enter a number n: "
read n

sum=0
for (( i=1; i<=n; i++ ))
do
    sum=$((sum + i))
done
echo "The sum from 1 to $n is: $sum"
```

**4. Write a script to input the scores of 3 subjects, calculate the average, and then rank them.**
```bash
#!/bin/bash
echo -n "Enter score for Subject 1: "
read s1
echo -n "Enter score for Subject 2: "
read s2
echo -n "Enter score for Subject 3: "
read s3

# Dùng lệnh bc để tính toán số thập phân trong bash
avg=$(echo "scale=2; ($s1 + $s2 + $s3) / 3" | bc)
echo "Average score is: $avg"

if [ $(echo "$avg >= 8" | bc) -eq 1 ]; then
    echo "Ranking: Excellent"
elif [ $(echo "$avg >= 6" | bc) -eq 1 ]; then
    echo "Ranking: Good"
elif [ $(echo "$avg >= 5" | bc) -eq 1 ]; then
    echo "Ranking: Average"
else
    echo "Ranking: Poor"
fi
```

**5. Write a script that takes multiple numbers from command-line parameters and finds: largest, smallest, sum.**
```bash
#!/bin/bash
if [ $# -eq 0 ]; then
    echo "Please provide numbers as arguments!"
    exit 1
fi

max=$1
min=$1
sum=0

# $@ là mảng chứa tất cả các argument truyền vào
for num in "$@"
do
    sum=$((sum + num))
    if [ $num -gt $max ]; then max=$num; fi
    if [ $num -lt $min ]; then min=$num; fi
done

echo "Largest number: $max"
echo "Smallest number: $min"
echo "Sum: $sum"
```

**6. Write a script to read numbers from the file numbers.txt and calculate how many prime numbers.**
```bash
#!/bin/bash
file="numbers.txt"

is_prime() {
    n=$1
    if [ $n -lt 2 ]; then return 1; fi
    for ((i=2; i*i<=n; i++))
    do
        if [ $((n % i)) -eq 0 ]; then return 1; fi
    done
    return 0
}

prime_count=0

while IFS= read -r line
do
    num=$(echo "$line" | xargs)
    if [[ "$num" =~ ^[0-9]+$ ]]; then
        if is_prime "$num"; then
            prime_count=$((prime_count + 1))
        fi
    fi
done < "$file"

echo "NO. prime number: $prime_count"
```

**7. Write a script to read a file containing multiple numbers, ignore invalid rows, and only sum rows that are integers.**
```bash
#!/bin/bash
file="input.txt"
sum=0

while IFS= read -r line
do
    row=$(echo "$line" | xargs)
    # Kiểm tra Regex xem dòng đó có phải số nguyên không (kể cả số âm)
    if [[ "$row" =~ ^-?[0-9]+$ ]]; then
        sum=$((sum + row))
    fi
done < "$file"

echo "Sum = $sum"
```

**8. Write a script for part C**
```bash
#!/bin/bash
echo "1. All lines containing 'GET':"
grep "GET" access.log

echo "2. Number of lines containing 'GET':"
grep -c "GET" access.log

echo "3. Extracted IP addresses:"
cut -d ' ' -f 1 access.log

echo "4. Number of regular files in current directory:"
find . -maxdepth 1 -type f | wc -l
```
