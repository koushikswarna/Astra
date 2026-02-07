#!/bin/bash
# Quick setup script for development.
#
# Usage:
#   source scripts/setup_env.sh
#
# Creates a venv, installs deps, and downloads models.

set -e

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating venv..."
source "$VENV_DIR/bin/activate"

echo "Installing dependencies..."
pip install -r requirements-dev.txt

echo "Downloading models (this may take a while)..."
python scripts/download_models.py

echo ""
echo "Setup complete. Run 'python main.py' to start Astra."
