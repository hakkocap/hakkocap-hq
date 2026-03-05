#!/usr/bin/env python3
"""
Skill-to-Task bridge: selects best skill manual for an incoming task description
and enqueues an Autopilot task (creates task record) for execution.
"""
import sqlite3, logging, time, os
DB='/home/hakkocap/다운로드/swp/backend/data/swp.db'
LOG='/home/hakkocap/다운로드/swp/backend/logs/swp_core.log'

logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

from services.engine import SWPEngine
engine=SWPEngine()

def pick_skill_for(description: str):
    # simple keyword match using engine.parse_intent
    intent = engine.parse_intent(description)
    # search skill_manuals for matching category
    conn=sqlite3.connect(DB)
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("SELECT * FROM skill_manuals WHERE category = ? ORDER BY updated_at DESC LIMIT 1", (intent['task_type'],))
    row=cur.fetchone()
    conn.close()
    if row:
        logging.info('Skill selected for %s : %s', description, row['name'])
        return dict(row)
    # fallback: most recent manual
    row=engine.get_skill_manuals()
    if row:
        logging.info('Fallback skill selected: %s', row[0]['name'])
        return row[0]
    return None

def create_autopilot_task(title, description):
    task_id = engine.create_task(title, description)
    logging.info('Created autopilot task %s for %s', task_id, title)
    return task_id

if __name__=='__main__':
    import sys
    if len(sys.argv)<2:
        print('usage: skill_task_bridge.py "task description"')
        sys.exit(1)
    desc=sys.argv[1]
    skill=pick_skill_for(desc)
    if skill:
        print('Selected skill:', skill['name'])
    tid=create_autopilot_task('Auto:'+desc, desc)
    print('Created task id', tid)
