#!/bin/bash

# Check if uv is installed
if ! command -v uv &> /dev/null
then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

echo "Setting up SparkSerial Pro..."
uv sync

echo "Setup complete. You can now run the tool using ./run.sh"
