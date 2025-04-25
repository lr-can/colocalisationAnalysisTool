#!/bin/bash

# Check if a file argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <file>"
    exit 1
fi
 # Detect Python interpreter
if command -v python &>/dev/null; then
    PYTHON_BIN=python
elif command -v python3 &>/dev/null; then
    PYTHON_BIN=python3
else
    echo "❌ No Python interpreter found. Please install Python 3 and try again."
    exit 1
fi


# Call the Python script with the provided file
$PYTHON_BIN ./scripts/checkFile.py -f "$1"