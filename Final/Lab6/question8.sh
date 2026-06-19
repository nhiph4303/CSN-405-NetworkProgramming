#!/bin/bash

echo "=== PART C AUTOMATION SCRIPTS ==="
echo ""

echo "1. All lines containing 'GET':"
grep "GET" access.log
echo "---------------------------------------"

echo "2. Number of lines containing 'GET':"
grep -c "GET" access.log
echo "---------------------------------------"

echo "3. Extracted IP addresses:"
cut -d ' ' -f 1 access.log
echo "---------------------------------------"

echo "4. Number of regular files in current directory:"
find . -maxdepth 1 -type f | wc -l
echo "---------------------------------------"
