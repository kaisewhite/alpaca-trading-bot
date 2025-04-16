#!/bin/bash

# Create a new virtual environment
python3 -m venv venv

# Create a function to activate the virtual environment
activate_venv() {
    source venv/bin/activate
}

# Export the function so it's available in the current shell
export -f activate_venv

# Call the function to activate the virtual environment
activate_venv

# Install the required packages using python3
python3 -m pip install -r requirements.txt