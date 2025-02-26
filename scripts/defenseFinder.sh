#!/bin/bash

# Initialize conda
eval "$(conda shell.bash hook)"
conda init
conda activate defensefinder

defense-finder update 

echo "DefenseFinder is installed and ready to use."
defense-finder run --help
conda deactivate