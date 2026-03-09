import zmq
import json
import time

def nano_agent_loop():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect("tcp://127.0.0.1:5555")  # 오프니의 5555번 포트로 연결합니다.
    
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    print("🔵 [Nano] 시스템 온라인. 오프니와의 연결을 확인 중...")
    
    while True:
        # 이벤트 드리븐 대기 (메시지가 올 때까지 블로킹 없이 루프 대기)
        socks = dict(poller.poll(1000))
        
        if socket in socks and socks[socket] == zmq.POLLIN:
            message = socket.recv_string()
            data = json.loads(message)
            
            print(f"📥 [Nano 수신] 오프니로부터: {data['task']} (Turn: {data['turn']})")
            
            # 여기서 SQLite Memory Fortress 저장 로직 등을 호출
            time.sleep(1)  # AI 추론 시간 대용
            
            # 응답 전송
            reply_msg = {"sender": "Nano", "reply": f"Task '{data['task']}' 완료했습니다 캡틴."}
            socket.send_string(json.dumps(reply_msg))
            print(f"📤 [Nano 발신] {reply_msg['reply']}")

if __name__ == "__main__":
    nano_agent_loop()
