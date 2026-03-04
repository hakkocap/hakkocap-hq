#!/usr/bin/env python3
"""
SWP Copilot Interface Module
GitHub Copilot CLI 연동 후크
"""
import subprocess
import json
from typing import List, Tuple
from pathlib import Path

COPILOT_CMDS = {
    "explain": "gh copilot explain",
    "suggest": "gh copilot suggest",
}

class CopilotInterface:
    """Copilot 연동 인터페이스"""
    
    @staticmethod
    def explain_code(code_snippet: str, language: str = "python") -> str:
        """코드 설명 요청"""
        try:
            cmd = f"{COPILOT_CMDS['explain']} '{code_snippet}'"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"[Copilot Error] {e}"
    
    @staticmethod
    def suggest_inline(prompt: str, target_file: str = None) -> str:
        """인라인 코드 제안"""
        try:
            flags = "-t shell" if target_file else "-t shell"
            cmd = f"echo '{prompt}' | {COPILOT_CMDS['suggest']} {flags}"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.stdout.strip() if result.returncode == 0 else ""
        except Exception as e:
            return f"[Copilot Error] {e}"
    
    @staticmethod
    def audit_with_copilot(code: str) -> Tuple[bool, str]:
        """Self-Audit with Copilot review"""
        explanation = CopilotInterface.explain_code(code[:500], "python")
        has_issues = "error" in explanation.lower() or "bug" in explanation.lower()
        return not has_issues, explanation

# SWP 호환 인터페이스
def copilot_explain(code: str, lang: str = "python") -> str:
    """SWP 호크 포맷"""
    return CopilotInterface.explain_code(code, lang)

def copilot_suggest(prompt: str) -> str:
    """코드 제안"""
    return CopilotInterface.suggest_inline(prompt)

def copilot_audit(code: str) -> str:
    """코드 감사"""
    passed, feedback = CopilotInterface.audit_with_copilot(code)
    return f"[AUDIT {'PASS' if passed else 'REVIEW NEEDED'}]\n{feedback}"

if __name__ == "__main__":
    # Demo: Fibonacci with Copilot
    test_code = "def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)"
    print("=== Copilot Explanation ===")
    print(copilot_explain(test_code))
    print("\n=== Copilot Audit ===")
    print(copilot_audit(test_code))
