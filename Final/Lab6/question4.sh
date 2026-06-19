#!/bin/bash

echo -n "Enter score for Subject 1: "
read s1
echo -n "Enter score for Subject 2: "
read s2
echo -n "Enter score for Subject 3: "
read s3

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
