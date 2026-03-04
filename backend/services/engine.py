"""
SWP Core Engine
Sovereign Workflow Protocol - Execution Engine
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from models.database import DB_PATH, init_db
import sqlite3

# === KEYWORD INTENT PARSER ===
INTENT_KEYWORDS = {
    "coding": ["code", "build", "create", "implement", "script", "function", "api", "debug"],
    "scraping": ["scrape", "crawl", "extract", "collect", "fetch", "parse", "download"],
    "recon": ["reconnaissance", "scan", "investigate", "analyze", "research", "find"],
    "deployment": ["deploy", "release", "publish", "launch", "serve", "host"],
    "database": ["database", "db", "query", "migrate", "schema", "sql"],
    "frontend": ["ui", "interface", "web", "page", "component", "react", "vue"],
    "backend": ["server", "api", "service", "endpoint", "backend", "logic"],
}



# === SWP-005: ANTI-HALLUCINATION VERIFICATION HOOK ===
VERIFICATION_PROTOCOLS = {
    "api_key_check": {
        "description": "API 키 존재 여부 확인",
        "source_of_truth": "/home/hakkocap/.nanobot/config.json",  
        "method": "file_read",
    },
    "file_existence": {
        "description": "파일 존재 확인",
        "method": "ls_check",
    },
    "service_status": {
        "description": "서비스 상태 확인", 
        "method": "curl_health",
    }
}

class VerificationResult:
    """Triple-check verification result container"""
    def __init__(self):
        self.fact_checked = False
        self.path_verified = False
        self.confidence = "unknown"  # verified / inferred / unknown
    
    def to_dict(self):
        return {
            "fact_checked": self.fact_checked,
            "path_verified": self.path_verified,
            "confidence": self.confidence
        }

class SWPEngine:
    """Sovereign Workflow Protocol Execution Engine"""
    
    def __init__(self):
        init_db()
        self.db_path = DB_PATH
    
    # === PRE-TASK HOOK: LOAD SKILL MANUAL ===
    def load_skill_manual(self, task_description: str) -> Optional[Dict]:
        """Find and load relevant skill manual based on keywords."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Find matching keywords
        matched_category = None
        for category, keywords in INTENT_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in task_description.lower():
                    matched_category = category
                    break
            if matched_category:
                break
        
        # Load manual if exists
        if matched_category:
            c.execute(
                "SELECT * FROM skill_manuals WHERE category = ? ORDER BY updated_at DESC LIMIT 1",
                (matched_category,)
            )
            row = c.fetchone()
            if row:
                manual = dict(row)
                conn.close()
                return manual
        
        conn.close()
        return None
    
    # === INTENT PARSER: GENERATE CHECKLIST ===
    def parse_intent(self, captain_intent: str) -> Dict[str, Any]:
        """Parse Captain's intent and generate dynamic checklist."""
        intent_lower = captain_intent.lower()
        
        # Detect task type
        task_type = "general"
        for category, keywords in INTENT_KEYWORDS.items():
            if any(kw in intent_lower for kw in keywords):
                task_type = category
                break
        
        # Generate base checklist by type
        base_checklists = {
            "coding": [
                "Read relevant Skill Manual",
                "Verify requirements & acceptance criteria",
                "Set up development environment",
                "Write core logic",
                "Add error handling",
                "Write unit tests",
                "Verify implementation against requirements"
            ],
            "scraping": [
                "Read relevant Skill Manual",
                "Identify target URL structure",
                "Check robots.txt compliance",
                "Implement rate limiting",
                "Handle edge cases & errors",
                "Store data in required format",
                "Verify data integrity"
            ],
            "recon": [
                "Read relevant Skill Manual",
                "Define reconnaissance scope",
                "Gather OSINT sources",
                "Document findings",
                "Cross-verify information"
            ],
            "deployment": [
                "Read relevant Skill Manual",
                "Verify build passes tests",
                "Check environment variables",
                "Execute deployment",
                "Verify health endpoints",
                "Monitor logs for errors"
            ],
            "general": [
                "Read relevant Skill Manual",
                "Analyze requirements",
                "Execute task",
                "Verify output",
                "Report completion"
            ]
        }
        
        return {
            "task_type": task_type,
            "checklist": base_checklists.get(task_type, base_checklists["general"]),
            "detected_keywords": [kw for kw, words in INTENT_KEYWORDS.items() 
                                 if any(w in intent_lower for w in words)]
        }
    
    # === POST-TASK VERIFICATION HOOK ===
    def verify_task(self, task_id: int, output: str) -> Dict[str, Any]:
        """Mandatory verification step - anti-hallucination."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = dict(c.fetchone())
        
        verification_results = {
            "task_id": task_id,
            "verified": True,
            "warnings": [],
            "errors": []
        }
        
        # Check 1: Is output empty?
        if not output or len(output.strip()) < 10:
            verification_results["verified"] = False
            verification_results["errors"].append("Output is empty or too short")
        
        # Check 2: Does output match task description?
        if task.get("description"):
            task_words = set(task["description"].lower().split())
            output_words = set(output.lower().split())
            overlap = len(task_words & output_words)
            if overlap < 3:
                verification_results["warnings"].append(
                    f"Low keyword overlap between task and output ({overlap} matches)"
                )
        
        # Check 3: Error indicators in output
        error_indicators = ["error", "failed", "exception", "traceback", "cannot", "unable"]
        found_errors = [w for w in error_indicators if w in output.lower()]
        if found_errors:
            verification_results["warnings"].append(f"Potential errors detected: {found_errors}")
        
        # Update task status
        new_status = "completed" if verification_results["verified"] else "verification"
        c.execute(
            "UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, datetime.now().isoformat(), task_id)
        )
        conn.commit()
        conn.close()
        
        return verification_results
    
    # === SELF-AUDIT & RCA ===
    def perform_rca(self, task_id: int, error_message: str) -> Dict[str, Any]:
        """Root Cause Analysis when errors detected."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Analyze error patterns
        root_cause = "unknown"
        correction = ""
        
        error_lower = error_message.lower()
        
        if "timeout" in error_lower or "connection" in error_lower:
            root_cause = "Network/Connectivity Issue"
            correction = "Add retry logic with exponential backoff"
        elif "permission" in error_lower or "access denied" in error_lower:
            root_cause = "Permission/Access Issue"
            correction = "Verify credentials and access rights"
        elif "syntax" in error_lower or "parse" in error_lower:
            root_cause = "Syntax/Parse Error"
            correction = "Review code syntax and input format"
        elif "memory" in error_lower or "resource" in error_lower:
            root_cause = "Resource Exhaustion"
            correction = "Optimize memory usage, add limits"
        else:
            root_cause = "Unknown Error"
            correction = "Review logs for details"
        
        # Log to disciplinary ledger
        c.execute('''
            INSERT INTO disciplinary_ledger 
            (task_id, error_type, error_message, root_cause, correction_action)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, root_cause, error_message, root_cause, correction))
        
        # Update task status
        c.execute(
            "UPDATE tasks SET status = 'correcting', rca_log = ?, updated_at = ? WHERE id = ?",
            (json.dumps({"root_cause": root_cause, "correction": correction}),
             datetime.now().isoformat(), task_id)
        )
        
        conn.commit()
        conn.close()
        
        return {
            "task_id": task_id,
            "root_cause": root_cause,
            "correction": correction,
            "disciplinary_logged": True
        }
    
    # === THREE-TIER MEMORY ===
    def save_memory_tier1(self, task_id: int, title: str, plan_content: str, phase: str):
        """Save Project Plans."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO memory_tier1_plans (task_id, title, plan_content, phase)
            VALUES (?, ?, ?, ?)
        ''', (task_id, title, plan_content, phase))
        conn.commit()
        conn.close()
    
    def save_memory_tier2(self, task_id: int, context_key: str, context_value: str):
        """Save Context Notes."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO memory_tier2_context (task_id, context_key, context_value, updated_at)
            VALUES (?, ?, ?, ?)
        ''', (task_id, context_key, context_value, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def save_memory_tier3(self, task_id: int, checklist: List[str]):
        """Save Active Checklists."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM memory_tier3_checklists WHERE task_id = ?", (task_id,))
        for i, item in enumerate(checklist):
            c.execute('''
                INSERT INTO memory_tier3_checklists (task_id, checklist_item, order_index)
                VALUES (?, ?, ?)
            ''', (task_id, item, i))
        conn.commit()
        conn.close()
    
    def get_task_memory(self, task_id: int) -> Dict[str, Any]:
        """Load all three tiers for a task."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Tier 1: Plans
        c.execute("SELECT * FROM memory_tier1_plans WHERE task_id = ?", (task_id,))
        plans = [dict(r) for r in c.fetchall()]
        
        # Tier 2: Context
        c.execute("SELECT * FROM memory_tier2_context WHERE task_id = ?", (task_id,))
        context = {r["context_key"]: r["context_value"] for r in c.fetchall()}
        
        # Tier 3: Checklist
        c.execute("SELECT * FROM memory_tier3_checklists WHERE task_id = ? ORDER BY order_index", (task_id,))
        checklist = [{"item": r["checklist_item"], "completed": bool(r["completed"])} for r in c.fetchall()]
        
        conn.close()
        
        return {
            "tier1_plans": plans,
            "tier2_context": context,
            "tier3_checklist": checklist
        }
    
    # === STATE PERSISTENCE ===
    def save_execution_state(self, task_id: int, current_step: str, step_index: int):
        """Save pause point for resume."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO execution_state 
            (task_id, current_step, step_index, last_resume_point, last_heartbeat)
            VALUES (?, ?, ?, ?, ?)
        ''', (task_id, current_step, step_index, current_step, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def load_execution_state(self, task_id: int) -> Optional[Dict]:
        """Resume from last state."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM execution_state WHERE task_id = ?", (task_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None
    
    # === TASK MANAGEMENT ===
    def create_task(self, title: str, description: str) -> int:
        """Create new task with intent parsing."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        intent = self.parse_intent(description)
        checklist_json = json.dumps(intent["checklist"])
        keywords_json = ",".join(intent["detected_keywords"])
        
        c.execute('''
            INSERT INTO tasks (title, description, intent_keywords, checklist, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (title, description, keywords_json, checklist_json))
        
        task_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Save to memory tiers
        self.save_memory_tier3(task_id, intent["checklist"])
        
        return task_id
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get task details."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """List all tasks, optionally filtered by status."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if status:
            c.execute("SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC", (status,))
        else:
            c.execute("SELECT * FROM tasks ORDER BY created_at DESC")
        
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    # === SKILL MANUAL CRUD ===
    def add_skill_manual(self, name: str, category: str, content: str, keywords: str = "") -> int:
        """Add new skill manual."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO skill_manuals (name, category, content, keywords)
            VALUES (?, ?, ?, ?)
        ''', (name, category, content, keywords))
        manual_id = c.lastrowid
        conn.commit()
        conn.close()
        return manual_id
    
    def get_skill_manuals(self, category: Optional[str] = None) -> List[Dict]:
        """List skill manuals."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if category:
            c.execute("SELECT * FROM skill_manuals WHERE category = ?", (category,))
        else:
            c.execute("SELECT * FROM skill_manuals")
        
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    # === DISCIPLINARY LEDGER ===
    def get_disciplinary_records(self, task_id: Optional[int] = None) -> List[Dict]:
        """Get disciplinary records."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        if task_id:
            c.execute("SELECT * FROM disciplinary_ledger WHERE task_id = ?", (task_id,))
        else:
            c.execute("SELECT * FROM disciplinary_ledger ORDER BY created_at DESC")
        
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    
    # === PATTERN RECOGNITION ===
    def record_pattern(self, pattern_type: str, duration_minutes: float, success: bool, errors: List[str]):
        """Record execution pattern for optimization."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Update or insert pattern
        c.execute("SELECT * FROM execution_patterns WHERE pattern_type = ?", (pattern_type,))
        existing = c.fetchone()
        
        if existing:
            c.execute('''
                UPDATE execution_patterns 
                SET avg_duration_minutes = (avg_duration_minutes * execution_count + ?) / (execution_count + 1),
                    execution_count = execution_count + 1,
                    last_used = ?,
                    common_errors = ?
                WHERE pattern_type = ?
            ''', (duration_minutes, datetime.now().isoformat(), json.dumps(errors), pattern_type))
        else:
            c.execute('''
                INSERT INTO execution_patterns (pattern_type, avg_duration_minutes, success_rate, common_errors, execution_count)
                VALUES (?, ?, ?, ?, 1)
            ''', (pattern_type, duration_minutes, 1.0 if success else 0.0, json.dumps(errors)))
        
        conn.commit()
        conn.close()
    
    def get_optimization_hints(self, pattern_type: str) -> Optional[Dict]:
        """Get optimization hints based on past patterns."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM execution_patterns WHERE pattern_type = ?", (pattern_type,))
        row = c.fetchone()
        conn.close()
        return dict(row) if row else None
