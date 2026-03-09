import sqlite3
import os

DB_PATH = "/home/hakkocap/다운로드/swp/data/test.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. 징계/상점 로그 테이블
cursor.execute('''
CREATE TABLE IF NOT EXISTS disciplinary_log (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 crew_id INTEGER,
 action_type TEXT,
 points INTEGER,
 description TEXT,
 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
 captain_score INTEGER
)
''')

# 2. 크루 테이블
cursor.execute('''
CREATE TABLE IF NOT EXISTS crew_members (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT,
 role TEXT,
 current_score INTEGER,
 efficiency_rating REAL
)
''')

# 3. 프로젝트 테이블
cursor.execute('''
CREATE TABLE IF NOT EXISTS project_status (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 project_name TEXT,
 status TEXT,
 progress_percent INTEGER,
 last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# 더미 데이터 삽입 (비어있을 경우)
cursor.execute("SELECT COUNT(*) FROM crew_members")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO crew_members (name, role, current_score, efficiency_rating) VALUES ('나노', '분석 에이전트', 100, 0.98)")
    cursor.execute("INSERT INTO crew_members (name, role, current_score, efficiency_rating) VALUES ('오프니', '행동 에이전트', 80, 0.95)")
    
    cursor.execute("INSERT INTO project_status (project_name, status, progress_percent) VALUES ('Sovereign Memory Fortress', '진행중', 80)")
    cursor.execute("INSERT INTO project_status (project_name, status, progress_percent) VALUES ('Langflow 동적 파이프라인', '완료', 100)")
    
    cursor.execute("INSERT INTO disciplinary_log (crew_id, action_type, points, description, captain_score) VALUES (1, '상점', 10, '아키텍처 설계 우수', 1510)")
    cursor.execute("INSERT INTO disciplinary_log (crew_id, action_type, points, description, captain_score) VALUES (2, '상점', 20, '신속한 ZMQ 돌파', 1530)")

conn.commit()
conn.close()
print("✅ [완료] SWP test.db 구조 셋업 및 초기 데이터 주입 완료.")
