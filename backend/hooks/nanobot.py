"""
SWP Hooks for Nanobot Integration
Pre-Task & Post-Task Mandatory Hooks
"""

import sys
from .services.engine import SWPEngine

# === PRE-TASK HOOK ===
def pre_task_hook(task_description: str) -> dict:
    """
    MANDATORY: Must be called before any Nanobot task execution.
    Loads relevant skill manual and prepares execution context.
    Also performs immutable command lookup to continue past contexts.
    """
    engine = SWPEngine()
    
    # 1. Load relevant skill manual
    manual = engine.load_skill_manual(task_description)
    
    # 2. Parse intent for checklist generation
    intent = engine.parse_intent(task_description)

    # 3. Lookup similar past immutable commands in Tier-3.
    import sqlite3
    db = engine.db_path
    conn = sqlite3.connect(db)
    c = conn.cursor()
    keyword = task_description.split()[0].lower() if task_description.strip() else ''
    c.execute("SELECT checklist_item FROM memory_tier3_checklists WHERE checklist_item LIKE ? LIMIT 5",('%'+keyword+'%',))
    past = [r[0] for r in c.fetchall()]
    conn.close()

    return {
        "hook": "pre_task",
        "skill_manual": manual,
        "intent": intent,
        "past_similar_commands": past,
        "status": "ready_to_execute"
    }

# === POST-TASK HOOK ===
def post_task_hook(task_id: int, output: str) -> dict:
    """
    MANDATORY: Must be called after task completion but before output finalization.
    Performs verification and self-audit.
    """
    engine = SWPEngine()
    
    # 1. Verification (anti-hallucination)
    verification = engine.verify_task(task_id, output)
    
    # 2. If verification fails, trigger RCA
    if not verification["verified"]:
        rca = {
            "requires_rca": True,
            "verification_result": verification
        }
    else:
        rca = {"requires_rca": False}
    
    return {
        "hook": "post_task",
        "verification": verification,
        "rca": rca,
        "status": "verified" if verification["verified"] else "needs_correction"
    }

# === ERROR HANDLING HOOK ===
def error_hook(task_id: int, error_message: str) -> dict:
    """
    Called when an error occurs during execution.
    Triggers Root Cause Analysis and self-correction.
    """
    engine = SWPEngine()
    
    # Perform RCA
    rca_result = engine.perform_rca(task_id, error_message)
    
    return {
        "hook": "error",
        "rca": rca_result,
        "status": "logged_to_ledger"
    }

# === STATE MANAGEMENT HOOKS ===
def save_state_hook(task_id: int, current_step: str, step_index: int):
    """Save execution state for long-running tasks."""
    engine = SWPEngine()
    engine.save_execution_state(task_id, current_step, step_index)

def resume_state_hook(task_id: int) -> dict:
    """Resume from last saved state."""
    engine = SWPEngine()
    state = engine.load_execution_state(task_id)
    if not state:
        return {"can_resume": False}
    return {
        "can_resume": True,
        "state": state
    }

# === USAGE EXAMPLE ===
if __name__ == "__main__":
    # Example workflow
    print("=== SWP Hooks Demo ===\n")
    
    # Pre-task
    print("1. Pre-Task Hook:")
    pre_result = pre_task_hook("Build a Python API with FastAPI")
    print(f"   Skill Manual: {pre_result['skill_manual'] is not None}")
    print(f"   Intent: {pre_result['intent']['task_type']}")
    print(f"   Checklist: {len(pre_result['intent']['checklist'])} items")
    
    # Create task in DB
    engine = SWPEngine()
    task_id = engine.create_task("Build API", "Build a Python API with FastAPI")
    print(f"\n2. Created Task #{task_id}")
    
    # Post-task (simulated)
    print("\n3. Post-Task Hook (successful):")
    post_result = post_task_hook(task_id, "Successfully built FastAPI endpoint at /api/users")
    print(f"   Verified: {post_result['verification']['verified']}")
    print(f"   Status: {post_result['status']}")
    
    print("\n✅ SWP Hooks operational!")
