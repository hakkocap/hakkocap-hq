import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Sovereign Memory Fortress", layout="wide")

# 데이터베이스 연결
def get_db_connection():
    return sqlite3.connect("/tmp/swp_comms/ghost_memory.db")

# 사이드바
with st.sidebar:
    st.title("🏴‍☠️ 기억 요새 제어실")
    st.markdown("---")
    
    # 검색 기능
    st.subheader("🔍 기억 검색")
    search_query = st.text_input("검색어를 입력하세요")
    search_button = st.button("검색 실행")
    
    # 필터
    st.subheader("📊 필터 옵션")
    category_filter = st.multiselect(
        "카테고리 필터",
        ["프로젝트", "하드웨어", "기술", "전략", "협력", "기타"],
        default=["프로젝트", "기술"]
    )
    
    date_range = st.date_input(
        "날짜 범위",
        value=(datetime.now() - timedelta(days=7), datetime.now())
    )
    
    st.markdown("---")
    st.info(f"서버 상태: ✅ 실행 중\n포트: 8501")

# 메인 대시보드
st.title("🏰 Sovereign Memory Fortress")
st.markdown("캡틴의 독립된 기억 요새 - 데이터 주권 100%")

# 통계 카드
col1, col2, col3, col4 = st.columns(4)
with col1:
    conn = get_db_connection()
    total_memories = pd.read_sql_query("SELECT COUNT(*) as count FROM long_term_memory", conn).iloc[0]['count']
    st.metric("총 기억 수", total_memories)
with col2:
    categories = pd.read_sql_query("SELECT COUNT(DISTINCT category) as count FROM long_term_memory", conn).iloc[0]['count']
    st.metric("카테고리 수", categories)
with col3:
    latest = pd.read_sql_query("SELECT MAX(timestamp) as latest FROM long_term_memory", conn).iloc[0]['latest']
    st.metric("최근 업데이트", latest[:10] if latest else "없음")
with col4:
    profile_items = pd.read_sql_query("SELECT COUNT(*) as count FROM user_profile", conn).iloc[0]['count']
    st.metric("프로필 항목", profile_items)
conn.close()

st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📝 기억 목록", "📈 통계 분석", "👤 캡틴 프로필"])

with tab1:
    st.subheader("최근 기록된 기억")
    conn = get_db_connection()
    
    # 검색 쿼리 구성
    query = "SELECT timestamp, content, category FROM long_term_memory WHERE 1=1"
    params = []
    
    if search_query and search_button:
        query += " AND content LIKE ?"
        params.append(f"%{search_query}%")
    
    if category_filter:
        placeholders = ','.join(['?'] * len(category_filter))
        query += f" AND category IN ({placeholders})"
        params.extend(category_filter)
    
    query += " ORDER BY timestamp DESC LIMIT 50"
    
    df = pd.read_sql_query(query, conn, params=params if params else None)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # 상세 보기
        selected_idx = st.selectbox("상세 보기 선택", range(len(df)), format_func=lambda x: df.iloc[x]['content'][:50] + "...")
        if selected_idx is not None:
            with st.expander("상세 내용", expanded=True):
                st.write(df.iloc[selected_idx]['content'])
                st.caption(f"카테고리: {df.iloc[selected_idx]['category']} | 시간: {df.iloc[selected_idx]['timestamp']}")
    else:
        st.info("검색 결과가 없습니다.")
    
    conn.close()

with tab2:
    st.subheader("기억 통계 분석")
    conn = get_db_connection()
    
    # 카테고리별 분포
    cat_df = pd.read_sql_query(
        "SELECT category, COUNT(*) as count FROM long_term_memory GROUP BY category ORDER BY count DESC",
        conn
    )
    
    if not cat_df.empty:
        fig1 = px.pie(cat_df, values='count', names='category', title='카테고리별 기억 분포')
        st.plotly_chart(fig1, use_container_width=True)
    
    # 시간별 추이
    time_df = pd.read_sql_query(
        """SELECT DATE(timestamp) as date, COUNT(*) as count 
           FROM long_term_memory 
           GROUP BY DATE(timestamp) 
           ORDER BY date""",
        conn
    )
    
    if not time_df.empty:
        fig2 = px.line(time_df, x='date', y='count', title='일별 기억 추가 추이')
        st.plotly_chart(fig2, use_container_width=True)
    
    conn.close()

with tab3:
    st.subheader("캡틴 프로필")
    conn = get_db_connection()
    
    profile_df = pd.read_sql_query(
        "SELECT key, value, updated_at FROM user_profile ORDER BY updated_at DESC",
        conn
    )
    
    if not profile_df.empty:
        for _, row in profile_df.iterrows():
            with st.expander(f"{row['key']} (업데이트: {row['updated_at'][:16]})"):
                st.write(row['value'])
    else:
        st.info("프로필 데이터가 없습니다.")
    
    conn.close()

# 푸터
st.markdown("---")
st.caption(f"Sovereign Memory Fortress v0.1 | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
