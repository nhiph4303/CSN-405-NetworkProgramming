#!/bin/bash

file="input.txt"

if [ ! -f "$file" ]; then
    echo "File $file does not exist!"
    exit 1
fi

sum=0

while IFS= read -r line
do
    row=$(echo "$line" | xargs)
    
    if [[ "$row" =~ ^-?[0-9]+$ ]]; then
        sum=$((sum + row))
    fi
done < "$file"

echo "Sum = $sum"
