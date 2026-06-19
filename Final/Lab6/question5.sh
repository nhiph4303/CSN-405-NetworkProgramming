#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Please provide numbers as arguments!"
    exit 1
fi

max=$1
min=$1
sum=0

for num in "$@"
do
    sum=$((sum + num))
    
    if [ $num -gt $max ]; then
        max=$num
    fi

    if [ $num -lt $min ]; then
        min=$num
    fi
done

echo "Largest number: $max"
echo "Smallest number: $min"
echo "Sum: $sum"

