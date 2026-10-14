# ═══════════════════════════════════════
#   AuraBeats - Dockerfile
#   Author: AuraBeatsOfficial (@Vip_Sakil_Bio)
# ═══════════════════════════════════════

FROM python:3.12-slim

# Metadata
LABEL maintainer="AuraBeatsOfficial <https://t.me/Vip_Sakil_Bio>"
LABEL description="AuraBeats - The Most Advanced Telegram Music Bot"
LABEL version="1.0.0"

# Environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Kolkata

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    curl \
    wget \
    build-essential \
    cmake \
    pkg-config \
    libopus-dev \
    libvpx-dev \
    libssl-dev \
    libffi-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directories
RUN mkdir -p data/{downloads,cache,logs,sessions} \
    assets/images

# Non-root user
RUN useradd -m -u 1000 aurabeats && \
    chown -R aurabeats:aurobeats /app

USER aurabeats

# Health check
HEALTHCHECK --interval=60s --timeout=15s --start-period=90s --retries=3 \
    CMD python -c "import os, sys; sys.exit(0 if os.path.exists('main.py') else 1)"

# Expose port (for POT server if needed)
EXPOSE 4416

# Start bot
CMD ["python", "main.py"]
