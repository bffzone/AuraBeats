<div align="center"><img src="assets/images/logo.png" alt="AuraBeats Logo" width="150"/>
🎧 AuraBeats
The Most Advanced Telegram Music Bot
https://img.shields.io/badge/Python-3.12-blue.svg?style=for-the-badge&logo=python
https://img.shields.io/badge/Kurigram-2.2.26-green.svg?style=for-the-badge
https://img.shields.io/badge/PyTgCalls-3.0.0-orange.svg?style=for-the-badge
https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge

⚡ Fast • 🎨 Unique • 💎 Feature-Rich

Made with ❤️ by AuraBeatsOfficial

</div>
🎯 About
AuraBeats is a production-grade Telegram music bot built from scratch with Python 3.12, Kurigram, and PyTgCalls. It streams high-quality audio to Telegram voice chats with live progress bars, thumbnails, audio filters, and beautiful UI.

✨ Features
🎵 Core Music
✅ Stream from YouTube

✅ High-quality audio (up to 320kbps)

✅ Queue management

✅ Auto-play next song

✅ Smart search with live animation

✅ Thumbnail support

🎛️ Audio Filters
🎸 Bass Boost

🎼 Treble Boost

🌙 Nightcore

🌊 Vaporwave

🎧 8D Audio

🎤 Karaoke

🏛️ Reverb

🎨 Premium UI
✅ Live progress bar (updates every 10s)

✅ Compact now-playing cards

✅ Thumbnail with every song

✅ Submenu buttons

✅ Pause/Resume timer

✅ Auto-delete commands

💎 Extra Features
✅ Download songs (MP3/MP4) via DM

✅ Clickable song links

✅ User settings

✅ Multi-language support

✅ Credits protection (anti-copy)

✅ Admin panel

📦 Installation
Prerequisites
Python 3.12 (recommended)

FFmpeg

Git

MongoDB (optional — JSON storage included)

Quick Setup
bash
git clone https://github.com/SakilSakil699/AuraBeats.git
cd AuraBeats
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python main.py
Using Makefile
bash
make venv          # Create virtual environment
make install       # Install dependencies
make run           # Start bot
make stop          # Stop bot
make restart       # Restart bot
make help          # Show all commands
🔑 Get Credentials
Credential	Where to Get
API_ID & API_HASH	my.telegram.org
BOT_TOKEN	@BotFather
SESSION_STRING	Run python scripts/session_gen.py
OWNER_ID	@userinfobot
🎮 Commands
🎵 Music
Command	Description
/play <song>	Play a song
/pause	Pause playback
/resume	Resume playback
/skip	Skip current song
/stop	Stop and clear queue
🎛️ Filters
Command	Effect
/bass	Bass boost
/nightcore	Nightcore effect
/8d	8D audio
/karaoke	Remove vocals
/reverb	Concert hall reverb
📋 Queue
Command	Description
/queue	Show current queue
/shuffle	Shuffle queue
/loop	Toggle loop mode
/clear	Clear queue
⚙️ Settings
Command	Description
/settings	Bot settings
/lang	Change language
/stats	Bot statistics
/ping	Check latency
🚀 Deployment
Termux (Android)
bash
pkg install proot-distro -y
proot-distro install ubuntu
proot-distro login ubuntu
Docker
bash
docker-compose up -d
docker-compose logs -f
VPS (Ubuntu/Debian)
bash
sudo apt update
sudo apt install python3.12 python3.12-venv ffmpeg git -y
Cloud Platforms
✅ Render

✅ Railway

✅ Fly.io

✅ Koyeb

✅ Heroku

📁 Project Structure
text
AuraBeats/
├── config/          # Configuration
├── core/            # Core engine
├── filters/         # FFmpeg filters
├── locales/         # Multi-language support
├── models/          # Data models
├── plugins/         # Command handlers
├── scripts/         # Utility scripts
├── services/        # Business logic
├── ui/              # UI components
├── utils/           # Helper functions
├── main.py          # Entry point
└── requirements.txt # Dependencies
🛡️ Credits Protection
AuraBeats includes built-in anti-copy protection:

✅ Visible credit: Made By AuraBeatsOfficial

✅ Hidden watermark (Base64 + Hex)

✅ SHA-256 integrity hash

✅ Runtime verification

✅ Removing credits will break the bot

🤝 Contributing
Contributions are welcome! See CONTRIBUTING.md

🐛 Issues
Found a bug? Open an issue

📜 License
This project is licensed under the MIT License — see LICENSE

👨‍💻 Author
<div align="center">
AuraBeatsOfficial

https://img.shields.io/badge/Telegram-@Vip__Sakil__Bio-2CA5E0?style=for-the-badge&logo=telegram
https://img.shields.io/badge/GitHub-SakilSakil699-181717?style=for-the-badge&logo=github

</div>
<div align="center">
⭐ Star this repo if you found it useful!

Made with ❤️ in India 🇮🇳

</div>
