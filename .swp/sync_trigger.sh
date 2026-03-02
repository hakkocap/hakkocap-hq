#!/bin/bash
# SWP GitHub Auto-Sync Trigger
# /home/hakkocap/hakkocap-hq/.swp/sync_trigger.sh

REPO="/home/hakkocap/hakkocap-hq"
CONTEXT_BRIDGE="/home/hakkocap/캡틴스룸/Context_Bridge"

echo "[SWP-SYNC] Starting auto-sync at $(date)"

# Step 1: Context Bridge sync
cd "$REPO" || exit 1
rsync -av "$CONTEXT_BRIDGE/" "$REPO/context/" --delete

# Step 2: SWP Core sync
if [ -d "/home/hakkocap/다운로드/swp/backend" ]; then
    rsync -av "/home/hakkocap/다운로드/swp/backend/" "$REPO/swp/backend/" --delete
fi

# Step 3: Check for changes
if git diff --quiet HEAD; then
    echo "[SWP-SYNC] No changes detected. Aborting."
    exit 0
fi

# Step 4: Commit and push
git add -A
COMMIT_MSG="[SWP-SYNC] Context Bridge update: $(date +%Y-%m-%d %H:%M)"
git commit -m "$COMMIT_MSG"

# Step 5: Push to both branches
git checkout context-stream 2>/dev/null || git checkout -b context-stream main
git merge main --no-edit 2>/dev/null || true
git push origin context-stream
git checkout main
git push origin main

echo "[SWP-SYNC] Complete: Changes pushed to GitHub"
