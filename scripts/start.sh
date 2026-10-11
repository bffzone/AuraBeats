#!/data/data/com.termux/files/usr/bin/bash
# AuraBeats - Start Script
# Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)

cd "$(dirname "$0")/.."

# Acquire wake lock so Termux keeps running
command -v termux-wake-lock &>/dev/null && termux-wake-lock

# Check .env
if [ ! -f ".env" ]; then
    echo "❌ .env missing! Run: bash scripts/setup.sh"
    exit 1
fi

echo "🎧 Starting AuraBeats..."
python3 main.py
