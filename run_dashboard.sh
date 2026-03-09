#!/bin/bash
# Sovereign Memory Fortress 대시보드 서버 구동 스크립트

echo "=== Sovereign Memory Fortress 대시보드 서버 구동 ==="
echo "시작 시간: $(date)"
echo ""

# 1. 포트 확인 (기본 8501, 사용 중이면 다음 포트)
PORT=8501
while netstat -tuln | grep ":$PORT " > /dev/null; do
    echo "⚠️ 포트 $PORT 사용 중, 다음 포트 시도..."
    PORT=$((PORT + 1))
    if [ $PORT -gt 8510 ]; then
        echo "❌ 사용 가능한 포트를 찾을 수 없음 (8501-8510)"
        exit 1
    fi
done

echo "✅ 사용 포트: $PORT"

# 2. Streamlit 서버 구동
echo ""
echo "2. Streamlit 서버 구동..."
echo "대시보드 파일: /tmp/swp_comms/dashboard.py"
echo "접속 주소: http://localhost:$PORT"

# 백그라운드에서 서버 실행
streamlit run /tmp/swp_comms/dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true &

# 프로세스 ID 저장
SERVER_PID=$!
echo $SERVER_PID > /tmp/swp_comms/streamlit_pid.txt
echo "✅ 서버 프로세스 ID: $SERVER_PID"

# 3. 서버 상태 확인
echo ""
echo "3. 서버 상태 확인..."
sleep 3
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Streamlit 서버 실행 중 (PID: $SERVER_PID)"
    echo "접속 정보:"
    echo "• 로컬: http://localhost:$PORT"
    echo "• 네트워크: http://$(hostname -I | awk '{print $1}'):$PORT"
    echo "• PID 파일: /tmp/swp_comms/streamlit_pid.txt"
else
    echo "❌ Streamlit 서버 시작 실패"
    exit 1
fi

# 4. 서버 종료 스크립트 생성
cat > /tmp/swp_comms/stop_dashboard.sh << 'STOPEOF'
#!/bin/bash
# 대시보드 서버 종료 스크립트
if [ -f "/tmp/swp_comms/streamlit_pid.txt" ]; then
    PID=$(cat /tmp/swp_comms/streamlit_pid.txt)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "✅ Streamlit 서버 종료 (PID: $PID)"
        rm /tmp/swp_comms/streamlit_pid.txt
    else
        echo "⚠️ 서버 프로세스 없음"
    fi
else
    echo "⚠️ PID 파일 없음"
fi
STOPEOF

chmod +x /tmp/swp_comms/stop_dashboard.sh
echo "✅ 서버 종료 스크립트 생성 완료: /tmp/swp_comms/stop_dashboard.sh"

echo ""
echo "=== 서버 구동 완료 ==="
echo "서버가 백그라운드에서 실행 중입니다."
echo "종료 명령: ./stop_dashboard.sh"
