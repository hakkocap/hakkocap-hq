import os
import json
import subprocess
from datetime import datetime

# SWP v3.0: Anti-Hallucination Audit Core
SWP_BASE = "/home/hakkocap/다운로드/swp"
STATS_FILE = f"{SWP_BASE}/context/hallucination_stats.json"

def get_physical_proof(commands):
    """
    강제 신뢰 시스템: AI의 설명이 아닌 시스템 명령어의 날것 그대로를 수집
    """
    proofs = {}
    for cmd in commands:
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            proofs[cmd] = result.strip()
        except Exception as e:
            proofs[cmd] = f"ERROR: {str(e)}"
    return proofs

def verify_report_integrity(report_data):
    """
    나노봇 교차 감사 (Cross-Audit) 시뮬레이션
    실제 파일 존재 여부, PID 활성 상태 등을 체크하여 [NA✓] 부여 결정
    """
    # 1. 파일 경로 체크
    for path in report_data.get('paths', []):
        if not os.path.exists(path):
            return False, f"Path not found: {path}"
    
    # 2. 프로세스 체크
    for pid in report_data.get('pids', []):
        try:
            subprocess.check_call(f"ps -p {pid}", shell=True, stdout=subprocess.DEVNULL)
        except:
            return False, f"PID not active: {pid}"
            
    return True, "Verified by Nanobot Legion [NA✓]"

def update_hallucination_stats(is_error):
    """
    할루시네이션 벌점제 기록
    """
    if not os.path.exists(STATS_FILE):
        stats = {"total_reports": 0, "hallucinations": 0, "score": 100}
    else:
        with open(STATS_FILE, 'r') as f:
            stats = json.load(f)
            
    stats["total_reports"] += 1
    if is_error:
        stats["hallucinations"] += 1
        stats["score"] -= 10
        
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    return stats

if __name__ == "__main__":
    # 초기화 및 테스트
    print("SWP v3.0 Anti-Hallucination Core Initialized.")
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    update_hallucination_stats(False)
