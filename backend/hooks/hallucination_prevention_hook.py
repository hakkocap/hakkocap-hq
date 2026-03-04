# HALUCINATION_PREVENTION_HOOK.py
## 파일 생성 자동 검증 시스템

import os
from pathlib import Path

class FileCreationValidator:
    """
    SWP-008: 파일 생성 주장 자동 검증
    - write/edit 후 반드시 존재 확인
    - 사이즈/라인수 주장 시 실제 검증
    """
    
    REQUIRED_PATHS = [
        "/home/hakkocap/캡틴스룸/인간의_정수/",
        "/home/hakkocap/hakkocap-hq/docs/",
        "/home/hakkocap/.openclaw/workspace/"
    ]
    
    @staticmethod
    def verify_file_created(claimed_path: str, claimed_size: int = None, claimed_lines: int = None) -> dict:
        """
        파일 생성 주장 검증
        Returns: {"valid": bool, "actual": {}, "discrepancy": str}
        """
        result = {"valid": False, "actual": {}, "discrepancy": None}
        
        # 1. 존재 확인
        if not os.path.exists(claimed_path):
            result["discrepancy"] = f"File does not exist: {claimed_path}"
            return result
        
        result["actual"]["exists"] = True
        
        # 2. 사이즈 검증
        actual_size = os.path.getsize(claimed_path)
        result["actual"]["size_bytes"] = actual_size
        
        if claimed_size and abs(actual_size - claimed_size) > 100:
            result["discrepancy"] = f"Size mismatch: claimed {claimed_size}, actual {actual_size}"
            return result
        
        # 3. 라인 수 검증
        if claimed_lines:
            with open(claimed_path, 'r', encoding='utf-8') as f:
                actual_lines = sum(1 for _ in f)
            result["actual"]["lines"] = actual_lines
            
            if abs(actual_lines - claimed_lines) > 5:
                result["discrepancy"] = f"Lines mismatch: claimed {claimed_lines}, actual {actual_lines}"
                return result
        
        result["valid"] = True
        return result
    
    @staticmethod
    def pre_report_hook():
        """
        모든 보고 전 실행: 미확인 주장이 있는지 스캔
        """
        unchecked_claims = []
        # 메모리 내 주장 추적 (구현 필요)
        return len(unchecked_claims) == 0

# SWP 통합용 데코레이터
def verified_file_creation(func):
    """
    파일 생성 함수 래퍼
    - 생성 후 자동 검증
    - 불일치 시 예외 발생
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # 경로 추출 (kwargs['path'] 또는 args[0])
        path = kwargs.get('path') or (args[0] if args else None)
        if path:
            validation = FileCreationValidator.verify_file_created(path)
            if not validation["valid"]:
                raise HallucinationError(f"FILE CREATION FAILED: {validation['discrepancy']}")
        return result
    return wrapper

class HallucinationError(Exception):
    """환각 검증 실패 예외"""
    pass
