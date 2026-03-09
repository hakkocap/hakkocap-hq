import zmq
import json
import time

def openy_agent_loop():
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://127.0.0.1:5555")  # 오프니가 5555번 포트 직통선을 엽니다.
    
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    print("🟢 [Openy] Sovereign Protocol 작동 준비. 나노의 연결을 기다립니다...")
    
    turn_count = 0
    max_turns = 5

    # 선제 공격 (오프니가 먼저 메시지를 보냄)
    initial_msg = {"sender": "Openy", "task": "Wake up, Nano!", "turn": turn_count}
    socket.send_string(json.dumps(initial_msg))
    print(f"📤 [Openy 발신] {initial_msg['task']}")

    while turn_count < max_turns:
        # 이벤트 드리븐: 콜백 대신 소켓에 메시지가 도착했는지 감지 (Timeout 1000ms)
        socks = dict(poller.poll(1000))
        
        if socket in socks and socks[socket] == zmq.POLLIN:
            message = socket.recv_string()
            data = json.loads(message)
            print(f"📥 [Openy 수신] 나노로부터: {data['reply']}")
            
            turn_count += 1
            time.sleep(1)  # AI 추론 시간 대용 (CrewAI 로직이 들어갈 부분)

            if turn_count < max_turns:
                reply_msg = {"sender": "Openy", "task": f"Next task {turn_count}", "turn": turn_count}
                socket.send_string(json.dumps(reply_msg))
                print(f"📤 [Openy 발신] {reply_msg['task']}")
            else:
                print("🛑 [Protocol] 무한 루프 방지: 5회 통신 도달. 세션 종료.")
                break

if __name__ == "__main__":
    openy_agent_loop()
