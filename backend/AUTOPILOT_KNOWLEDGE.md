AUTOPILOT_KNOWLEDGE

This file collects successful autopilot run patterns and operational notes for successor agents.

Recent entries:

- PROVISIONAL PASS: s02 simulation (Simulate s02 tool use: run pwd and ls)
  - Preconditions: .env present, venv available, skill_manuals loaded
  - Steps taken: pre_task_hook -> run_bash(pwd, ls) -> save tier2/tier3 -> post_task verification (TEST_MODE)
  - Notes: system paths: /home/hakkocap/.nanobot/workspace/skills/learn-claude-code

- PROVISIONAL PASS: s01 agent loop (test-mode)
  - Preconditions: MODEL_ID set in .env (test value), anthropic package installed in venv
  - Steps: venv python runs agents/s01_agent_loop.py, logs captured to output.log, memory tiers updated
  - Notes: Real LLM API key required for full PASS

How to use:
1. Inspect critical_context table in SWP DB for captain preferences and recent context.
2. Load .env and venv paths from SNAPSHOT_SYSTEM.md
3. To run full PASS: populate ANTHROPIC_API_KEY in .env and re-run AUTOPILOT

