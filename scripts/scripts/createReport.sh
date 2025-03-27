#!/bin/bash

# Assign arguments to variables
base_name=$(date +"%Y%m%d%H%M%S")

# Activate the conda environment
eval "$(conda shell.bash hook)" > /dev/null 2>&1
conda init > /dev/null 2>&1
echo -e "\e[36mActivating colocATool environment\e[0m"
conda activate colocATool


python ./scripts/createReport.py -b "$base_name" -i

# Deactivate the conda environment
conda deactivate