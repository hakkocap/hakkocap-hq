import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import time
import os
import sys
from datetime import datetime

# 기존 기억 요새 코어 연동 (에러 무시용 래핑)
try:
    from ghost_memory_core import SovereignMemory
    mem_engine = SovereignMemory()
except:
    mem_engine = None

st.set_page_config(page_title="통합 캡틴스 지휘 센터", layout="wide", page_icon="🏴‍☠️")

with st.sidebar:
    st.title("🏴‍☠️ 지휘 센터 제어실")
    selected_modules = st.multiselect(
        "활성 모듈",
        ["SWP 모니터링", "기억 요새", "Langflow 통합", "🧪 나노봇 실험실"],
        default=["SWP 모니터링", "🧪 나노봇 실험실"]
    )
    st.subheader("📡 제어 패널")
    swp_db_path = st.text_input("SWP DB 경로", "/home/hakkocap/다운로드/swp/data/test.db")
    if st.button("🚀 ZMQ 네트워크 전체 동기화"):
        st.success("스웜 동기화 완료!")

st.title("🏰 통합 캡틴스 지휘 센터 (Captain's Board)")

# 1. SWP 모니터링 모듈
if "SWP 모니터링" in selected_modules:
    with st.container():
        st.header("📊 SWP 실시간 모니터링")
        if os.path.exists(swp_db_path):
            conn = sqlite3.connect(swp_db_path)
            try:
                score_df = pd.read_sql_query("SELECT captain_score, timestamp FROM disciplinary_log ORDER BY timestamp DESC LIMIT 10", conn)
                current_score = score_df.iloc[0]['captain_score'] if not score_df.empty else 1500
            except:
                score_df = pd.DataFrame()
                current_score = 1500
            conn.close()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("캡틴 누적 점수", f"{current_score:,} ⚡️", "+25")
            col2.metric("스웜 가동 효율", "99.1% 🚀", "+1.2%")
            col3.metric("진행 중인 작전", "3개", "1개 완료")
            col4.metric("수집된 야생 스킬", "14개", "신규")
                
            if not score_df.empty:
                st.subheader("📈 상벌점 누적 추이")
                score_df = score_df.sort_values(by='timestamp', ascending=True)
                fig = go.Figure(data=go.Scatter(x=score_df['timestamp'], y=score_df['captain_score'], mode='lines+markers', line=dict(color='#ff4500')))
                fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")

# 2. 나노봇 실험실 모듈
if "🧪 나노봇 실험실" in selected_modules:
    with st.container():
        st.header("🧪 나노봇 실험실 (자가 진화 생태계)")
        st.caption("외부 무기(코드)를 샌드박스에서 검증하고, 오프니-나노의 '공동 서명 합의제'로 SWP 무기고에 자동 병합합니다.")
        
        col_queue, col_lab = st.columns([1, 2])
        
        with col_queue:
            st.subheader("📥 1. 수집된 스킬 대기열")
            st.info("현재 대기 중인 야생 스킬 조각들")
            
            # 더미 데이터 큐
            skills_queue = [
                {"name": "github_crawler_v2", "risk": "High", "size": "45 lines"},
                {"name": "system_stat_monitor", "risk": "Low", "size": "12 lines"},
                {"name": "auto_clicker", "risk": "Medium", "size": "28 lines"}
            ]
            
            for s in skills_queue:
                st.markdown(f"**{s['name']}** (위험도: {s['risk']} / {s['size']})")
                
            if st.button("▶️ 샌드박스 병렬 폭격 개시", type="primary"):
                st.session_state['run_lab'] = True
                
        with col_lab:
            st.subheader("⚙️ 2. 격리 샌드박스 상태 & 판결")
            
            if st.session_state.get('run_lab', False):
                with st.spinner("🐳 병렬 Docker 샌드박스 컨테이너 가동 중... (CPU 0.25 / MEM 256MB 제한)"):
                    time.sleep(2) # 시뮬레이션 딜레이
                    
                st.success("✅ 컨테이너 실행 및 로그 추출 완료. 공동 판결 진행 중...")
                time.sleep(1)
                
                # 결과 렌더링 시뮬레이션
                st.markdown("### 🚦 [오프니-나노 공동 서명 판결문]")
                
                # 스킬 1 (합의 성공)
                with st.expander("🟢 [채택] system_stat_monitor (총점: 88/100)", expanded=True):
                    st.write("- **🧠 오프니 (40/50):** 무단 통신 없음. 안전함. (서명 완료 📝)")
                    st.write("- **⚙️ 나노 (48/50):** 외부 의존성 없음, 코드 최적화 우수. (서명 완료 📝)")
                    st.write("➡️ **결과:** `/app/swp/tools/system_stat_monitor.py` 병합 완료!")
                    
                # 스킬 2 (합의 기각 - 위험 감지)
                with st.expander("🔴 [기각] github_crawler_v2 (총점: 45/100)"):
                    st.write("- **🧠 오프니 (10/50):** 무단 `requests` 호출 및 의심스러운 헤더 발견. (기각 ❌)")
                    st.write("- **⚙️ 나노 (35/50):** 코드 길이는 적절하나 에러 발생 우려. (서명 완료 📝)")
                    st.write("➡️ **결과:** 보안 위험으로 즉시 컨테이너 및 코드 폐기.")
                    
                st.session_state['run_lab'] = False
            else:
                st.write("대기열의 스킬을 폭격하여 테스트를 시작하십시오.")
                
        st.markdown("---")

# 3. 기억 요새 모듈
if "기억 요새" in selected_modules:
    with st.container():
        st.header("🧠 소버린 기억 요새")
        st.write("현재 비활성화 됨 (대시보드 축소 뷰)")
        st.markdown("---")
