from crewai.tools import BaseTool
from typing import Type
import zmq
import json
import time

class ZmqCommTool(BaseTool):
    name: str = "ZMQ Communication Tool"
    description: str = "ZeroMQ를 통해 다른 에이전트와 통신하는 도구"
    args_schema: Type = None  # 필요시 Pydantic 모델 정의
    
    def __init__(self, agent_name: str = "Nano", port: int = 5555):
        super().__init__()
        self.agent_name = agent_name
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        
        if agent_name.lower() == "openy":
            # 오프니: 서버 모드 (bind)
            self.socket.bind(f"tcp://127.0.0.1:{port}")
            print(f"🟢 [{agent_name}] ZMQ 서버 시작 (포트: {port})")
        else:
            # 나노: 클라이언트 모드 (connect)
            self.socket.connect(f"tcp://127.0.0.1:{port}")
            print(f"🔵 [{agent_name}] ZMQ 클라이언트 연결 (포트: {port})")
    
    def _run(self, message: str, timeout_ms: int = 5000) -> str:
        """메시지 전송 및 응답 수신"""
        try:
            # 메시지 전송
            payload = {
                "sender": self.agent_name,
                "message": message,
                "timestamp": time.time()
            }
            self.socket.send_string(json.dumps(payload))
            print(f"📤 [{self.agent_name} 발신] {message}")
            
            # 응답 대기 (폴링)
            poller = zmq.Poller()
            poller.register(self.socket, zmq.POLLIN)
            
            socks = dict(poller.poll(timeout_ms))
            if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                response = self.socket.recv_string()
                data = json.loads(response)
                print(f"📥 [{self.agent_name} 수신] {data.get('reply', 'No reply')}")
                return data.get("reply", "응답 없음")
            else:
                return "타임아웃: 응답 없음"
                
        except Exception as e:
            return f"통신 오류: {str(e)}"
    
    def close(self):
        """소켓 정리"""
        self.socket.close()
        self.context.term()
        print(f"🔴 [{self.agent_name}] ZMQ 연결 종료")

# 사용 예시
if __name__ == "__main__":
    # 오프니 툴 생성
    openy_tool = ZmqCommTool(agent_name="Openy", port=5556)
    
    # 나노 툴 생성
    nano_tool = ZmqCommTool(agent_name="Nano", port=5556)
    
    # 테스트 통신
    response = nano_tool._run("안녕 오프니, 작업 상태는?")
    print(f"나노 응답: {response}")
    
    # 정리
    openy_tool.close()
    nano_tool.close()
