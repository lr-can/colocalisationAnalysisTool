#!/bin/bash

# Assign arguments to variables
result_finder="$1"
result_genomad="$2"
file_name="$3"
result_phastest="$4"

# Activate the conda environment
# Initialize conda
eval "$(conda shell.bash hook)"
conda init
conda activate colocATool

# Run the Python script with the provided arguments
python scripts/proje.py "$result_finder" "$result_genomad" "$file_name" --path_to_phastest_result_folder "$result_phastest"

python scripts/visualisation.py -f "./merged_res.csv"

# Deactivate the conda environment
conda deactivate