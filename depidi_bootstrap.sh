#!/bin/bash
# SWP 데피디 자동 부팅 스크립트
# 작성: 2026-03-04

SWP_DIR="/home/hakkocap/다운로드/swp"
VENV="$SWP_DIR/venv"
BACKEND="$SWP_DIR/backend/main.py"
LOG_FILE="$SWP_DIR/data/audit.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 데피디 부팅 시작" >> "$LOG_FILE"

# 1. 가상환경 확인
if [ ! -d "$VENV" ]; then
    echo "[ERROR] venv 없음. 생성 중..."
    python3 -m venv "$VENV"
    source "$VENV/bin/activate"
    pip install -r "$SWP_DIR/requirements.txt"
else
    source "$VENV/bin/activate"
fi

# 2. Port 8080 충돌 확인
if lsof -i:8080 >/dev/null 2>&1; then
    echo "[INFO] Port 8080 이미 사용 중. 기존 프로세스 유지." >> "$LOG_FILE"
    exit 0
fi

# 3. Backend 실행
cd "$SWP_DIR"
nohup python "$BACKEND" >> "$LOG_FILE" 2>&1 &
PID=$!

sleep 3

# 4. 헬스체크
if curl -s http://localhost:8080/health | grep -q "operational"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SWP 부팅 성공 (PID: $PID)" >> "$LOG_FILE"
    exit 0
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SWP 부팅 실패" >> "$LOG_FILE"
    exit 1
fi
