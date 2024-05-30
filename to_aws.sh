#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Deactivate any active virtual environment
deactivate 2>/dev/null || true

# Navigate to the site-packages directory of the virtual environment
cd v-env/lib/python3.10/site-packages

# Create a ZIP file containing all installed packages
zip -r9 ../../../../lambda_function.zip .

# Navigate back to the project root directory
cd ../../../../

# Add your lambda function code to the ZIP file
zip -g lambda_function.zip lambda_function.py
