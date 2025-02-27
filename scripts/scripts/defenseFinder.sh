#!/bin/bash

file_=$1
filename=$(basename -- "$file_")
filename="${filename%%.*}"

# Initialize conda
eval "$(conda shell.bash hook)"
conda init
conda activate defensefinder

defense-finder update 

echo "DefenseFinder is installed and ready to use."
mkdir -p ../results/result_Finder/$filename

defense-finder run -o ../results/result_Finder/$filename $file_

conda deactivate
