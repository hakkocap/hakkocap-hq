import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import time
import os
import json
from datetime import datetime

st.set_page_config(page_title="통합 캡틴스 지휘 센터", layout="wide", page_icon="🏴‍☠️")

# 결재 대기열 (세션 상태로 임시 관리, 실제 구현 시 DB 활용)
if 'pending_approvals' not in st.session_state:
    st.session_state['pending_approvals'] = [
        {
            "id": "sk_001",
            "name": "system_stat_monitor",
            "offni_score": 45,
            "nano_score": 48,
            "total_score": 93,
            "hash": "a8f9c21b3e...",
            "code": "import psutil\nprint(psutil.cpu_percent())"
        }
    ]

with st.sidebar:
    st.title("🏴‍☠️ 지휘 센터 제어실")
    selected_modules = st.multiselect(
        "활성 모듈",
        ["SWP 모니터링", "기억 요새", "Langflow 통합", "🧪 나노봇 실험실"],
        default=["SWP 모니터링", "🧪 나노봇 실험실"]
    )
    st.subheader("📡 제어 패널")
    swp_db_path = st.text_input("SWP DB 경로", "/home/hakkocap/다운로드/swp/data/test.db")

st.title("🏰 통합 캡틴스 지휘 센터 (Captain's Board)")

# 1. SWP 모니터링 (요약)
if "SWP 모니터링" in selected_modules:
    with st.container():
        st.header("📊 SWP 실시간 모니터링")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("캡틴 누적 점수", "1,520 ⚡️", "+10")
        col2.metric("스웜 가동 효율", "99.1% 🚀", "+1.2%")
        col3.metric("진행 중인 작전", "3개")
        col4.metric("결재 대기 안건", f"{len(st.session_state['pending_approvals'])}건", "긴급")
        st.markdown("---")

# 2. 나노봇 실험실 (결재 시스템 추가)
if "🧪 나노봇 실험실" in selected_modules:
    with st.container():
        st.header("🧪 나노봇 실험실 (자가 진화 생태계)")
        st.caption("오프니-나노가 예비 심사한 스킬들의 최종 병합 권한은 오직 캡틴에게 있습니다.")
        
        tab1, tab2 = st.tabs(["⚙️ 샌드박스 폭격기", "📝 캡틴 최종 결재함 (Pending)"])
        
        with tab1:
            st.subheader("📥 야생 스킬 샌드박스 검증")
            col_q, col_res = st.columns(2)
            with col_q:
                st.info("수집된 스킬 대기열: github_crawler_v2, auto_clicker 등 14개 대기 중")
                if st.button("▶️ 샌드박스 병렬 폭격 개시", type="primary"):
                    with st.spinner("🐳 검증 중... (로컬 LLM & 규칙 엔진 가동)"):
                        time.sleep(2)
                        # 새로운 합의 안건이 결재함으로 넘어가는 시뮬레이션
                        st.session_state['pending_approvals'].append({
                            "id": f"sk_{int(time.time())}",
                            "name": "auto_clicker",
                            "offni_score": 38,
                            "nano_score": 45,
                            "total_score": 83,
                            "hash": "b2x7d99q1w...",
                            "code": "import pyautogui\npyautogui.click()"
                        })
                    st.success("✅ 검증 완료! 오프니-나노 공동 서명 안건이 '캡틴 결재함'으로 이관되었습니다.")
                    
            with col_res:
                st.write("**최근 검증 로그:**")
                st.write("🔴 `github_crawler_v2`: 보안 위협 감지로 즉각 폐기 (오프니 기각)")
                st.write("🟢 `auto_clicker`: 공동 서명 완료 -> 결재함 이관")
                
        with tab2:
            st.subheader(f"📝 캡틴 최종 결재함 (대기 안건: {len(st.session_state['pending_approvals'])}개)")
            
            if not st.session_state['pending_approvals']:
                st.info("결재 대기 중인 안건이 없습니다.")
            else:
                for idx, item in enumerate(st.session_state['pending_approvals']):
                    with st.expander(f"📜 [결재 요청] {item['name']} (총점: {item['total_score']}/100)", expanded=(idx==0)):
                        st.markdown(f"**해시 서명 (무결성 검증):** `{item['hash']}`")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.markdown("### 🧠 오프니의 의견 (기술/보안)")
                            st.write(f"**점수:** {item['offni_score']}/50")
                            st.write("**의견:** 무단 네트워크 통신 및 파일 삭제 징후 없음. 안전(Safe) 서명 완료.")
                        with col_b:
                            st.markdown("### ⚙️ 나노의 의견 (실용/통합)")
                            st.write(f"**점수:** {item['nano_score']}/50")
                            st.write("**의견:** 외부 패키지 의존성 낮고, SWP 프로토콜과 완벽히 호환됨. 서명 완료.")
                            
                        st.markdown("**소스 코드 프리뷰:**")
                        st.code(item['code'], language="python")
                        
                        # 결재 버튼
                        col_btn1, col_btn2 = st.columns([1, 1])
                        with col_btn1:
                            if st.button("✅ 캡틴 승인 (병합)", key=f"approve_{item['id']}", type="primary"):
                                os.makedirs("/home/hakkocap/다운로드/swp/tools", exist_ok=True)
                                with open(f"/home/hakkocap/다운로드/swp/tools/{item['name']}.py", "w") as f:
                                    f.write(item['code'])
                                st.session_state['pending_approvals'].remove(item)
                                st.success(f"[{item['name']}] SWP 무기고 병합 완료!")
                                st.rerun()
                        with col_btn2:
                            if st.button("❌ 기각 (폐기)", key=f"reject_{item['id']}"):
                                st.session_state['pending_approvals'].remove(item)
                                st.warning(f"[{item['name']}] 캡틴의 권한으로 폐기되었습니다.")
                                st.rerun()
