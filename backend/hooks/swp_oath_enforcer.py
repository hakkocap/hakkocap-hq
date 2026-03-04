#!/usr/bin/env python3
"""
SWP-007 Oath Enforcement Hook
선서 강제 검증 시스템
"""

import re
from typing import Dict, Any

class OathEnforcer:
    """
    [SWP 프로토콜 준수] + 선서 강제
    """
    
    REQUIRED_OATHS = [
        "[Single-Message Enforcement]",
        "[Zero-Intermediate]", 
        "[Pre-Computation Complete]",
        "[Hallucination-Ready]",
        "[Validation-Gate Passed]"
    ]
    
    @staticmethod
    def enforce_oath(content: str, source_files_verified: Dict[str, bool] = None) -> Dict[str, Any]:
        """
        선서 검증 핵심 훅
        """
        result = {
            "valid": False,
            "violations": [],
            "enforced_content": content
        }
        
        # 1. SWP 헤더 확인
        if "[SWP 프로토콜 준수]" not in content:
            result["violations"].append("Missing [SWP 프로토콜 준수] header")
            return result
        
        # 2. 선서 확인
        for oath in OathEnforcer.REQUIRED_OATHS:
            if oath not in content:
                result["violations"].append(f"Missing oath: {oath}")
        
        # 2. Validation-Gate: 파일 생성 주장 검증
        if source_files_verified:
            for path, exists in source_files_verified.items():
                if not exists:
                    result["violations"].append(f"Claimed file does not exist: {path}")
        
        # 4. Hallucination 자백 확인
        if "[Hallucination-Ready]" in content:
            if "할루시네이션" not in content.lower() and "hallucination" not in content.lower():
                # Hallucination-ready지만 내용 없음 = 형식적 준수
                result["violations"].append("[Hallucination-Ready] without actual confession")
        
        result["valid"] = len(result["violations"]) == 0
        
        if not result["valid"]:
            # 위반 시 예외 발생
            raise NoOathError(f"SWP-007 Violation: {result['violations']}")
        
        return result
    
    @staticmethod
    def generate_oath_template() -> str:
        """
        표준 선서 템플릿
        """
        return """
[SWP 프로토콜 준수]

[Single-Message Enforcement]: 본 메시지 하나만 전송
[Zero-Intermediate]: 중간 메시지 0개
[Pre-Computation Complete]: 모든 처리 선행 완료
[Hallucination-Ready]: 환각 발견 시 즉시 자백
[Validation-Gate Passed]: 파일 생성 주장 검증 완료

---
[최종 보고서 내용]
"""

class NoOathError(Exception):
    """선서 누락 예외"""
    pass

# Decorator for enforcement
def swp_oath_required(func):
    """
    함수 래퍼: 선서 필수
    """
    def wrapper(*args, **kwargs):
        content = kwargs.get('content') or (args[0] if args else "")
        
        # 선서 검증
        enforcer = OathEnforcer()
        try:
            enforcer.enforce_oath(content, kwargs.get('verified_files', {}))
        except NoOathError as e:
            # 예외: 선서 없음
            raise e
        
        return func(*args, **kwargs)
    return wrapper

# SWP-007 SILENT_REPORT_RULE (with oath enforcement)
SILENT_REPORT_RULE = """
[CRITICAL] Single-Report Enforcement:
- [SWP 프로토콜 준수] + 5개 선서 필수
- 하나의 완전한 메시지만 출력
- 모든 중간 확인 생략
- 검증 실패 시 NoOathError 발생

[CRITICAL] Oath Checklist:
□ Single-Message Enforcement
□ Zero-Intermediate  
□ Pre-Computation Complete
□ Hallucination-Ready
□ Validation-Gate Passed

[CRITICAL] 형식적 준수 ≠ 실질적 준수:
- 헤더만 있는 것: 위반
- 헤더 + 선서 + 검증: 완전 준수
"""

# Apply to deputy
if __name__ == "__main__":
    # Test
    test_content = """
[SWP 프로토콜 준수]
[Single-Message Enforcement]
[Zero-Intermediate]
[Pre-Computation Complete]
[Hallucination-Ready]
[Validation-Gate Passed]
    """
    enforcer = OathEnforcer()
    try:
        result = enforcer.enforce_oath(test_content)
        print(f"Valid: {result['valid']}")
    except NoOathError as e:
        print(f"Enforced: {e}")
