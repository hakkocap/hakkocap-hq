#!/usr/bin/env python3
"""
Mailbox watcher: watches /home/hakkocap/agent_mailbox/openclaw.inbox and ingests new lines
immediately into SWP DB Tier-2 (context) and Tier-3 (immutable commands). Writes unified log.
"""
import os, time, sqlite3, logging
INBOX='/home/hakkocap/agent_mailbox/openclaw.inbox'
DB='/home/hakkocap/다운로드/swp/backend/data/swp.db'
LOG='/home/hakkocap/다운로드/swp/backend/logs/swp_core.log'

os.makedirs(os.path.dirname(LOG), exist_ok=True)
logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

logging.info('Mailbox watcher starting')

last_mtime = 0
while True:
    try:
        if os.path.exists(INBOX):
            m = os.path.getmtime(INBOX)
            if m > last_mtime:
                last_mtime = m
                with open(INBOX,'r') as f:
                    lines=[l.strip() for l in f.readlines() if l.strip()]
                if lines:
                    conn=sqlite3.connect(DB)
                    cur=conn.cursor()
                    for line in lines:
                        # write to tier2 as context and tier3 as immutable command
                        now=time.strftime('%Y-%m-%d %H:%M:%S')
                        cur.execute("INSERT INTO memory_tier2_context (task_id, context_key, context_value, updated_at) VALUES (?,?,?,?)",(0,'inbox_line', line, now))
                        cur.execute("INSERT INTO memory_tier3_checklists (task_id, checklist_item, order_index) VALUES (?,?,?)",(0,'IMMUTABLE_CMD: '+line, int(time.time())))
                        cur.execute("INSERT OR REPLACE INTO critical_context (key,value,source) VALUES ('last_inbox_command',?, 'inbox')",(line,))
                        logging.info('Ingested inbox line to DB: %s', line)
                    conn.commit(); conn.close()
                    # clear inbox
                    open(INBOX,'w').close()
        time.sleep(1)
    except Exception as e:
        logging.exception('Watcher error: %s', e)
        time.sleep(5)
