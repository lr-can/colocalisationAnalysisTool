#!/bin/bash

# Initialize conda
eval "$(conda shell.bash hook)"
conda activate defensefinder

defense-finder update 
conda deactivate