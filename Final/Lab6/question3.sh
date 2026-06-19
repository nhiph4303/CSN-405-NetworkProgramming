#!/bin/bash

echo -n "Enter a number n: "
read n

sum=0

for (( i=1; i<=n; i++ ))
do
    sum=$((sum + i))
done
h
echo "The sum from 1 to $n is: $sum"
