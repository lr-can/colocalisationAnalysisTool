#!/bin/bash

echo "Creating and activating a virtual environment..."
# Create a virtual environment in the current directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

echo "Virtual environment created and activated."