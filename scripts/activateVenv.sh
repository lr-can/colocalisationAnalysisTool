#!/bin/bash

if [ -d ".venv" ]; then
    echo ".venv directory already exists. Skipping virtual environment creation."
    source activate ./.venv
    echo "Virtual environment has successfully been activated" 
    exit 0
else
    echo ".venv directory does not exist. Creating a conda environment..."
    conda create --prefix ./.venv -y
    source activate ./.venv
    echo "Conda environment created and activated."
    exit 0
fi
