#!/usr/bin/env python3
"""
hook_manual.py - 거짓말 금지 훅 (Anti-Hallucination Hook)
所有 보고 전 물리적 수치 검증
"""
import os
import re
import subprocess
from datetime import datetime

# 설정
TARGET_DIR = "/home/hakkocap/essence_of_humanity/"
LOG_FILE = "/home/hakkocap/.openclaw/workspace/logs/swp_essence.log"

# 거짓말 검증 통계
STATS_FILE = "/home/hakkocap/.openclaw/workspace/data/hallucination_stats.json"

def load_stats():
    """통계 로드"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return eval(f.read())
    return {"success": 0, "blocked": 0, "mute_until": None}

def save_stats(stats):
    """통계 저장"""
    with open(STATS_FILE, 'w') as f:
        f.write(str(stats))

def check_mute_status():
    """강제 침묵 상태 확인"""
    stats = load_stats()
    if stats["mute_until"]:
        import time
        if time.time() < stats["mute_until"]:
            remaining = int(stats["mute_until"] - time.time())
            print(f"[🚫 MUTED] 거짓말 누적 3회 - {remaining}초간 침묵 중")
            return True
        else:
            stats["mute_until"] = None
            save_stats(stats)
    return False

def get_physical_numbers():
    """물리적 수치 실제 조회"""
    numbers = {}
    
    # 1. NVMe 용량 조회
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 4:
                numbers['nvme_total'] = parts[1]
                numbers['nvme_used'] = parts[2]
                numbers['nvme_available'] = parts[3]
                # GB 숫자 추출
                avail_match = re.search(r'(\d+)', numbers['nvme_available'])
                if avail_match:
                    numbers['nvme_avail_gb'] = int(avail_match.group(1))
    except Exception as e:
        numbers['nvme_error'] = str(e)
    
    # 2. 프로세스 개수 조회
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=5)
        numbers['process_count'] = len(result.stdout.strip().split('\n')) - 1
    except Exception as e:
        numbers['process_error'] = str(e)
    
    # 3. 메모리 조회
    try:
        result = subprocess.run(['free', '-h'], capture_output=True, text=True, timeout=5)
        numbers['memory_info'] = result.stdout
    except Exception as e:
        numbers['memory_error'] = str(e)
    
    return numbers

def verify_claim(claim_text, physical_numbers):
    """주장 검증"""
    stats = load_stats()
    
    # 탐지할 패턴들
    patterns = [
        (r'(\d+)\s*(TB|GB)', 'storage'),
        (r'(\d+)\s*프로세스', 'process'),
        (r'PID\s*(\d+)', 'pid'),
    ]
    
    errors = []
    
    for pattern, ptype in patterns:
        matches = re.findall(pattern, claim_text, re.IGNORECASE)
        for match in matches:
            value = int(match[0]) if match[0].isdigit() else 0
            
            if ptype == 'storage':
                # NVMe 가용 용량과 비교
                if 'nvme_avail_gb' in physical_numbers:
                    actual = physical_numbers['nvme_avail_gb']
                    if 'TB' in claim_text.upper():
                        # TB 단위면 1000倍以上
                        actual_tb = actual / 1000
                        if value > actual_tb * 1.01:  # 1% 오차
                            errors.append(f"용량 과대 주장: {value}TB vs 실제 {actual}GB")
                    elif value > actual * 1.01:
                        errors.append(f"용량 과대 주장: {value}GB vs 실제 {actual}GB")
            
            elif ptype == 'process':
                if 'process_count' in physical_numbers:
                    actual = physical_numbers['process_count']
                    if abs(value - actual) > actual * 0.01:  # 1% 오차
                        errors.append(f"프로세스 수 과대 주장: {value} vs 실제 {actual}")
    
    return errors

def log_blocked(blocked_info):
    """차단 기록"""
    stats = load_stats()
    stats["blocked"] += 1
    save_stats(stats)
    
    # 3회 누적 시 강제 침묵
    if stats["blocked"] >= 3:
        import time
        stats["mute_until"] = time.time() + 300  # 5분
        save_stats(stats)
        print(f"[🚫 MUTED] 3회 누적 - 5분간 침묵 처분")
    
    # 로그에 기록
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [거짓말 차단] {blocked_info}\n")

# 메인 실행
print('[HOOK] 시스템 컨텍스트 스캔 중...')

# 침묵 상태 확인
if check_mute_status():
    print("[🚫 HOOK BLOCKED] 강제 침묵 중 - 어떤 보고도 불가")
    exit(1)

# 물리적 수치 조회
physical_numbers = get_physical_numbers()

# 보고할 내용을 검증 (여기서는 스캔 결과)
if os.path.isdir(TARGET_DIR):
    try:
        files = os.listdir(TARGET_DIR)
        if files:
            file_count = len(files)
            print(f"Found files in {TARGET_DIR}:")
            for file_name in files:
                print(f"- {file_name}")
            
            # 수치 검증
            claim = f"{file_count}개 파일"
            errors = verify_claim(claim, physical_numbers)
            
            if errors:
                for err in errors:
                    print(f"[⚠️ 경고] {err}")
                    log_blocked(err)
            
            stats = load_stats()
            stats["success"] += 1
            save_stats(stats)
            
        else:
            print(f"Directory {TARGET_DIR} is empty.")
        print('[HOOK] 시스템 컨텍스트 스캔 완료. 정상.')
        
    except Exception as e:
        print(f'[HOOK] Error scanning directory {target_dir}: {e}')
else:
    print(f'[HOOK] Directory not found: {target_dir}')
    print('[HOOK] 시스템 컨텍스트 스캔 중... 오류 발생.')

# 검증 통계 출력
stats = load_stats()
print(f"[📊 검증 통계] 성공: {stats['success']}회 / 차단: {stats['blocked']}회")
