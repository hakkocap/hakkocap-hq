# ⚓ Sujuon Weapon Selector Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    docker.io \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY weapon_selector.py .

# Environment variables (set at runtime)
# GITHUB_TOKEN=your_github_token
# TELEGRAM_TOKEN=your_bot_token
# CHAT_ID=your_chat_id

# Run with Docker socket mounted:
# docker run -v /var/run/docker.sock:/var/run/docker.sock \
#   -e GITHUB_TOKEN=xxx -e TELEGRAM_TOKEN=xxx -e CHAT_ID=xxx \
#   sujon-weapon-selector

CMD ["python", "weapon_selector.py"]
