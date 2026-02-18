#!/bin/bash

'''
Log Cleanup Utility

Truncates log and analysis files in the shared logs directory without
deleting them (preserves file descriptors).

Usage:
  ./logs/clear_logs.sh   # on host (from project root)
  clean                  # alias inside blue container

Behavior:
  clean            - clears all *.log, *.csv, *.json files
  clean <pattern>  - clears files containing <pattern>
                     e.g., clean col == clean collected.log

The script auto-detects environment:
  - /logs   (inside Docker)
  - ./logs  (host execution)
'''


shopt -s nullglob  ## the loops should execute even if there are no files in the dir

if [ -f /.dockerenv ]; then
    LOG_DIR="/logs"
else 
    LOG_DIR="./logs"
fi

FILES=()

if [ $# -eq 0 ]; then
    # clear all files if no arguments provided
    FILES=("$LOG_DIR"/*.{log,csv,json})
else
    # match fragments to file names
    for arg in "$@"; do
        matches=("$LOG_DIR/"*"$arg"*".log" "$LOG_DIR/"*"$arg"*".csv" "$LOG_DIR/"*"$arg"*".json")
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
