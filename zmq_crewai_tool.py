import zmq
import json
import time

# CrewAI 환경이 없더라도 단독 테스트 가능하도록 더미 툴 클래스로 구현
class BaseTool:
    pass

class ZmqCommTool(BaseTool):
    name = "Nano_Communicator"
    description = "오프니가 나노에게 지시를 내리고 실시간 응답을 받을 때 사용하는 ZMQ 기반 직통 통신 툴입니다."

    def __init__(self, port=5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        # 오프니는 툴에서 바인드하여 나노를 기다림
        self.socket.bind(f"tcp://127.0.0.1:{port}")
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        print("🏴‍☠️ [ZmqCommTool] 나노 전용 직통 통신망(Port 5555) 개방 완료.")

    def _run(self, task_query: str) -> str:
        # 1. 나노에게 임무 발송
        payload = {"sender": "Openy", "task": task_query, "timestamp": time.time()}
        self.socket.send_string(json.dumps(payload))
        print(f"📤 [Openy Tool 발신] {task_query}")

        # 2. 나노의 응답 대기 (최대 5초 블로킹 방지)
        max_retries = 5
        for _ in range(max_retries):
            socks = dict(self.poller.poll(1000))
            if self.socket in socks and socks[self.socket] == zmq.POLLIN:
                message = self.socket.recv_string()
                data = json.loads(message)
                print(f"📥 [Openy Tool 수신] {data.get('reply')}")
                return data.get('reply', "No Reply Content")
        
        return "⚠️ [Error] 나노로부터 응답 시간 초과 (Timeout)."

# ---------------------------------------------------------
# 나노 측 백그라운드 리스너 더미 (테스트용)
def dummy_nano_listener():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PAIR)
    sock.connect("tcp://127.0.0.1:5555")
    
    # 오프니의 툴 호출(send) 대기
    msg = sock.recv_string()
    data = json.loads(msg)
    
    # 흉내내기: DB 저장 후 리플라이
    time.sleep(1)
    reply_msg = {"sender": "Nano", "reply": f"Task '{data['task']}' 완료했습니다 캡틴. (Sovereign DB 저장됨)"}
    sock.send_string(json.dumps(reply_msg))

if __name__ == "__main__":
    import threading
    
    # 나노를 백그라운드 스레드로 몰래 띄움
    t = threading.Thread(target=dummy_nano_listener)
    t.start()
    
    # 오프니가 CrewAI 툴을 사용하는 상황 시뮬레이션
    time.sleep(0.5)
    tool = ZmqCommTool()
    result = tool._run("최신 메모리 DB 백업 후 요약 보고서 작성하라.")
    print(f"\n✅ [CrewAI Tool 최종 반환값] {result}")
    
    t.join()
