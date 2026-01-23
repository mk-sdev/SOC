#!/bin/bash

# execute this only from the root directory on the host

shopt -s nullglob  ## the loops should execute even if there are no files in the dir

LOG_DIR="./logs"

FILES=()

if [ $# -eq 0 ]; then
    # clear all files if no arguments provided
    FILES=("$LOG_DIR"/*.{log,csv})
else
    # match fragments to file names
    for arg in "$@"; do
        matches=("$LOG_DIR/"*"$arg"*".log" "$LOG_DIR/"*"$arg"*".csv")
        FILES+=("${matches[@]}")
    done
fi

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Clearing file: $file"
        > "$file"
    else
        echo "No matching file for: $file"
    fi
done
