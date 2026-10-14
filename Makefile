# ═══════════════════════════════════════
#   AuraBeats - Makefile
#   Author: AuraBeatsOfficial (@Vip_Sakil_Bio)
# ═══════════════════════════════════════

.PHONY: help install install-dev venv activate test lint format clean run stop restart logs

# ─── Variables ───
PYTHON = python3
VENV = venv
VENV_BIN = $(VENV)/bin

# ═══════════════════════════════════════
#   HELP (default)
# ═══════════════════════════════════════
help:
	@echo ""
	@echo "  🎧 AuraBeats - Available Commands"
	@echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "  Setup:"
	@echo "    make venv          Create virtual environment"
	@echo "    make install       Install dependencies"
	@echo "    make install-dev   Install dev dependencies"
	@echo ""
	@echo "  Run:"
	@echo "    make run           Start the bot"
	@echo "    make stop          Stop the bot"
	@echo "    make restart       Restart the bot"
	@echo "    make logs          Show recent logs"
	@echo ""
	@echo "  Code Quality:"
	@echo "    make test          Run tests"
	@echo "    make lint          Check code style"
	@echo "    make format        Auto-format code"
	@echo "    make clean         Clean cache and temporary files"
	@echo ""
	@echo "  Info:"
	@echo "    make version       Show version"
	@echo "    make status        Show bot status"
	@echo ""

# ═══════════════════════════════════════
#   SETUP
# ═══════════════════════════════════════
venv:
	@echo "📦 Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "✅ Venv created"

activate:
	@echo "Activate venv with: source $(VENV_BIN)/activate"

install:
	@echo "📦 Installing dependencies..."
	$(VENV_BIN)/pip install --upgrade pip setuptools wheel
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "✅ Dependencies installed"

install-dev:
	@echo "📦 Installing dev dependencies..."
	$(VENV_BIN)/pip install -r requirements-dev.txt
	@echo "✅ Dev dependencies installed"

# ═══════════════════════════════════════
#   RUN
# ═══════════════════════════════════════
run:
	@echo "🚀 Starting AuraBeats..."
	$(VENV_BIN)/python main.py

run-bg:
	@echo "🚀 Starting AuraBeats in background..."
	@nohup $(VENV_BIN)/python main.py > data/logs/bot.log 2>&1 &
	@echo "✅ Bot started in background"
	@echo "📋 View logs: tail -f data/logs/bot.log"

stop:
	@echo "⏹️ Stopping AuraBeats..."
	@pkill -f "python main.py" || echo "No bot running"
	@echo "✅ Stopped"

restart: stop run

logs:
	@echo "📋 Recent logs:"
	@tail -n 50 data/logs/*.log 2>/dev/null || echo "No logs found"

# ═══════════════════════════════════════
#   QUALITY
# ═══════════════════════════════════════
test:
	@echo "🧪 Running tests..."
	$(VENV_BIN)/pytest tests/ -v

lint:
	@echo "🔍 Linting code..."
	$(VENV_BIN)/flake8 src/ plugins/ core/ services/ ui/ utils/ 2>/dev/null || echo "flake8 not installed"

format:
	@echo "✨ Formatting code..."
	$(VENV_BIN)/black . 2>/dev/null || echo "black not installed"
	$(VENV_BIN)/isort . 2>/dev/null || echo "isort not installed"

clean:
	@echo "🧹 Cleaning..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@rm -rf .pytest_cache .mypy_cache htmlcov .coverage 2>/dev/null || true
	@echo "✅ Cleaned"

clean-all: clean
	@echo "🧹 Full clean..."
	@rm -rf $(VENV) 2>/dev/null || true
	@echo "✅ Venv removed"

# ═══════════════════════════════════════
#   INFO
# ═══════════════════════════════════════
version:
	@echo "🎧 AuraBeats v1.0.0"
	@echo "👨‍💻 Made By AuraBeatsOfficial"
	@echo "📱 @Vip_Sakil_Bio"

status:
	@echo "📊 Bot Status:"
	@ps aux | grep "python main.py" | grep -v grep || echo "❌ Not running"

# ═══════════════════════════════════════
#   DATABASE
# ═══════════════════════════════════════
db-backup:
	@echo "💾 Backing up database..."
	@mkdir -p data/backups
	@cp data/aurobeats.json data/backups/aurobeats_$$(date +%Y%m%d_%H%M%S).json
	@echo "✅ Backup created"

db-restore:
	@echo "🔄 Restoring database..."
	@echo "Usage: make db-restore FILE=data/backups/filename.json"

db-reset:
	@echo "⚠️ Resetting database..."
	@rm -f data/aurobeats.json
	@echo "✅ Database reset (will recreate on next start)"
