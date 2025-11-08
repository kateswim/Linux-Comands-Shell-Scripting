#!/bin/bash
# Example: Batch rename files
# Why Bash? - String manipulation and loops work naturally

# Rename all .txt files to have prefix
counter=1
for file in *.txt; do
    if [ -f "$file" ]; then
        mv "$file" "document_${counter}.txt"
        echo "Renamed: $file -> document_${counter}.txt"
        ((counter++))
    fi
done

