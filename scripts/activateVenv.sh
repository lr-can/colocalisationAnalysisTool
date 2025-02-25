#!/bin/bash

if [ -d ".venv" ]; then
    echo ".venv directory already exists. Skipping virtual environment creation."
    source activate ./.venv
    echo "Virtual environment has successfully been activated" 
    exit 0
else
    if command -v conda &> /dev/null; then
        echo ".venv directory does not exist. Creating a conda environment..."
        conda create --prefix ./.venv -y
        source activate ./.venv
        echo "Conda environment created and activated."
    else
        echo ".venv directory does not exist. Creating a virtual environment using venv..."
        python3 -m venv .venv
        source .venv/bin/activate
        echo "Virtual environment created and activated using venv."
    fi
    exit 0
fi
