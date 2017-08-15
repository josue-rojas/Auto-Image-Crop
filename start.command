#!/bin/bash
cd "$(dirname "$0")"
mkdir images #jus in case you didnt make one (might need sudo for some)
python crop.py
