#!/bin/bash

# Assign arguments to variables
result_finder="$1"
result_genomad="$2"
file_name="$3"
result_phastest="$4"
base_name="$5"

# Activate the conda environment
# Initialize conda
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

# Run the Python script with the provided arguments
$PYTHON_BIN scripts/proje.py "$result_finder" "$result_genomad" "$file_name" --path_to_phastest_result_folder "$result_phastest"

$PYTHON_BIN scripts/visualisation.py -f "./merged_res.csv" -b "$base_name" -o "$result_genomad/$file_name"

# Deactivate the conda environment
conda deactivate