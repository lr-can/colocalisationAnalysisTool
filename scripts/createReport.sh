#!/bin/bash

base_name=$1

# Activate the conda environment
eval "$(conda shell.bash hook)" > /dev/null 2>&1
conda init > /dev/null 2>&1
echo -e "\e[36mActivating colocATool environment\e[0m"
conda activate colocATool

 # Detect Python interpreter
if command -v python &>/dev/null; then
    PYTHON_BIN=python
elif command -v python3 &>/dev/null; then
    PYTHON_BIN=python3
else
    echo "❌ No Python interpreter found. Please install Python 3 and try again."
    exit 1
fi

$PYTHON_BIN ./scripts/createReport.py -b "$base_name" -i

# Deactivate the conda environment
conda deactivate