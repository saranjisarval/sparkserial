#!/bin/bash

echo "Launching SparkSerial Pro..."
export PYTHONPATH=$PYTHONPATH:.
uv run python sparkserial/main.py
