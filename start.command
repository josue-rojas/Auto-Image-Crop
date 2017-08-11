#!/bin/bash
cd "$(dirname "$0")"
mkdir images #jus in case you didnt make one (might need sudo for some)
open crop.command & python localhost.py & ./ngrok start --none
