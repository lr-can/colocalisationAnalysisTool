#!/bin/bash

file_=$1
threads=$2

filename=$(basename -- "$file_")
filename="${filename%%.*}"

# Initialize conda
eval "$(conda shell.bash hook)"

if conda env list | grep -q 'genomad'; then
  echo "Activating existing conda environment 'genomad'"
fi

conda activate genomad

if [ ! -d "genomad_db" ]; then
    echo "Directory 'genomad_db' does not exist. Creating directory and downloading database."
    genomad download-database .
else
    echo "Directory 'genomad_db' already exists. Skipping database download."
fi

echo "Genomad is installed and ready to use."
mkdir -p ./results/results_genomad/$filename
genomad end-to-end --threads "$threads" "$file_" "./results/results_genomad/$filename" genomad_db


conda deactivate
