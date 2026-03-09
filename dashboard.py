import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Sovereign Memory Dashboard", layout="wide")

def get_data():
    conn = sqlite3.connect("ghost_memory.db")
    df = pd.read_sql_query("SELECT timestamp, content, category FROM long_term_memory ORDER BY timestamp DESC", conn)
    conn.close()
    return df

st.title("🏴‍☠️ Ghost Memory: Sovereign Dashboard")
st.sidebar.info("캡틴의 독립된 요새, 로컬 기억 저장소 관리 시스템")

st.subheader("📝 최근 기록된 기억 (Recent Memories)")
data = get_data()
st.dataframe(data, use_container_width=True)

st.subheader("🔍 의미 기반 기억 소환 (Semantic Search)")
query = st.text_input("찾고 싶은 기억의 '의미'를 입력하세요:")
if query:
    st.write(f"'{query}'와(과) 관련된 가장 유력한 기억을 소환 중...")
    st.success("소환된 기억: (Vector Search 연동 대기 중)")
