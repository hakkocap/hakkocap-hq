#!/usr/bin/env python3
"""
Self-healing helper: checks common issues and attempts repair
- ensures critical venv packages installed
- fixes common permission issues on key paths
Logs actions to swp_core.log
"""
import os, subprocess, logging
LOG='/home/hakkocap/다운로드/swp/backend/logs/swp_core.log'
logging.basicConfig(filename=LOG, level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

VENV='/home/hakkocap/.nanobot/workspace/skills/learn-claude-code/venv'
REQUIRED=['anthropic','python-dotenv']

# fix permissions for key paths
KEY_PATHS=['/home/hakkocap/다운로드/swp/backend/data','/home/hakkocap/.nanobot/workspace/skills/learn-claude-code']
for p in KEY_PATHS:
    try:
        if os.path.exists(p):
            os.chmod(p, 0o755)
            logging.info('Set perms 755 on %s', p)
    except Exception as e:
        logging.exception('perm fix failed %s %s', p, e)

# ensure venv packages
pip=os.path.join(VENV,'bin','pip')
if os.path.exists(pip):
    try:
        out=subprocess.check_output([pip,'install']+REQUIRED, stderr=subprocess.STDOUT).decode()
        logging.info('pip install output: %s', out[:200])
    except Exception as e:
        logging.exception('pip install failed: %s', e)
else:
    logging.warning('venv pip not found at %s', pip)

print('self-heal completed')
