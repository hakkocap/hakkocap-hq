#!/usr/bin/env python3
import subprocess, sqlite3, time, os
from datetime import datetime

# import hooks
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from hooks.nanobot import pre_task_hook, post_task_hook, save_state_hook
from services.engine import SWPEngine

DB='/home/hakkocap/다운로드/swp/backend/data/swp.db'
AGENT_PY='/home/hakkocap/.nanobot/workspace/skills/learn-claude-code/agents/s01_agent_loop.py'
VENV_PY='/home/hakkocap/.nanobot/workspace/skills/learn-claude-code/venv/bin/python3'

engine = SWPEngine()

def save_memory_t1(task_id, title, content, phase='active'):
    engine.save_memory_tier1(task_id, title, content, phase)

def save_memory_t2(task_id, key, value):
    engine.save_memory_tier2(task_id, key, value)

def save_memory_t3(task_id, checklist):
    engine.save_memory_tier3(task_id, checklist)

def append_ledger(entry):
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    now=datetime.utcnow().isoformat()
    cur.execute("INSERT INTO disciplinary_ledger (entry, created_at) VALUES (?,?)",(entry, now))
    conn.commit(); conn.close()


def run_autopilot():
    task_desc='Run s01_agent_loop'
    pre=pre_task_hook(task_desc)
    # save into tier1 plan (use fake task id)
    task_id = int(time.time())
    save_memory_t1(task_id, 'pre_task', str(pre))

    # run agent subprocess
    cmd=[VENV_PY, AGENT_PY]
    proc=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    collected=[]
    start=time.time()
    first30=[]
    try:
        # collect first 30 lines / up to 10 seconds
        while True:
            line=proc.stdout.readline()
            if not line and proc.poll() is not None:
                break
            if line:
                collected.append(line)
                if len(first30)<30:
                    first30.append(line)
                # save short-term context
                save_memory(2,'runtime_line', line.strip())
            if time.time()-start>10 and len(first30)>=1:
                # enough
                break
        # attempt graceful termination
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
    except Exception as e:
        append_ledger(f'Autopilot exception: {e}')

    output=''.join(collected)
    save_memory(3,'final_output_summary', output[:4000])

    # call post task hook
    # create a fake task_id
    task_id= int(time.time())
    post=post_task_hook(task_id, output)
    save_memory(3,'post_verification', str(post))
    if not post.get('verification',{}).get('verified', True):
        append_ledger(f'Post verification failed: {post}')

    # write a short report to stdout
    print('--- AUTOPILOT REPORT ---')
    print('Pre-Task Hook:', pre['status'])
    print('First logs:')
    for l in first30:
        print(l.rstrip())
    print('Post-Task status:', post['status'])

if __name__=='__main__':
    run_autopilot()
