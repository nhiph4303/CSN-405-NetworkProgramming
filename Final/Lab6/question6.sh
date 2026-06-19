#!/bin/bash

file="numbers.txt"

if [ ! -f "$file" ]; then
    echo "File $file does not exist!"
    exit 1
fi

is_prime() {
    n=$1
    if [ $n -lt 2 ]; then
        return 1
    fi
    for ((i=2; i*i<=n; i++))
    do
        if [ $((n % i)) -eq 0 ]; then
            return 1
        fi
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
