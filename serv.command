#!/bin/bash
mkdir images
cd "$(dirname "$0")"
python localhost.py & ./ngrok http 8080
