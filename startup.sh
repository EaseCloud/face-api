#!/usr/bin/env bash

set -e

apt -y install cmake

python3 -m pip install -r requirements.txt

./main.py --tolerance 0.6
