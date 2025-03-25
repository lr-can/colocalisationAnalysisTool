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

if [ -d "./results/result_Finder/$filename" ]; then
    echo -e "\e[31mWARNING : output directory already exists for $filename, skipping DefenseFinder step.\e[0m"
    conda deactivate
    exit 0
fi

defense-finder run -o ./results/result_Finder/$filename $file_

conda deactivate
