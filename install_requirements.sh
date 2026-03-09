#!/bin/bash
# Sovereign Memory Fortress 필수 라이브러리 설치 스크립트

echo "=== Sovereign Memory Fortress 필수 라이브러리 설치 ==="
echo "시작 시간: $(date)"
echo ""

# 1. 기본 패키지 업데이트
echo "1. 기본 패키지 업데이트..."
pip install --upgrade pip setuptools wheel

# 2. 핵심 라이브러리 설치
echo ""
echo "2. 핵심 라이브러리 설치..."
echo "2.1 sentence-transformers (한국어 임베딩 모델)..."
pip install sentence-transformers

echo ""
echo "2.2 streamlit (대시보드)..."
pip install streamlit

echo ""
echo "2.3 데이터 처리 라이브러리..."
pip install numpy pandas sqlite-utils

echo ""
echo "2.4 시각화 라이브러리..."
pip install plotly networkx matplotlib

echo ""
echo "2.5 기타 유틸리티..."
pip install requests python-dotenv

# 3. 설치 확인
echo ""
echo "3. 설치 확인..."
echo "sentence-transformers: $(python3 -c "import sentence_transformers; print('✅')" 2>/dev/null || echo '❌')"
echo "streamlit: $(python3 -c "import streamlit; print('✅')" 2>/dev/null || echo '❌')"
echo "numpy: $(python3 -c "import numpy; print('✅')" 2>/dev/null || echo '❌')"
echo "plotly: $(python3 -c "import plotly; print('✅')" 2>/dev/null || echo '❌')"

echo ""
echo "=== 설치 완료 ==="
echo "설치된 패키지 목록:"
pip list | grep -E "(sentence|streamlit|numpy|pandas|plotly|networkx)"
