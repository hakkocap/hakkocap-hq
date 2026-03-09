# Langflow Custom Component Node
# 오프니 작성: 상벌점 데이터 추출 가상 노드 (테스트용)

from langflow.custom import Component
from langflow.io import Output, MessageTextInput
import json
import os
import sqlite3

class SWPDisciplinaryDataNode(Component):
    display_name = "SWP 상벌점 데이터 추출기"
    description = "캡틴의 상벌점 SQLite DB를 읽어와 JSON 형태로 반환합니다."

    inputs = [
        MessageTextInput(name="db_path", display_name="DB 경로", value="/home/hakkocap/다운로드/swp/data/test.db"),
    ]

    outputs = [
        Output(display_name="Data JSON", name="data_json", method="fetch_data"),
    ]

    def fetch_data(self) -> str:
        # 실제 DB 연동 전 하드코딩 테스트 데이터 (DB가 비어있거나 스키마를 모를 경우 대비)
        test_data = {
            "status": "success",
            "captain_score": 1500,
            "nanobot_efficiency": "98%",
            "recent_actions": [
                {"action": "Langflow 부활 작전", "score": "+50"},
                {"action": "과거 Tabler 실패 분석", "score": "+20"}
            ]
        }
        
        # 실제 DB 연결 로직 (향후 활성화)
        # conn = sqlite3.connect(self.db_path)
        # cursor = conn.cursor()
        # cursor.execute("SELECT * FROM scores LIMIT 10")
        # rows = cursor.fetchall()
        # test_data["db_rows"] = rows
        
        return json.dumps(test_data, ensure_ascii=False)
