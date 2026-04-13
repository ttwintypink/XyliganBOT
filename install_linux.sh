#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Done."
echo "1) Copy .env.example to .env"
echo "2) Put your bot token into .env"
echo "3) Start with: source venv/bin/activate && ./start.sh"
