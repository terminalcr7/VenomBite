#!/bin/bash
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install pycryptodome colorama requests netifaces python-dateutil
else
    source venv/bin/activate
fi
python3 main.py "$@"
deactivate
