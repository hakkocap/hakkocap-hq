import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

st.set_page_config(page_title="Sovereign Memory Fortress", layout="wide")

# Stage 2: 코어 엔진 연동
from ghost_memory_core import SovereignMemory

@st.cache_resource
def load_memory_engine():
    return SovereignMemory()

mem_engine = load_memory_engine()

def get_memories():
    conn = sqlite3.connect("/tmp/swp_comms/ghost_memory.db")
    df = pd.read_sql_query("SELECT id, timestamp, content, category FROM long_term_memory ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def get_profiles():
    conn = sqlite3.connect("/tmp/swp_comms/ghost_memory.db")
    df = pd.read_sql_query("SELECT key, value, updated_at FROM user_profile", conn)
    conn.close()
    return df

st.title("🏰 Sovereign Memory Fortress")
st.sidebar.success("✅ 엔진 연결 완료: jhgan/ko-sroberta-multitask")

tab1, tab2, tab3 = st.tabs(["📝 통합 기억 목록", "🔍 의미 기반 검색 (Stage 2)", "👤 캡틴 프로필"])

with tab1:
    st.subheader("모든 기억 로그")
    st.dataframe(get_memories(), use_container_width=True)

with tab2:
    st.subheader("한국어 AI 벡터 검색")
    query = st.text_input("질문이나 키워드를 입력하세요 (예: 캡틴의 프로젝트는?)")
    if query:
        st.write(f"검색어: `{query}`")
        results = mem_engine.recall(query, top_k=5)
        if results:
            for score, content, cat in results:
                st.info(f"[유사도: {score:.3f}] {content} (카테고리: {cat})")
        else:
            st.warning("일치하는 기억이 없습니다.")

with tab3:
    st.subheader("고스트 에이전트 자동 수집 프로필")
    st.table(get_profiles())
    
    st.markdown("---")
    st.subheader("🛠 수동 프로필 주입")
    col1, col2 = st.columns(2)
    with col1:
        new_key = st.text_input("프로필 항목 (예: 선호무기)")
    with col2:
        new_val = st.text_input("값 (예: 장검)")
    if st.button("프로필 주입"):
        mem_engine.update_profile(new_key, new_val)
        st.success(f"프로필 업데이트 완료: {new_key} = {new_val}")
        st.rerun()
