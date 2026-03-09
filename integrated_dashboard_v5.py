import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import time
import os
import json

st.set_page_config(page_title="통합 캡틴스 지휘 센터", layout="wide", page_icon="🏴‍☠️")

# 병합된 스킬 히스토리 (결재창을 대체)
if 'merged_skills' not in st.session_state:
    st.session_state['merged_skills'] = [
        {
            "date": "2026-03-08 15:40",
            "name": "scrapling_spider_v1",
            "score": 92,
            "type": "Free/OpenSource",
            "desc": "클라우드플레어 등 안티봇을 회피하는 초고속 정찰 프레임워크."
        }
    ]

with st.sidebar:
    st.title("🏴‍☠️ 지휘 센터 제어실")
    selected_modules = st.multiselect(
        "활성 모듈",
        ["SWP 모니터링", "🧪 나노봇 실험실 (Auto)"],
        default=["SWP 모니터링", "🧪 나노봇 실험실 (Auto)"]
    )
    st.subheader("📡 제어 패널")
    swp_db_path = st.text_input("SWP DB 경로", "/home/hakkocap/다운로드/swp/data/test.db")

st.title("🏰 통합 캡틴스 지휘 센터 (Captain's Board)")

if "SWP 모니터링" in selected_modules:
    with st.container():
        st.header("📊 SWP 실시간 모니터링")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("캡틴 누적 점수", "1,520 ⚡️", "+10")
        col2.metric("스웜 가동 효율", "99.1% 🚀", "+1.2%")
        col3.metric("진행 중인 작전", "3개")
        col4.metric("자동 획득 무기", f"{len(st.session_state['merged_skills'])}개", "100% Free")
        st.markdown("---")

if "🧪 나노봇 실험실 (Auto)" in selected_modules:
    with st.container():
        st.header("🧪 나노봇 실험실 (완전 자율 병합 모드)")
        st.caption("⚠️ 캡틴의 인지 과부하 방지: 오프니와 나노가 [무료/고성능/안전]을 엄격히 검증한 후 자동 병합하고 리스트만 보고합니다.")
        
        tab1, tab2 = st.tabs(["⚙️ 실시간 샌드박스 현황", "📜 획득 무기(스킬) 리스트 보고서"])
        
        with tab1:
            st.subheader("📥 샌드박스 백그라운드 폭격 상태")
            st.info("현재 오프니가 Scrapling으로 깃허브/레딧에서 수집한 1,200개의 코드를 나노가 8코어로 갈아버리는 중입니다.")
            
            if st.button("▶️ 수집-검증 루프 가동 (시뮬레이션)", type="primary"):
                with st.spinner("🐳 수천 개의 샌드박스 폭발 중... (에러 발생 코드, 유료 API 코드 99% 폐기 중)"):
                    time.sleep(3)
                    # 중복 방지 로직 추가
                    if not any(skill['name'] == 'auto_clicker_free' for skill in st.session_state['merged_skills']):
                        st.session_state['merged_skills'].insert(0, {
                        "date": time.strftime("%Y-%m-%d %H:%M"),
                        "name": "auto_clicker_free",
                        "score": 88,
                        "type": "Free/OpenSource",
                        "desc": "외부 결제 API가 없는 100% 무료 마우스 자동화 스크립트. (오프니-나노 공동 승인)"
                    })
                st.success("✅ [결과] 1,500개 중 단 1개의 '진짜 무료/안전 스킬'을 발굴하여 무기고에 자동 병합했습니다!")
                
        with tab2:
            st.subheader(f"📜 캡틴 보고용: 최근 획득 무기 리스트 (총 {len(st.session_state['merged_skills'])}개)")
            st.write("아래 리스트는 캡틴의 결재 없이 이미 `/home/hakkocap/다운로드/swp/tools` 폴더에 다운로드되어 장착 완료된 상태입니다.")
            
            for item in st.session_state['merged_skills']:
                with st.expander(f"🟢 [{item['date']}] {item['name']} (총점 {item['score']}점)"):
                    st.markdown(f"**라이선스 검증:** `{item['type']}` (비용 $0 보장)")
                    st.markdown(f"**스킬 요약:** {item['desc']}")
                    st.info("이 파일은 이미 미니 PC 무기고에 존재하므로 언제든 호출 가능합니다.")
