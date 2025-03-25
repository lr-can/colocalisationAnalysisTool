#!/bin/bash

# Assign arguments to variables
result_finder=$1
result_genomad=$2
file_name=$3
result_phastest=$4

# Activate the conda environment
# Initialize conda
eval "$(conda shell.bash hook)"
conda init
conda activate colocATool

# Run the Python script with the provided arguments
python ./proje.py "$result_finder" "$result_genomad" "$file_name" "$result_phastest"

# Deactivate the conda environment
conda deactivate