import os
import re

INDEX_PATH = "/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/frontend/index.html"

def inject_v4():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # V4 스크립트: 실제 8888 포트에서 데이터를 끌어오는 해적식 파이프라인 연동
    injected_script = """
    <script id="captain-board-v4">
        (function() {
            if (document.getElementById('captain-board-v4-logic')) return;

            const board = document.createElement('div');
            board.id = 'captain-board-v4-logic';
            board.style.cssText = 'position:fixed; top:20px; right:20px; z-index:99999; background:rgba(20,20,20,0.9); border:2px solid #ff4500; border-radius:10px; padding:15px; color:#fff; font-family:monospace; box-shadow:0 0 15px rgba(255,69,0,0.5); backdrop-filter:blur(5px); transition:all 0.3s ease;';

            board.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #444; padding-bottom:10px; margin-bottom:10px;">
                    <h3 style="margin:0; font-size:16px; color:#ff4500;">🏴‍☠️ SWP Live Board</h3>
                    <button id="cap-refresh-btn-v4" style="background:none; border:none; cursor:pointer; font-size:16px; padding:5px; border-radius:5px; transition:background 0.2s;">🔄</button>
                </div>
                <div style="font-size:14px; margin-bottom:8px;">Live Score: <strong id="cap-score-v4" style="color:#00ff00;">Loading...</strong></div>
                <div style="font-size:14px; margin-bottom:10px;">Efficiency: <strong id="cap-eff-v4" style="color:#00ff00;">Loading...</strong></div>
                <div id="cap-status-v4" style="font-size:11px; color:#888; text-align:right;">Connecting Pipeline...</div>
            `;

            document.body.appendChild(board);

            const scoreEl = document.getElementById('cap-score-v4');
            const effEl = document.getElementById('cap-eff-v4');
            const statusEl = document.getElementById('cap-status-v4');
            const refreshBtn = document.getElementById('cap-refresh-btn-v4');

            async function fetchRealData() {
                scoreEl.innerText = 'Syncing...';
                effEl.innerText = 'Syncing...';
                statusEl.innerText = 'Fetching from Pump...';
                
                try {
                    // 해적식 데이터 펌프 (포트 8888) 직결
                    const response = await fetch('http://localhost:8888');
                    const data = await response.json();
                    
                    scoreEl.innerText = data.score;
                    effEl.innerText = data.efficiency;
                    statusEl.innerText = data.status + ' - ' + new Date().toLocaleTimeString();
                    statusEl.style.color = '#00ff00';
                } catch (err) {
                    scoreEl.innerText = 'Pipeline ERR';
                    effEl.innerText = 'Pipeline ERR';
                    statusEl.innerText = 'Pump Offline (Port 8888)';
                    statusEl.style.color = '#ff0000';
                }
            }

            refreshBtn.addEventListener('click', () => {
                refreshBtn.style.transform = 'rotate(180deg)';
                setTimeout(() => refreshBtn.style.transform = 'rotate(0deg)', 300);
                fetchRealData();
            });

            // 초기 로드
            fetchRealData();
            
            // 15초마다 자동 갱신
            setInterval(fetchRealData, 15000);

            // 바퀴벌레 부활 모듈 (React가 덮어써도 살아남음)
            const observer = new MutationObserver(() => {
                if (!document.body.contains(board)) {
                    document.body.appendChild(board);
                }
            });
            observer.observe(document.body, { childList: true, subtree: true });
        })();
    </script>
    """

    # 기존 주입된 스크립트(V3)가 있다면 싹 날려버리고 V4로 교체
    html_content = re.sub(r'<script id="captain-board-.*?<\/script>', '', html_content, flags=re.DOTALL)
    
    if "</body>" in html_content:
        new_html = html_content.replace("</body>", f"{injected_script}\n</body>")
    else:
        new_html = html_content + injected_script

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("✅ [성공] V4 (Real Data Pipeline) JS 주입 완료.")

if __name__ == "__main__":
    inject_v4()
