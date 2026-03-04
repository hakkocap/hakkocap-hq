#!/usr/bin/env python3
"""
SWP Task Auto-Resume System
작업 재개 시 자동으로 3개 문서 읽고 중단 지점부터 시작
"""

import os
import json
from pathlib import Path

class TaskResumer:
    """
    TASK 자동 복구 시스템
    """
    
    SWP_DATA_DIR = Path("/home/hakkocap/다운로드/swp/data")
    
    @staticmethod
    def find_task_files(task_name: str):
        """
        특정 TASK의 3개 문서 경로 반환
        예: task_name = "AntiHallucination"
        """
        return {
            "task": TaskResumer.SWP_DATA_DIR / f"TASK_{task_name}.md",
            "context": TaskResumer.SWP_DATA_DIR / f"CONTEXT_{task_name}.md",
            "checklist": TaskResumer.SWP_DATA_DIR / f"CHECKLIST_{task_name}.md"
        }
    
    @staticmethod
    def read_task_plan(task_name: str) -> dict:
        """
        TASK 계획서 읽기
        Returns: {
            "tasks": [...],
            "current_status": {...},
            "next_checkpoint": "..."
        }
        """
        files = TaskResumer.find_task_files(task_name)
        
        if not files["task"].exists():
            raise FileNotFoundError(f"TASK_{task_name}.md not found")
        
        with open(files["task"], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 매트릭스 파싱 (간단 버전)
        result = {
            "raw_content": content,
            "tasks": [],
            "file_path": str(files["task"])
        }
        
        return result
    
    @staticmethod
    def read_context(task_name: str) -> dict:
        """
        맥락노트 읽기
        Returns: {
            "completed": [...],
            "in_progress": [...],
            "interrupted_at": "...",
            "next_steps": [...]
        }
        """
        files = TaskResumer.find_task_files(task_name)
        
        if not files["context"].exists():
            return {"error": "Context file not found"}
        
        with open(files["context"], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 중단 지점 추출
        result = {
            "raw_content": content,
            "file_path": str(files["context"])
        }
        
        # "중단 지점" 섹션 파싱
        if "## 중단 지점" in content:
            lines = content.split("## 중단 지점")[1].split("##")[0].strip()
            result["interrupted_at"] = lines
        else:
            result["interrupted_at"] = "없음"
        
        return result
    
    @staticmethod
    def read_checklist(task_name: str) -> dict:
        """
        체크리스트 읽기
        Returns: {
            "total_items": 100,
            "completed": 10,
            "next_item": "AH-003: 캡틴 진술 우선권 구현"
        }
        """
        files = TaskResumer.find_task_files(task_name)
        
        if not files["checklist"].exists():
            return {"error": "Checklist file not found"}
        
        with open(files["checklist"], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 체크박스 파싱
        total = content.count("- [ ]") + content.count("- [x]")
        completed = content.count("- [x]")
        
        result = {
            "raw_content": content,
            "file_path": str(files["checklist"]),
            "total_items": total,
            "completed": completed,
            "progress_percent": round(completed / total * 100, 1) if total > 0 else 0
        }
        
        return result
    
    @staticmethod
    def auto_resume(task_name: str) -> str:
        """
        3개 문서 읽고 요약 생성
        """
        print(f"[TaskResumer] 작업 '{task_name}' 복구 중...")
        
        # 1. TASK 계획서
        task_plan = TaskResumer.read_task_plan(task_name)
        print(f"✓ TASK 계획서 로드: {task_plan['file_path']}")
        
        # 2. 맥락노트
        context = TaskResumer.read_context(task_name)
        print(f"✓ 맥락노트 로드: {context['file_path']}")
        print(f"  중단 지점: {context['interrupted_at']}")
        
        # 3. 체크리스트
        checklist = TaskResumer.read_checklist(task_name)
        print(f"✓ 체크리스트 로드: {checklist['file_path']}")
        print(f"  진행률: {checklist['completed']}/{checklist['total_items']} ({checklist['progress_percent']}%)")
        
        # 요약 생성
        summary = f"""
[TaskResumer] 작업 복구 완료

📋 TASK: {task_name}
📂 파일:
  - 계획서: {task_plan['file_path']}
  - 맥락: {context['file_path']}
  - 체크리스트: {checklist['file_path']}

🔄 진행 상황:
  - 완료: {checklist['completed']}/{checklist['total_items']} ({checklist['progress_percent']}%)
  - 중단 지점: {context['interrupted_at']}

📌 다음 단계:
  맥락노트의 "다음 단계" 섹션 참조
"""
        return summary

# CLI 사용 예시
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python task_resumer.py <TaskName>")
        print("Example: python task_resumer.py AntiHallucination")
        sys.exit(1)
    
    task_name = sys.argv[1]
    summary = TaskResumer.auto_resume(task_name)
    print(summary)
