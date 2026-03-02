"""
SWP API Routes
Sovereign Workflow Protocol - REST API
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List
import json

from services.engine import SWPEngine

app = FastAPI(title="Sovereign Workflow Protocol")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SWPEngine()

# === MODELS ===
class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    checklist: Optional[List[str]] = None

class SkillManualCreate(BaseModel):
    name: str
    category: str
    content: str
    keywords: Optional[str] = ""

class VerificationRequest(BaseModel):
    task_id: int
    output: str

class RCARequest(BaseModel):
    task_id: int
    error_message: str

# === TASK ROUTES ===
@app.post("/api/tasks")
def create_task(task: TaskCreate):
    task_id = engine.create_task(task.title, task.description)
    return {"task_id": task_id, "status": "pending"}

@app.get("/api/tasks")
def list_tasks(status: Optional[str] = None):
    return engine.list_tasks(status)

@app.get("/api/tasks/{task_id}")
def get_task(task_id: int):
    task = engine.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Load memory tiers
    task["memory"] = engine.get_task_memory(task_id)
    # Load execution state
    task["execution_state"] = engine.load_execution_state(task_id)
    return task

@app.patch("/api/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    # This would update task - simplified for demo
    return {"task_id": task_id, "updated": True}

# === VERIFICATION HOOK ===
@app.post("/api/verify")
def verify_output(req: VerificationRequest):
    """Post-task verification hook."""
    result = engine.verify_task(req.task_id, req.output)
    return result

# === RCA HOOK ===
@app.post("/api/rca")
def trigger_rca(req: RCARequest):
    """Self-audit and disciplinary logic."""
    result = engine.perform_rca(req.task_id, req.error_message)
    return result

# === SKILL MANUALS ===
@app.post("/api/skills")
def add_skill_manual(manual: SkillManualCreate):
    manual_id = engine.add_skill_manual(
        manual.name, manual.category, manual.content, manual.keywords or ""
    )
    return {"manual_id": manual_id}

@app.get("/api/skills")
def list_skills(category: Optional[str] = None):
    return engine.get_skill_manuals(category)

@app.get("/api/skills/{category}/load")
def load_skill_for_task(category: str):
    """Pre-task hook: Load skill manual."""
    manuals = engine.get_skill_manuals(category)
    return {"manual": manuals[0] if manuals else None} if manuals else {"manual": None}

# === MEMORY ===
@app.get("/api/memory/{task_id}")
def get_task_memory(task_id: int):
    """Get three-tier memory for task."""
    return engine.get_task_memory(task_id)

# === DISCIPLINARY LEDGER ===
@app.get("/api/disciplinary")
def get_disciplinary_records(task_id: Optional[int] = None):
    return engine.get_disciplinary_records(task_id)

# === PATTERN RECOGNITION ===
@app.get("/api/patterns/{pattern_type}/hints")
def get_hints(pattern_type: str):
    return engine.get_optimization_hints(pattern_type)

# === STATE PERSISTENCE ===
@app.post("/api/state/{task_id}/save")
def save_state(task_id: int, current_step: str, step_index: int):
    engine.save_execution_state(task_id, current_step, step_index)
    return {"saved": True}

@app.get("/api/state/{task_id}/resume")
def resume_state(task_id: int):
    state = engine.load_execution_state(task_id)
    if not state:
        raise HTTPException(status_code=404, detail="No saved state found")
    return state

# === WEB DASHBOARD ===
@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SWP - Captain's Dashboard</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Segoe UI', sans-serif; background: #0a0a0f; color: #e0e0e0; min-height: 100vh; }
            .header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 20px; border-bottom: 2px solid #0f3460; }
            .header h1 { color: #e94560; font-size: 1.8rem; }
            .header .subtitle { color: #888; font-size: 0.9rem; margin-top: 5px; }
            .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .card { background: #1a1a2e; border-radius: 12px; padding: 20px; border: 1px solid #0f3460; }
            .card h2 { color: #e94560; margin-bottom: 15px; font-size: 1.2rem; border-bottom: 1px solid #0f3460; padding-bottom: 10px; }
            .btn { background: #e94560; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            .btn:hover { background: #ff6b6b; }
            .btn-small { padding: 5px 10px; font-size: 0.8rem; }
            .btn-success { background: #00d9a5; }
            .input { width: 100%; padding: 10px; background: #0a0a0f; border: 1px solid #0f3460; color: #e0e0e0; border-radius: 6px; margin-bottom: 10px; }
            .input:focus { outline: none; border-color: #e94560; }
            textarea.input { min-height: 100px; resize: vertical; }
            .task-list { max-height: 400px; overflow-y: auto; }
            .task-item { background: #0a0a0f; padding: 12px; margin-bottom: 8px; border-radius: 8px; border-left: 3px solid #0f3460; }
            .task-item.pending { border-left-color: #ffc107; }
            .task-item.in_progress { border-left-color: #2196f3; }
            .task-item.completed { border-left-color: #00d9a5; }
            .task-item.failed { border-left-color: #e94560; }
            .task-header { display: flex; justify-content: space-between; align-items: center; }
            .task-title { font-weight: bold; }
            .task-status { font-size: 0.8rem; padding: 2px 8px; border-radius: 4px; background: #0f3460; }
            .checklist { margin-top: 10px; }
            .checklist-item { padding: 5px 0; font-size: 0.9rem; }
            .checklist-item.completed { text-decoration: line-through; color: #666; }
            .ledger-item { background: #0a0a0f; padding: 10px; margin-bottom: 8px; border-radius: 6px; }
            .ledger-item .error { color: #e94560; }
            .ledger-item .root-cause { color: #ffc107; font-size: 0.9rem; }
            .ledger-item .correction { color: #00d9a5; font-size: 0.9rem; }
            .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
            .tab { padding: 10px 20px; background: #1a1a2e; border: 1px solid #0f3460; border-radius: 6px; cursor: pointer; }
            .tab.active { background: #e94560; border-color: #e94560; }
            .hidden { display: none; }
            #taskModal { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); display: none; justify-content: center; align-items: center; }
            #taskModal .modal-content { background: #1a1a2e; padding: 30px; border-radius: 12px; max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto; }
            .skill-category { display: inline-block; padding: 3px 10px; background: #0f3460; border-radius: 4px; font-size: 0.8rem; margin-right: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚓ Sovereign Workflow Protocol</h1>
            <div class="subtitle">Captain's Command Dashboard | Nanobot Control Center</div>
        </div>
        
        <div class="container">
            <div class="tabs">
                <button class="tab active" onclick="showTab('tasks')">Tasks</button>
                <button class="tab" onclick="showTab('skills')">Skill Vault</button>
                <button class="tab" onclick="showTab('ledger')">Disciplinary Ledger</button>
                <button class="tab" onclick="showTab('memory')">Memory</button>
            </div>
            
            <!-- TASKS TAB -->
            <div id="tasksTab">
                <div class="grid">
                    <div class="card">
                        <h2>⚔️ Create New Task</h2>
                        <input class="input" id="taskTitle" placeholder="Task Title">
                        <textarea class="input" id="taskDesc" placeholder="Captain's Intent - Describe what needs to be done..."></textarea>
                        <button class="btn" onclick="createTask()">Create Task</button>
                    </div>
                    
                    <div class="card">
                        <h2>📋 Active Tasks</h2>
                        <div class="task-list" id="taskList">
                            <p style="color:#666">No active tasks</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- SKILLS TAB -->
            <div id="skillsTab" class="hidden">
                <div class="grid">
                    <div class="card">
                        <h2>📚 Add Skill Manual</h2>
                        <input class="input" id="skillName" placeholder="Manual Name">
                        <select class="input" id="skillCategory">
                            <option value="frontend">Frontend</option>
                            <option value="backend">Backend</option>
                            <option value="database">Database</option>
                            <option value="devops">DevOps</option>
                            <option value="recon">Reconnaissance</option>
                            <option value="scraping">Web Scraping</option>
                        </select>
                        <input class="input" id="skillKeywords" placeholder="Trigger keywords (comma-separated)">
                        <textarea class="input" id="skillContent" placeholder="Skill Manual Content..."></textarea>
                        <button class="btn" onclick="addSkill()">Save Manual</button>
                    </div>
                    
                    <div class="card">
                        <h2>📖 Skill Vault</h2>
                        <div id="skillList"></div>
                    </div>
                </div>
            </div>
            
            <!-- LEDGER TAB -->
            <div id="ledgerTab" class="hidden">
                <div class="card">
                    <h2>📊 Disciplinary Ledger</h2>
                    <p style="color:#666;margin-bottom:15px">Root Cause Analysis & Error Tracking</p>
                    <div id="ledgerList"></div>
                </div>
            </div>
            
            <!-- MEMORY TAB -->
            <div id="memoryTab" class="hidden">
                <div class="card">
                    <h2>🧠 Three-Tier Memory System</h2>
                    <p style="color:#666;margin-bottom:15px">Tier 1: Plans | Tier 2: Context | Tier 3: Checklists</p>
                    <p>Select a task to view its memory</p>
                </div>
            </div>
        </div>
        
        <script>
            const API = '';
            
            function showTab(tab) {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                event.target.classList.add('active');
                document.querySelectorAll('[id$="Tab"]').forEach(t => t.classList.add('hidden'));
                document.getElementById(tab + 'Tab').classList.remove('hidden');
                if (tab === 'tasks') loadTasks();
                if (tab === 'skills') loadSkills();
                if (tab === 'ledger') loadLedger();
            }
            
            async function createTask() {
                const title = document.getElementById('taskTitle').value;
                const desc = document.getElementById('taskDesc').value;
                if (!title || !desc) return alert('Fill all fields');
                
                const res = await fetch(API + '/api/tasks', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({title, description: desc})
                });
                const data = await res.json();
                alert('Task #' + data.task_id + ' created');
                document.getElementById('taskTitle').value = '';
                document.getElementById('taskDesc').value = '';
                loadTasks();
            }
            
            async function loadTasks() {
                const res = await fetch(API + '/api/tasks');
                const tasks = await res.json();
                const list = document.getElementById('taskList');
                
                if (!tasks.length) {
                    list.innerHTML = '<p style=\"color:#666\">No tasks</p>';
                    return;
                }
                
                list.innerHTML = tasks.map(t => {
                    const checklist = t.checklist ? JSON.parse(t.checklist) : [];
                    return `
                        <div class=\"task-item ${t.status}\">
                            <div class=\"task-header\">
                                <span class=\"task-title\">#${t.id} ${t.title}</span>
                                <span class=\"task-status\">${t.status}</span>
                            </div>
                            <p style=\"font-size:0.85rem;color:#888;margin:5px 0\">${t.description.substring(0,100)}...</p>
                            <div class=\"checklist\">
                                ${checklist.slice(0,3).map((c,i) => `<div class=\"checklist-item\">☐ ${c}</div>`).join('')}
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            async function addSkill() {
                const name = document.getElementById('skillName').value;
                const category = document.getElementById('skillCategory').value;
                const keywords = document.getElementById('skillKeywords').value;
                const content = document.getElementById('skillContent').value;
                
                const res = await fetch(API + '/api/skills', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, category, keywords, content})
                });
                alert('Manual saved');
                loadSkills();
            }
            
            async function loadSkills() {
                const res = await fetch(API + '/api/skills');
                const skills = await res.json();
                const list = document.getElementById('skillList');
                
                list.innerHTML = skills.map(s => `
                    <div style=\"background:#0a0a0f;padding:12px;margin-bottom:8px;border-radius:8px\">
                        <span class=\"skill-category\">${s.category}</span>
                        <strong>${s.name}</strong>
                        <p style=\"font-size:0.85rem;color:#888;margin-top:5px\">${s.content.substring(0,100)}...</p>
                    </div>
                `).join('');
            }
            
            async function loadLedger() {
                const res = await fetch(API + '/api/disciplinary');
                const records = await res.json();
                const list = document.getElementById('ledgerList');
                
                if (!records.length) {
                    list.innerHTML = '<p style=\"color:#666\">No disciplinary records</p>';
                    return;
                }
                
                list.innerHTML = records.map(r => `
                    <div class=\"ledger-item\">
                        <div class=\"error\">⚠️ ${r.error_type}</div>
                        <div class=\"root-cause\">🔍 Root Cause: ${r.root_cause}</div>
                        <div class=\"correction\">✅ Correction: ${r.correction_action}</div>
                    </div>
                `).join('');
            }
            
            // Initial load
            loadTasks();
        </script>
    </body>
    </html>
    """

@app.get("/dashboard")
def dashboard_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse("/")
