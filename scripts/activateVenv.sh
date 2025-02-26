#!/bin/bash
echo "Checking if conda is installed..."
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Installing Miniconda for the current user..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p $HOME/miniconda
    export PATH="$HOME/miniconda/bin:$PATH"
    echo 'export PATH=$HOME/miniconda/bin:$PATH' >> ~/.bashrc
    source ~/.bashrc
    rm ~/miniconda.sh
    echo "Miniconda installed successfully."
    exit 0
fi
echo "Conda is already installed."
