#!/data/data/com.termux/files/usr/bin/bash
# AuraBeats - Initial Setup Script
# Author: Sakil Anowar (@YO_UR_OFFICIAL_CRUSH)

echo "╔══════════════════════════════════════════╗"
echo "║   AuraBeats - Setup Wizard               ║"
echo "║   By Sakil Anowar                        ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python not found!"
    exit 1
fi

# Check .env
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env created. Please fill in your credentials:"
    echo "   nano .env"
    exit 1
fi

# Install requirements
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create data dirs
mkdir -p data/{downloads,cache,logs,sessions}

echo ""
echo "✅ Setup complete!"
echo "▶️  Run the bot: python3 main.py"
