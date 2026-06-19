#!/bin/bash

LOG_FILE="q3_server.log"
echo "==Q3 AUDIT=="

if [ ! -f "$LOG_FILE" ]; then
    echo "1. q3_server.log does not exist."
    exit 1
fi

echo "1. q3_server.log exists"

awk '
BEGIN { 
    total=0; 
    invalid=0; 
    valid_count=0; 
    valid_sum=0; 
    highest=-9999; 
    
    # Init classification counts to 0
    class["EXCELLENT"] = 0
    class["GOOD"] = 0
    class["AVERAGE"] = 0
    class["POOR"] = 0
}
{
    total++
    result = $NF
    score = $(NF-1)
    
    if (result == "INVALID") {
        invalid++
    } else {
        # Valid numeric score
        valid_count++
        valid_sum += score
        
        if (score > highest) {
            highest = score
        }
        
        class[result]++
    }
}
END {
    print "2. Total number of requests: " total
    print "3. Number of INVALID inputs: " invalid
    
    if (valid_count > 0) {
        printf "4. Average valid score: %.2f\n", valid_sum / valid_count
    } else {
        print "4. Average valid score: 0"
    }
    
    print "5. Count how many students belong to each classification:"
    print "   - EXCELLENT: " class["EXCELLENT"]
    print "   - GOOD:      " class["GOOD"]
    print "   - AVERAGE:   " class["AVERAGE"]
    print "   - POOR:      " class["POOR"]
    
    if (valid_count > 0) {
        print "6. Highest valid score: " highest
    } else {
        print "6. Highest valid score: N/A"
    }
}' "$LOG_FILE"
