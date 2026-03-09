#!/bin/bash
# 캡틴스 대시보드 데모 확인 스크립트

echo "=== 캡틴스 대시보드 데모 확인 ==="
echo "실행 시간: $(date)"
echo ""

# 1. Langflow 서버 상태 확인
echo "1. Langflow 서버 상태 확인..."
if timeout 3 curl -s http://localhost:7860 > /dev/null 2>&1; then
    echo "✅ Langflow 서버 실행 중"
    SERVER_STATUS="running"
else
    echo "⚠️ Langflow 서버 응답 없음 (재시작 중일 수 있음)"
    SERVER_STATUS="down"
fi

# 2. 웹 페이지 기본 확인
echo ""
echo "2. 웹 페이지 기본 확인..."
if [ "$SERVER_STATUS" = "running" ]; then
    PAGE_TITLE=$(curl -s http://localhost:7860 | grep -o '<title>[^<]*</title>' | sed 's/<title>//;s/<\/title>//')
    echo "페이지 제목: $PAGE_TITLE"
    
    # Captain 관련 내용 검색
    CAPTAIN_CONTENT=$(curl -s http://localhost:7860 | grep -i "captain\|board\|상벌점\|게이지" | head -3)
    if [ -n "$CAPTAIN_CONTENT" ]; then
        echo "✅ Captain 관련 내용 발견:"
        echo "$CAPTAIN_CONTENT"
    else
        echo "⚠️ Captain 관련 내용 없음 (UI 주입 확인 필요)"
    fi
fi

# 3. index.html 수정 확인
echo ""
echo "3. index.html 수정 확인..."
INDEX_PATHS=(
    "/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/frontend/index.html"
    "/home/hakkocap/.openclaw/workspace/langflow_dir/langflow/frontend/index.html"
)

for INDEX_PATH in "${INDEX_PATHS[@]}"; do
    if [ -f "$INDEX_PATH" ]; then
        echo "✅ index.html 발견: $INDEX_PATH"
        INJECTION_COUNT=$(grep -i "captain\|board\|inject\|swp" "$INDEX_PATH" | wc -l)
        echo "   주입된 내용 라인 수: $INJECTION_COUNT"
        if [ $INJECTION_COUNT -gt 0 ]; then
            echo "   ✅ UI 주입 확인됨"
            # 샘플 라인 출력
            grep -i "captain\|board\|inject\|swp" "$INDEX_PATH" | head -2
        else
            echo "   ⚠️ UI 주입 내용 없음"
        fi
        break
    fi
done

# 4. 데모 접속 정보
echo ""
echo "4. 데모 접속 정보"
echo "URL: http://localhost:7860"
echo "확인 요소: 우측 상단 'Captain's Board' 팝업 UI"
echo "예상 내용: 상벌점 게이지, 스웜 효율 98%"
echo ""
echo "5. 확인 방법"
echo "1. 브라우저에서 http://localhost:7860 접속"
echo "2. 페이지 우측 상단 확인"
echo "3. 'Captain's Board' 또는 유사 UI 찾기"
echo "4. 상벌점 게이지 및 효율 표시 확인"

# 6. 상태 요약
echo ""
echo "=== 상태 요약 ==="
echo "서버 상태: $SERVER_STATUS"
echo "UI 주입: $(if [ $INJECTION_COUNT -gt 0 2>/dev/null ]; then echo "확인됨"; else echo "미확인"; fi)"
echo "데모 준비: $(if [ "$SERVER_STATUS" = "running" ] && [ $INJECTION_COUNT -gt 0 2>/dev/null ]; then echo "✅ 준비 완료"; else echo "⚠️ 준비 중"; fi)"
echo "캡틴 확인: 브라우저에서 직접 접속 권장"
