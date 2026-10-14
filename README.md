<div align="center">

<img src="assets/images/logo.png" alt="AuraBeats" width="180"/>

# 🎧 AuraBeats

**The Most Advanced Telegram Music Bot**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Kurigram](https://img.shields.io/badge/Kurigram-2.2.26-00A67E?style=flat-square)](https://github.com/Kurigram)
[![PyTgCalls](https://img.shields.io/badge/PyTgCalls-3.0.0-FF6B35?style=flat-square)](https://github.com/pytgcalls/pytgcalls)
[![License](https://img.shields.io/badge/License-MIT-FFD700?style=flat-square)](LICENSE)

</div>

---

## ✨ Features

| 🎵 Music | 🎛 Filters | 🎨 UI | 💎 Extras |
|:--------:|:----------:|:-----:|:---------:|
| YouTube Stream | Bass Boost | Live Progress | MP3/MP4 Download |
| High Quality | Nightcore | Thumbnails | User Settings |
| Queue System | Vaporwave | Submenus | Multi-Language |
| Auto-Play | 8D Audio | Timer Pause | Anti-Copy |
| Smart Search | Karaoke | Auto-Delete | Admin Panel |

---

## ⚡ Quick Setup

    git clone https://github.com/SakilSakil699/AuraBeats.git
    cd AuraBeats
    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env
    nano .env
    python main.py

Ya use karo Makefile:

    make venv && make install && make run

---

## 🔑 Credentials

| Key | From |
|-----|------|
| API_ID API_HASH | my.telegram.org |
| BOT_TOKEN | @BotFather |
| SESSION_STRING | python scripts/session_gen.py |

---

## 🎮 Commands

**Music** - /play /pause /resume /skip /stop

**Filters** - /bass /nightcore /8d /karaoke /reverb

**Queue** - /queue /shuffle /loop /clear

**Settings** - /settings /lang /stats /ping

---

# 🚀 Full Deployment Guide

Choose your platform and follow the steps.

---

## 📱 Option 1: Termux (Android)

### Step 1: Install Termux

Download Termux from **F-Droid** (not Play Store).

### Step 2: Install Ubuntu (Proot)

    pkg update && pkg upgrade -y
    pkg install proot-distro -y
    proot-distro install ubuntu
    proot-distro login ubuntu

### Step 3: Install Dependencies

    apt update && apt upgrade -y
    apt install python3.12 python3.12-venv python3.12-dev ffmpeg git build-essential cmake pkg-config libopus-dev libvpx-dev libssl-dev libffi-dev -y

### Step 4: Clone and Setup

    git clone https://github.com/SakilSakil699/AuraBeats.git
    cd AuraBeats
    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Step 5: Configure .env

    cp .env.example .env
    nano .env

Fill in: API_ID, API_HASH, BOT_TOKEN, SESSION_STRING, OWNER_ID

### Step 6: Run Bot

    python main.py

### Step 7: Background Run (Recommended)

    termux-wake-lock
    nohup python main.py > bot.log 2>&1 &

---

## 🐳 Option 2: Docker

### Step 1: Install Docker

    curl -fsSL https://get.docker.com | sh
    sudo usermod -aG docker $USER

### Step 2: Clone Repository

    git clone https://github.com/SakilSakil699/AuraBeats.git
    cd AuraBeats

### Step 3: Configure .env

    cp .env.example .env
    nano .env

### Step 4: Build and Run

    docker-compose up -d

### Step 5: View Logs

    docker-compose logs -f

### Step 6: Stop Bot

    docker-compose down

### Docker Services

| Service | Port | Purpose |
|---------|------|---------|
| aurabeats | 8080 | Main Bot |
| mongodb | 27017 | Database |
| redis | 6379 | Cache |
| pot-server | 4416 | YouTube Bypass |

---

## ☁️ Option 3: Render (Free Cloud)

### Step 1: Fork Repository

Fork this repo to your GitHub account.

### Step 2: Create Render Account

Sign up at render.com (free tier available).

### Step 3: New Web Service

- Click **New** → **Web Service**
- Connect your GitHub fork
- Select **AuraBeats** repository

### Step 4: Configure

| Setting | Value |
|---------|-------|
| Name | aurabeats |
| Region | Singapore |
| Branch | main |
| Runtime | Python 3 |
| Build Command | pip install -r requirements.txt |
| Start Command | python main.py |
| Plan | Free |

### Step 5: Add Environment Variables

Go to **Environment** tab and add:

- API_ID
- API_HASH
- BOT_TOKEN
- SESSION_STRING
- OWNER_ID
- OWNER_USERNAME
- MONGO_URI (use MongoDB Atlas free tier)
- REDIS_URI (use Redis Cloud free tier)

### Step 6: Deploy

Click **Create Web Service**. Wait for build to complete.

Note: Free tier sleeps after 15 min inactivity. Use UptimeRobot to keep alive.

---

## 🚂 Option 4: Railway

### Step 1: Sign Up

Go to railway.app and sign up with GitHub.

### Step 2: New Project

- Click **New Project**
- Select **Deploy from GitHub repo**
- Choose **AuraBeats**

### Step 3: Add Variables

Click **Variables** tab and add:

    API_ID=your_api_id
    API_HASH=your_api_hash
    BOT_TOKEN=your_bot_token
    SESSION_STRING=your_session
    OWNER_ID=your_id
    MONGO_URI=mongodb://...
    REDIS_URI=redis://...

### Step 4: Deploy

Railway auto-deploys. Check **Deployments** tab.

### Step 5: Add MongoDB & Redis

- Click **New** → **Database** → **MongoDB**
- Click **New** → **Database** → **Redis**
- Variables auto-linked

---

## 🪰 Option 5: Fly.io

### Step 1: Install flyctl

    curl -L https://fly.io/install.sh | sh

### Step 2: Login

    flyctl auth login

### Step 3: Launch App

    cd AuraBeats
    flyctl launch

### Step 4: Set Secrets

    flyctl secrets set API_ID=xxx
    flyctl secrets set API_HASH=xxx
    flyctl secrets set BOT_TOKEN=xxx
    flyctl secrets set SESSION_STRING=xxx
    flyctl secrets set OWNER_ID=xxx

### Step 5: Deploy

    flyctl deploy

### Step 6: View Logs

    flyctl logs

---

## 🖥 Option 6: VPS (Ubuntu/Debian)

### Step 1: SSH into VPS

    ssh root@your_server_ip

### Step 2: Update System

    apt update && apt upgrade -y

### Step 3: Install Dependencies

    apt install python3.12 python3.12-venv python3.12-dev ffmpeg git build-essential cmake pkg-config libopus-dev libvpx-dev libssl-dev libffi-dev -y

### Step 4: Install MongoDB (Optional)

    wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-7.0.list
    apt update
    apt install -y mongodb-org
    systemctl start mongod
    systemctl enable mongod

### Step 5: Install Redis (Optional)

    apt install redis-server -y
    systemctl start redis
    systemctl enable redis

### Step 6: Clone and Setup

    cd /root
    git clone https://github.com/SakilSakil699/AuraBeats.git
    cd AuraBeats
    python3.12 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### Step 7: Configure

    cp .env.example .env
    nano .env

### Step 8: Run as systemd Service

Create service file:

    nano /etc/systemd/system/aurobeats.service

Paste:

    [Unit]
    Description=AuraBeats Music Bot
    After=network.target

    [Service]
    Type=simple
    User=root
    WorkingDirectory=/root/AuraBeats
    ExecStart=/root/AuraBeats/venv/bin/python main.py
    Restart=always
    RestartSec=10
    StandardOutput=append:/root/AuraBeats/data/logs/bot.log
    StandardError=append:/root/AuraBeats/data/logs/error.log

    [Install]
    WantedBy=multi-user.target

### Step 9: Enable and Start

    systemctl daemon-reload
    systemctl enable aurabeats
    systemctl start aurabeats

### Step 10: Check Status

    systemctl status aurabeats
    journalctl -u aurabeats -f

---

## 🌐 Option 7: Heroku

### Step 1: Install Heroku CLI

    curl https://cli-assets.heroku.com/install.sh | sh

### Step 2: Login

    heroku login

### Step 3: Create App

    cd AuraBeats
    heroku create aurabeats-bot

### Step 4: Set Environment

    heroku config:set API_ID=xxx
    heroku config:set API_HASH=xxx
    heroku config:set BOT_TOKEN=xxx
    heroku config:set SESSION_STRING=xxx
    heroku config:set OWNER_ID=xxx

### Step 5: Deploy

    git push heroku main

### Step 6: View Logs

    heroku logs --tail

---

## 🔧 Platform Comparison

| Platform | Free | 24/7 | Setup | Best For |
|----------|:----:|:----:|:-----:|----------|
| Termux | ✅ | ⚠️ | Easy | Personal |
| Docker | ✅ | ✅ | Medium | VPS |
| Render | ✅ | ⚠️ | Easy | Testing |
| Railway | ⚠️ | ✅ | Easy | Small |
| Fly.io | ⚠️ | ✅ | Medium | Medium |
| VPS | ❌ | ✅ | Hard | Production |
| Heroku | ❌ | ✅ | Easy | Production |

Note: ⚠️ = Limited (sleeps or has quota), ✅ = Full support

---

## 🛡 Credits Protection

> This bot has built-in anti-copy protection.
> Removing credits will break the bot at startup.

- Visible Credit
- Hidden Watermark (Base64 + Hex)
- SHA-256 Integrity Hash
- Runtime Verification

---

<div align="center">

### 👨‍💻 Author

**AuraBeatsOfficial**

[![Telegram](https://img.shields.io/badge/Telegram-@Vip__Sakil__Bio-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/Vip_Sakil_Bio)
[![GitHub](https://img.shields.io/badge/GitHub-SakilSakil699-181717?style=for-the-badge&logo=github)](https://github.com/SakilSakil699)

**⭐ Star this repo if you found it useful!**

Made with ❤️ in India 🇮🇳

</div>
