#!/bin/bash

# Initialize conda
eval "$(conda shell.bash hook)"
conda init
conda activate defensefinder

defense-finder update 

echo "DefenseFinder is installed and ready to use."
defense-finder run --help

defense-finder run -o result_Finder ../ressources/GCF_000006765.1.fa.gz

conda deactivate
