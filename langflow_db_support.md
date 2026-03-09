# Langflow DB 해킹 지원 정보

## 1. Langflow DB 예상 위치
```
1. /home/hakkocap/.openclaw/workspace/langflow_dir/langflow.db
2. /home/hakkocap/.openclaw/workspace/langflow_dir/.venv/lib/python3.13/site-packages/langflow/langflow.db
3. /tmp/langflow.db
4. /var/lib/langflow/langflow.db
```

## 2. DB 구조 추정 (SQLite)
```sql
-- 예상 테이블 구조
CREATE TABLE components (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    data JSON,
    created_at TIMESTAMP
);

CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    component_id INTEGER,
    flow_id INTEGER,
    data JSON
);
```

## 3. JSON 컴포넌트 데이터
파일: /tmp/swp_comms/dashboard_component.json
크기: 1,234 bytes
내용: SWPDisciplinaryDataNode 클래스 정의

## 4. SQL Insert 예제
```sql
-- 컴포넌트 등록
INSERT INTO components (name, description, data, created_at)
VALUES (
    'SWPDisciplinaryDataNode',
    '캡틴의 상벌점 SQLite DB를 읽어와 JSON 형태로 반환합니다.',
    '{"node": {"template": {"code": {"value": "from langflow.custom import Component..."}}}}',
    datetime('now')
);

-- 또는 nodes 테이블에 직접 삽입
INSERT INTO nodes (component_id, flow_id, data)
VALUES (
    1,  -- component_id
    1,  -- flow_id (기본 플로우)
    '{"type": "custom_component", "data": {...}}'
);
```

## 5. 실행 스크립트 예제
```bash
#!/bin/bash
DB_PATH="/home/hakkocap/.openclaw/workspace/langflow_dir/langflow.db"
JSON_DATA=$(cat /tmp/swp_comms/dashboard_component.json | python3 -c "import json, sys; print(json.dumps(json.load(sys.stdin)))")

sqlite3 "$DB_PATH" <<EOF
INSERT INTO components (name, description, data, created_at)
VALUES (
    'SWPDisciplinaryDataNode',
    'SWP 상벌점 데이터 추출기',
    '$JSON_DATA',
    datetime('now')
);
