#!/bin/bash

if [ -d ".venv" ]; then
    echo ".venv directory already exists. Skipping virtual environment creation."
    source .venv/bin/activate
    echo "Virtual environment has successfully been activated" 
    exit 0
fi 

echo "Creating and activating a virtual environment..."
# Create a virtual environment in the current directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

echo "Virtual environment created and activated."