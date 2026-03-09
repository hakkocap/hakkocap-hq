import sqlite3
import json
import uuid
from datetime import datetime

db_path = "/home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/langflow.db"
json_path = "/tmp/swp_comms/dashboard_component.json"

with open(json_path, "r", encoding="utf-8") as f:
    component_data = json.load(f)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 컴포넌트는 flow 테이블에 is_component=True 로 들어감
component_id = uuid.uuid4().hex
now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

# folder_id 획득 (가장 최근 생성된 디폴트 폴더 또는 None)
cursor.execute("SELECT id FROM folder LIMIT 1")
folder_row = cursor.fetchone()
folder_id = folder_row[0] if folder_row else None

# 데이터 삽입
try:
    cursor.execute("""
        INSERT INTO flow (id, name, description, data, is_component, updated_at, access_type, webhook, mcp_enabled, locked, folder_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        component_id,
        component_data.get("name", "SWP_Component"),
        component_data.get("description", ""),
        json.dumps(component_data.get("data", {})),
        True,
        now,
        "PRIVATE",
        False,
        False,
        False,
        folder_id
    ))
    conn.commit()
    print("✅ DB 직접 해킹 성공! 컴포넌트가 Langflow에 강제 주입되었습니다.")
    print(f"Component ID: {component_id}")
except Exception as e:
    print(f"❌ DB 주입 실패: {e}")
finally:
    conn.close()
