import os
html_path = "/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/frontend/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()
inject_html = """
<!-- 🏴‍☠️ CAPTAIN DASHBOARD INJECTION -->
<div id="captain-dashboard" style="position: absolute; top: 10px; right: 10px; width: 350px; background: #1e1e2f; color: white; border: 2px solid #4caf50; border-radius: 8px; z-index: 999999; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); font-family: sans-serif;">
  <h3 style="margin: 0 0 10px 0; color: #4caf50;">🏴‍☠️ Captain's Board</h3>
  <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
    <span>Score:</span> <strong style="font-size: 1.2em; color: #fff;">1500</strong>
  </div>
  <div style="display: flex; justify-content: space-between;">
    <span>Swarm Eff:</span> <strong style="font-size: 1.2em; color: #03a9f4;">98%</strong>
  </div>
</div>
<!-- /CAPTAIN DASHBOARD INJECTION -->
"""
if "CAPTAIN DASHBOARD INJECTION" not in content:
    new_content = content.replace("<body>", f"<body>\n{inject_html}")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Inject Success")
else:
    print("Already Injected")
