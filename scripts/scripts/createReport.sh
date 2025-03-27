#!/bin/bash

# Assign arguments to variables
base_name="$1"
base_name="${base_name%%.*}"

# Activate the conda environment
eval "$(conda shell.bash hook)" > /dev/null 2>&1
conda init > /dev/null 2>&1
echo -e "\e[36mActivating colocATool environment\e[0m"
conda activate colocATool

# Run the Python script with the provided arguments
python ./scripts/createReport.py -b $base_name -i

# Deactivate the conda environment
conda deactivate