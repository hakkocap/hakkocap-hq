import sqlite3
import datetime

conn = sqlite3.connect('/tmp/swp_comms/ghost_memory.db')
cursor = conn.cursor()

# 테스트 데이터 삽입
test_memories = [
    ("캡틴이 Langflow 대시보드 프로젝트를 성공적으로 완료했다.", "프로젝트"),
    ("Ryzen 9 미니 PC의 성능이 Sovereign Memory Fortress 구축에 적합하다.", "하드웨어"),
    ("한국어 모델 jhgan/ko-sroberta-multitask를 채택하기로 결정했다.", "기술"),
    ("데이터 주권 100%를 위한 로컬 벡터 DB 구축이 진행 중이다.", "전략"),
    ("오프니와 나노의 협력이 프로젝트 진행 속도를 크게 높였다.", "협력")
]

for content, category in test_memories:
    cursor.execute(
        "INSERT INTO long_term_memory (content, category) VALUES (?, ?)",
        (content, category)
    )

# 사용자 프로필 데이터
profile_data = [
    ("latest_interest", "로컬 AI 인프라"),
    ("technical_focus", "한국어 NLP"),
    ("project_priority", "데이터 주권"),
    ("collaboration_style", "오프니-나노 역할 분담"),
    ("hardware_status", "Ryzen 9 미니 PC 가동 중")
]

for key, value in profile_data:
    cursor.execute(
        "INSERT OR REPLACE INTO user_profile (key, value) VALUES (?, ?)",
        (key, value)
    )

conn.commit()
conn.close()
print("✅ 테스트 데이터 5건 삽입 완료")
