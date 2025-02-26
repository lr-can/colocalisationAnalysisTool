#!/bin/bash

# Initialize conda
eval "$(conda shell.bash hook)"

if conda env list | grep -q 'genomad'; then
  echo "Activating existing conda environment 'genomad'"
fi

conda activate genomad

if [ ! -d "genomad_db" ]; then
    echo "Directory 'genomad_db' does not exist. Creating directory and downloading database."
    genomad download-database .
    rm genomad_db_*_tar.gz
else
    echo "Directory 'genomad_db' already exists. Skipping database download."
fi


conda deactivate