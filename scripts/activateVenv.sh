#!/bin/bash

if [ -d ".venv" ]; then
    echo ".venv directory already exists. Skipping virtual environment creation."
    source activate ./.venv
    echo "Virtual environment has successfully been activated" 
else
    echo ".venv directory does not exist. Creating a conda environment..."
    if ! command -v conda &> /dev/null; then
        echo "Conda is not installed. Installing Miniconda for the current user..."
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
        bash ~/miniconda.sh -b -p $HOME/miniconda
        export PATH="$HOME/miniconda/bin:$PATH"
        echo 'export PATH=$HOME/miniconda/bin:$PATH' >> ~/.bashrc
        source ~/.bashrc
        rm ~/miniconda.sh
        echo "Miniconda installed successfully."
    fi
    conda create --prefix ./.venv -y
    source activate ./.venv
    echo "Conda environment created and activated."
fi
current_dir=$(pwd)
export PATH="$current_dir/.venv/bin:$PATH"
source ~/.bashrc
