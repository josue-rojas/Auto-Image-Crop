#!/bin/bash
cd "$(dirname "$0")"
mkdir images
python localhost.py & ./ngrok http 8080
