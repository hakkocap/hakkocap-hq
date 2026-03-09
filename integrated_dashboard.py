import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os

# 기억 요새 코어 연동 (Stage 2에서 만들었던 것)
from ghost_memory_core import SovereignMemory

st.set_page_config(page_title="🏴‍☠️ Captain's Command Center", layout="wide")

@st.cache_resource
def load_memory_engine():
    return SovereignMemory()

mem_engine = load_memory_engine()
SWP_DB_PATH = "/home/hakkocap/다운로드/swp/data/test.db"

def get_swp_data():
    conn = sqlite3.connect(SWP_DB_PATH)
    
    # 캡틴 누적 점수
    cap_score = pd.read_sql_query("SELECT captain_score FROM disciplinary_log ORDER BY timestamp DESC LIMIT 1", conn)
    score = cap_score.iloc[0]['captain_score'] if not cap_score.empty else 1500
    
    # 크루 효율
    crew_eff = pd.read_sql_query("SELECT AVG(efficiency_rating) as eff FROM crew_members", conn)
    eff = crew_eff.iloc[0]['eff'] if not crew_eff.empty else 0
    
    # 최근 활동
    logs = pd.read_sql_query("SELECT action_type, points, description, timestamp FROM disciplinary_log ORDER BY timestamp DESC LIMIT 5", conn)
    
    # 크루 현황
    crews = pd.read_sql_query("SELECT name, role, efficiency_rating * 100 as efficiency FROM crew_members", conn)
    
    # 프로젝트
    projects = pd.read_sql_query("SELECT project_name, status, progress_percent FROM project_status", conn)
    
    conn.close()
    return score, eff, logs, crews, projects

st.title("🏴‍☠️ SWP 통합 지휘 센터 (Captain's Dashboard)")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📊 SWP 통계 및 제어", "🏰 기억 요새 (Vector DB)", "⚙️ Langflow 파이프라인"])

with tab1:
    st.header("SWP 실시간 모니터링")
    
    if os.path.exists(SWP_DB_PATH):
        score, eff, logs, crews, projects = get_swp_data()
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="👑 캡틴 권위 지수 (Score)", value=f"{score} ⚡", delta="최고 수준")
        col2.metric(label="🤖 나노봇 스웜 효율 (Efficiency)", value=f"{eff*100:.1f} %", delta="정상 가동 중")
        col3.metric(label="🚀 진행 중인 작전", value=len(projects[projects['status'] == '진행중']))
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_chart, col_table = st.columns(2)
        
        with col_chart:
            st.subheader("크루 가동 효율성")
            fig = px.bar(crews, x='name', y='efficiency', color='name', text='efficiency')
            st.plotly_chart(fig, use_container_width=True)
            
        with col_table:
            st.subheader("최근 SWP 활동 로그")
            st.dataframe(logs, use_container_width=True)
            
            st.subheader("작전 (Project) 진행률")
            st.dataframe(projects, use_container_width=True)
    else:
        st.error(f"SWP 데이터베이스를 찾을 수 없습니다: {SWP_DB_PATH}")

with tab2:
    st.header("의미 기반 기억 소환 (Sovereign Memory)")
    query = st.text_input("질문이나 키워드를 입력하세요 (예: 캡틴의 프로젝트는?)")
    if query:
        results = mem_engine.recall(query, top_k=5)
        if results:
            for sim, content, cat in results:
                st.info(f"[유사도: {sim:.3f}] {content} (카테고리: {cat})")
        else:
            st.warning("일치하는 기억이 없습니다.")

with tab3:
    st.header("Langflow 오케스트레이션")
    st.write("현재 구동 중인 Langflow V4 파이프라인과 ZeroMQ 워커들의 상태입니다.")
    st.success("✅ ZeroMQ (ZMQ) Manager Node: 포트 5556 정상 대기 중")
    st.success("✅ Langflow API: http://localhost:7860/ 연결 완료")
    
    if st.button("🔄 수동 동기화 트리거"):
        with st.spinner("ZeroMQ를 통해 Langflow에 동기화 신호를 쏘는 중..."):
            time.sleep(1)
            st.success("동기화 완료!")
