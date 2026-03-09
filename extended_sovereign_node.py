import json
import sqlite3

class IntegratedSWPNode:
    display_name = "SWP 통합 노드 (ZeroMQ 연동)"
    
    def __init__(self):
        self.db_path = "/home/hakkocap/다운로드/swp/data/test.db"

    def build(self, operation: str, query: str = "") -> str:
        result_payload = {}
        
        if operation == "get_captain_metrics":
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("SELECT captain_score FROM disciplinary_log ORDER BY timestamp DESC LIMIT 1")
                score = c.fetchone()
                result_payload["captain_score"] = score[0] if score else "N/A"
                conn.close()
            except Exception as e:
                result_payload["error"] = str(e)
                
        elif operation == "trigger_swarm":
            # 실제 ZMQ import/실행은 에이전트/매니저 루프가 켜져 있을 때만 작동하도록 래핑
            try:
                import zmq
                context = zmq.Context()
                socket = context.socket(zmq.PUB) # PUB으로 변경하여 연결 상관없이 쏠 수 있게 함
                socket.connect("tcp://127.0.0.1:5556")
                socket.send_string(json.dumps({"action": "langflow_trigger", "query": query}))
                socket.close(linger=0)
                context.term()
                result_payload["swarm_status"] = "ZMQ Signal Sent to Swarm Manager"
            except Exception as e:
                result_payload["error"] = f"ZMQ 전송 에러: {e}"
                
        return json.dumps(result_payload, ensure_ascii=False)

if __name__ == "__main__":
    node = IntegratedSWPNode()
    print("1. Metrics 테스트:", node.build(operation="get_captain_metrics"))
    print("2. Swarm 트리거 테스트:", node.build(operation="trigger_swarm", query="섹터 D 점검"))
