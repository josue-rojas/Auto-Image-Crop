#!/bin/bash
cd "$(dirname "$0")"
python localhost.py & ./ngrok http 8080
