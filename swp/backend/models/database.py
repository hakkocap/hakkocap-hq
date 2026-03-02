"""
SWP Database Schema
Sovereign Workflow Protocol - Persistent Storage
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "swp.db"

def init_db():
    """Initialize all SWP tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # === SKILL MANUALS ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS skill_manuals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,  -- frontend, backend, database, devops, recon
            content TEXT NOT NULL,
            keywords TEXT,           -- comma-separated trigger keywords
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # === TASKS & EXECUTION ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            intent_keywords TEXT,    -- parsed from Captain's intent
            status TEXT DEFAULT 'pending',  -- pending, in_progress, verification, correcting, completed, failed
            skill_manual_id INTEGER REFERENCES skill_manuals(id),
            checklist TEXT,          -- JSON array of checklist items
            execution_log TEXT,       -- JSON array of execution steps
            errors TEXT,              -- JSON array of errors encountered
            rca_log TEXT,             -- Root Cause Analysis log
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    # === THREE-TIER MEMORY ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS memory_tier1_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            title TEXT NOT NULL,
            plan_content TEXT NOT NULL,
            phase TEXT,              -- planning, execution, verification
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS memory_tier2_context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            context_key TEXT NOT NULL,
            context_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS memory_tier3_checklists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            checklist_item TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            order_index INTEGER DEFAULT 0
        )
    ''')
    
    # === DISCIPLINARY LEDGER ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS disciplinary_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER REFERENCES tasks(id),
            error_type TEXT NOT NULL,
            error_message TEXT,
            root_cause TEXT,
            correction_action TEXT,
            resolved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # === PATTERN RECOGNITION ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS execution_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT NOT NULL,  -- scraping, coding, recon, analysis
            avg_duration_minutes REAL,
            success_rate REAL,
            common_errors TEXT,          -- JSON array
            optimization_hints TEXT,      -- JSON array
            execution_count INTEGER DEFAULT 0,
            last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # === EXECUTION STATE ===
    c.execute('''
        CREATE TABLE IF NOT EXISTS execution_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER UNIQUE REFERENCES tasks(id),
            current_step TEXT,
            step_index INTEGER DEFAULT 0,
            last_resume_point TEXT,
            is_paused BOOLEAN DEFAULT 0,
            last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ SWP Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
