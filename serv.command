#!/bin/bash
cd "$(dirname "$0")"
sudo mkdir images
python localhost.py & ./ngrok start --none
