#!/bin/bash

# Check if a file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

# Call the Python script with the provided file
python ./scripts/checkFile.py -f "$1"