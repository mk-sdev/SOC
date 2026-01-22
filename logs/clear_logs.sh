#!/bin/bash

# execute this only from the root directory on the host

shopt -s nullglob # the loops should execute even if there are no files in the dir

for file in ./logs/*.{log,csv}; do
    if [ -f "$file" ]; then
        echo "Clearing file: $file"
        > "$file"
    fi
done
