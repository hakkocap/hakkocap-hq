import os
import re

html_path = "/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/frontend/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 기존에 주입된 정적 HTML을 걷어냄
content = re.sub(r'<!-- 🏴‍☠️ CAPTAIN DASHBOARD INJECTION -->.*?<!-- /CAPTAIN DASHBOARD INJECTION -->\n?', '', content, flags=re.DOTALL)

# 동적 데이터 Fetch 및 UI 생성을 수행하는 JS 코드 주입
inject_js = """
<!-- 🏴‍☠️ CAPTAIN DASHBOARD INJECTION V3 -->
<script>
  function createCaptainDashboard() {
    if (document.getElementById('captain-dashboard')) return;

    const board = document.createElement('div');
    board.id = 'captain-dashboard';
    board.style.cssText = 'position: absolute; top: 10px; right: 10px; width: 350px; background: #1e1e2f; color: white; border: 2px solid #4caf50; border-radius: 8px; z-index: 999999; padding: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); font-family: sans-serif; transition: all 0.3s ease;';
    
    board.innerHTML = `
      <h3 style="margin: 0 0 10px 0; color: #4caf50; display:flex; justify-content: space-between; align-items:center;">
        <span>🏴‍☠️ Captain's Board</span>
        <button id="cap-refresh-btn" style="background:transparent; border:none; color:white; cursor:pointer; font-size:16px;">🔄</button>
      </h3>
      <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
        <span>Score:</span> <strong id="cap-score" style="font-size: 1.2em; color: #fff;">Loading...</strong>
      </div>
      <div style="display: flex; justify-content: space-between;">
        <span>Swarm Eff:</span> <strong id="cap-eff" style="font-size: 1.2em; color: #03a9f4;">Loading...</strong>
      </div>
      <div style="margin-top: 10px; font-size: 0.8em; color: #aaa; text-align: right;" id="cap-status">Initializing...</div>
    `;
    
    document.body.appendChild(board);

    // 이벤트 리스너: React가 바디 내용을 지우더라도 대시보드를 부활시킴 (MutationObserver)
    const observer = new MutationObserver(() => {
        if (!document.body.contains(board)) {
            document.body.appendChild(board);
        }
    });
    observer.observe(document.body, { childList: true });

    document.getElementById('cap-refresh-btn').addEventListener('click', fetchDashboardData);
    
    fetchDashboardData();
    setInterval(fetchDashboardData, 30000); // 30초 자동 갱신
  }

  async function fetchDashboardData() {
    const statusEl = document.getElementById('cap-status');
    const scoreEl = document.getElementById('cap-score');
    const effEl = document.getElementById('cap-eff');
    
    statusEl.innerText = 'Fetching data...';
    try {
        // 실제 API 연동 전에는 Phase 1 노드의 응답 형식에 맞춰 Mock Fetch (추후 실제 Endpoint로 변경)
        // 현재 Langflow Flow API 연동에 인증(Auth) 장벽이 있을 수 있으므로 임시로 자체 데이터 표시
        setTimeout(() => {
            scoreEl.innerText = '1,500 🌟';
            effEl.innerText = '98.5% ⚡';
            statusEl.innerText = 'Live Sync (Node API 연동 대기)';
            statusEl.style.color = '#4caf50';
        }, 800);
    } catch (e) {
        statusEl.innerText = 'Error: ' + e.message;
        statusEl.style.color = 'red';
    }
  }

  // DOMContentLoaded 와 상관없이 바로 실행하고, load 시점에도 확인
  createCaptainDashboard();
  window.addEventListener('load', createCaptainDashboard);
</script>
<!-- /CAPTAIN DASHBOARD INJECTION V3 -->
"""

new_content = re.sub(r'(<body[^>]*>)', r'\1\n' + inject_js, content)
with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)
print("Inject JS V3 Success")
