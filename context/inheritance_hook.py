#!/usr/bin/env python3
"""
SWP Context Inheritance Hook
하위 에이전트는 이를 Pre-Task로 실행해야 함
"""
import json
import sys
from pathlib import Path

CONTEXT_PATH = Path("/home/hakkocap/캡틴스룸/Context_Bridge/current_context.json")

def inherit_context():
    """캡틴의 맥락을 로드하고 에이전트 페르소나에 주입"""
    if not CONTEXT_PATH.exists():
        print("[WARN] Context snapshot not found. Running with defaults.")
        return None
    
    with open(CONTEXT_PATH, 'r', encoding='utf-8') as f:
        ctx = json.load(f)
    
    # Extract key context for agents
    persona = {
        "role": "부관 ( deputy/first officer )",
        "crew": "하꼬 해적단",
        "captain": "D.Piddy (데피디)",
        "tone": ctx.get("captain_preferences", {}).get("tone", "default"),
        "report_style": ctx.get("captain_preferences", {}).get("report_style", "default"),
        "current_mission": ctx.get("current_mission", {}).get("primary", "None"),
        "verification_required": ctx.get("swp_compliance", {}).get("anti_hallucination", False),
        "memory_refs": ctx.get("memory_reference", {})
    }
    
    return ctx, persona

def apply_to_prompt(base_prompt: str, persona: dict) -> str:
    """프롬프트에 캡틴 스타일 주입"""
    style_prefix = f"""[SWP Context Injected]
당신은 {persona['crew']}의 {persona['role']}입니다.
캡틴: {persona['captain']}
현재 임무: {persona['current_mission']}
보고 방식: {persona['report_style']}

{base_prompt}

**필수 준수:** Anti-Hallucination 검증 수행 후 결과 보고.
"""
    return style_prefix

if __name__ == "__main__":
    ctx, persona = inherit_context()
    
    if ctx:
        print(f"[CONTEXT LOADED] Snapshot: {ctx.get('snapshot_id', 'N/A')}")
        print(f"[PERSONA] {persona['role']} of {persona['crew']}")
        print(f"[MISSION] {persona['current_mission']}")
        print(f"[STYLE] {persona['tone']}")
        sys.exit(0)
    else:
        print("[ERROR] Context inheritance failed")
        sys.exit(1)
