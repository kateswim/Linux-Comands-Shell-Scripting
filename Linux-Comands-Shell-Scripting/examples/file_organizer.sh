#!/bin/bash
# Example: Organize files by extension
# Why Bash? - Perfect for file operations, loops, and conditionals

# Move files to folders by extension
for file in *.*; do
    if [ -f "$file" ]; then
        ext="${file##*.}"
        mkdir -p "$ext"
        mv "$file" "$ext/"
        echo "Moved $file to $ext/"
    fi
done

