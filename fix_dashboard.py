with open("/tmp/swp_comms/integrated_dashboard_v5.py", "r") as f:
    lines = f.readlines()

with open("/tmp/swp_comms/integrated_dashboard_v5.py", "w") as f:
    for line in lines:
        if "st.session_state['merged_skills'].insert(0," in line:
            f.write("""                    # 중복 방지 로직 추가
                    if not any(skill['name'] == 'auto_clicker_free' for skill in st.session_state['merged_skills']):
                        st.session_state['merged_skills'].insert(0, {
""")
        else:
            f.write(line)
