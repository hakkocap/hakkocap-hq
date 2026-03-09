#!/bin/bash
# SWP 프로젝트 안전 업로드 스크립트
set -e  # 에러 발생 시 스크립트 중단

echo "=== SWP 프로젝트 GitHub 업로드 시작 ==="
echo "시간: $(date)"
echo ""

# 작업 디렉토리 확인
cd /tmp/swp_upload_to_github || { echo "디렉토리 없음"; exit 1; }

# Git 저장소 초기화 (이미 있으면 스킵)
if [ ! -d .git ]; then
    echo "1. Git 저장소 초기화..."
    git init
    git config user.email "hakkocap@openclaw-ai"
    git config user.name "hakkocap"
else
    echo "1. 기존 Git 저장소 사용"
fi

# 파일 추가
echo "2. 파일 추가..."
git add .

# 커밋 생성
echo "3. 커밋 생성..."
git commit -m "SWP 프로젝트 스마트 백업 v1.0

- 통합 대시보드: integrated_dashboard_v4.py
- 나노봇 실험실: nanobot_lab_consensus.py
- Sovereign Memory: ghost_memory_core.py
- ZeroMQ 통신: openy_node.py
- 총 파일: 93개, 용량: 528KB
- 백업 일시: $(date '+%Y-%m-%d %H:%M:%S KST')" || echo "커밋 실패 (변경사항 없음)"

# 원격 저장소 설정
echo "4. 원격 저장소 설정..."
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:hakkocap/hakkocap-hq.git

# 업로드 실행
echo "5. GitHub 업로드 실행..."
echo "SSH 키 사용: $(ssh -T git@github.com 2>&1 | grep -o 'successfully authenticated' || echo '인증 확인 중')"

# 안전한 푸시 (force 없음)
if git push -u origin main 2>&1; then
    echo "✅ GitHub 업로드 성공!"
    echo "저장소 URL: https://github.com/hakkocap/hakkocap-hq"
else
    echo "⚠️ 일반 푸시 실패, 대체 방법 시도..."
    # 충돌 해결을 위한 안전한 방법
    git fetch origin
    git merge --allow-unrelated-histories -m "Merge SWP project" origin/main || true
    git push -u origin main && echo "✅ 대체 방법으로 업로드 성공!"
fi

echo ""
echo "=== 업로드 완료 ==="
