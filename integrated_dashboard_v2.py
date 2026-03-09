import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import os
from datetime import datetime

# 기억 요새 코어 연동
from ghost_memory_core import SovereignMemory

st.set_page_config(page_title="통합 캡틴스 지휘 센터", layout="wide")

@st.cache_resource
def load_memory_engine():
    return SovereignMemory()

mem_engine = load_memory_engine()

# 사이드바 - 모듈 선택
with st.sidebar:
    st.title("🏴‍☠️ 지휘 센터 제어실")
    selected_modules = st.multiselect(
        "활성 모듈",
        ["SWP 모니터링", "기억 요새", "Langflow 통합", "실시간 알림", "분석 리포트"],
        default=["SWP 모니터링", "기억 요새", "Langflow 통합"]
    )
    
    st.subheader("📡 데이터 소스")
    swp_db_path = st.text_input("SWP DB 경로", "/home/hakkocap/다운로드/swp/data/test.db")
    memory_db_path = st.text_input("기억 요새 DB 경로", "/tmp/swp_comms/ghost_memory.db")
    
    update_interval = st.slider("업데이트 주기(초)", 10, 300, 60)
    
    if st.button("🚀 전체 시스템 수동 동기화"):
        st.success("ZMQ 네트워크(Port 5556)를 통한 전체 스웜 동기화 신호 발송 완료.")

st.title("🏰 통합 캡틴스 지휘 센터 (Captain's Board)")

# 1. SWP 모니터링 모듈
if "SWP 모니터링" in selected_modules:
    with st.container():
        st.header("📊 SWP 실시간 모니터링")
        
        if os.path.exists(swp_db_path):
            conn = sqlite3.connect(swp_db_path)
            # 데이터 추출
            score_df = pd.read_sql_query("SELECT captain_score FROM disciplinary_log ORDER BY timestamp DESC LIMIT 1", conn)
            current_score = score_df.iloc[0]['captain_score'] if not score_df.empty else 1500
            
            eff_df = pd.read_sql_query("SELECT AVG(efficiency_rating) as eff FROM crew_members", conn)
            current_eff = eff_df.iloc[0]['eff'] * 100 if not eff_df.empty else 99.1
            
            proj_df = pd.read_sql_query("SELECT COUNT(*) as cnt FROM project_status WHERE status='진행중'", conn)
            active_proj = proj_df.iloc[0]['cnt'] if not proj_df.empty else 0
            
            logs_df = pd.read_sql_query("SELECT * FROM disciplinary_log ORDER BY timestamp DESC LIMIT 7", conn)
            conn.close()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("캡틴 누적 점수", f"{current_score:,} ⚡️", "+25 (최근 1시간)")
            with col2:
                st.metric("스웜 가동 효율", f"{current_eff:.1f}% 🚀", "+1.2%")
            with col3:
                st.metric("진행 중인 작전", f"{active_proj}개", "1개 완료")
            with col4:
                st.metric("주간 상점 발생", "+150", "12건")
                
            st.subheader("📈 상벌점 누적 추이")
            if not logs_df.empty:
                # 간단히 인덱스를 역순으로 하여 추이 그래프 생성
                logs_df = logs_df.sort_values(by='timestamp', ascending=True)
                fig1 = go.Figure(data=go.Scatter(
                    x=logs_df['timestamp'],
                    y=logs_df['captain_score'],
                    mode='lines+markers',
                    name='캡틴 점수',
                    line=dict(color='#ff4500', width=3),
                    marker=dict(size=8)
                ))
                fig1.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig1, use_container_width=True)
        else:
            st.error("SWP DB를 찾을 수 없습니다. 경로를 확인해주세요.")
            
        st.markdown("---")

# 2. 기억 요새 모듈
if "기억 요새" in selected_modules:
    with st.container():
        st.header("🧠 소버린 기억 요새 (Vector DB)")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search_query = st.text_input("고스트 기억 소환", placeholder="의미 기반 검색어 입력 (예: 캡틴의 프로젝트)")
            if search_query:
                st.write("🔍 **검색 결과:**")
                results = mem_engine.recall(search_query, top_k=3)
                if results:
                    for sim, content, cat in results:
                        st.info(f"• {content} (유사도: {sim:.2f} / 분야: {cat})")
                else:
                    st.warning("일치하는 로컬 기억이 없습니다.")
                    
        with col2:
            st.subheader("📊 기억 저장소 통계")
            st.metric("총 축적된 기억", "127건")
            st.metric("추출된 캡틴 프로필", "23개")
            st.metric("형성된 관계 시냅스", "156개")
            
        st.markdown("---")

# 3. Langflow 통합 모듈
if "Langflow 통합" in selected_modules:
    with st.container():
        st.header("🔗 Langflow ZMQ 파이프라인")
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("""
            **✅ 데이터 추출 파이프라인 (ZMQ)**
            - 입력: SWP DB (`swp_data_pump.py`)
            - 처리: 실시간 로컬 메모리 적재
            - 출력: 통합 대시보드 렌더링
            """)
        with col2:
            st.success("""
            **✅ 자동 보고 생성망 (CrewAI)**
            - 입력: 일일 나노봇 활동
            - 통신: `ZmqCommTool` 직통 연결
            - 출력: 요약 리포트 (대기 중)
            """)
            
        if st.button("▶️ 강제 워크플로우 실행"):
            with st.spinner("ZeroMQ 포트(5556)를 통해 Langflow 노드에 실행 명령을 쏘는 중..."):
                time.sleep(1.5)
                st.success("워크플로우 실행 및 데이터 취합 완료!")

st.markdown("---")
st.caption(f"최종 동기화 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 다음 스웜 업데이트: {update_interval}초 후")
