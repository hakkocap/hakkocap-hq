import zmq
import json
import time

def swarm_manager():
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind("tcp://127.0.0.1:5556")
    
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    print("🏴‍☠️ [Openy Manager] Swarm ROUTER 개방 (Port 5556). 나노 군단의 연결을 기다립니다...")

    # 나노 군단에게 브로드캐스트할 수 없으므로, 먼저 워커들의 'Ready' 신호를 수집하여 주소를 기억함
    active_workers = set()
    
    # 3명의 워커가 접속할 때까지 대기
    while len(active_workers) < 3:
        socks = dict(poller.poll(2000))
        if socket in socks and socks[socket] == zmq.POLLIN:
            # ROUTER 소켓은 [Identity, Empty, Data] 형태로 받음
            identity, empty, message = socket.recv_multipart()
            data = json.loads(message.decode())
            if data.get("status") == "Ready":
                worker_id = identity.decode()
                active_workers.add(worker_id)
                print(f"✅ [Manager] 나노봇 합류 감지: {worker_id} (현재 {len(active_workers)}/3)")

    print("\n🚀 [Openy Manager] 3기의 나노봇 군단 집결 완료! 임무 하달 시작.")
    
    # 각 워커에게 개별 임무 하달
    tasks = ["섹터 A 데이터 크롤링", "섹터 B 시스템 보안 점검", "섹터 C 로그 백업"]
    for worker_id, task in zip(list(active_workers), tasks):
        payload = {"task": task, "urgency": "High"}
        # ROUTER는 특정 워커(identity)에게 메시지를 쏠 수 있음
        socket.send_multipart([worker_id.encode(), b"", json.dumps(payload).encode()])
        print(f"📤 [Manager -> {worker_id}] 지시: {task}")

    # 군단의 결과 취합
    completed = 0
    while completed < 3:
        socks = dict(poller.poll(5000))
        if socket in socks and socks[socket] == zmq.POLLIN:
            identity, empty, message = socket.recv_multipart()
            data = json.loads(message.decode())
            print(f"📥 [Manager 수신] {identity.decode()} 보고: {data['result']}")
            completed += 1
            
    print("🏆 [Openy Manager] 군단(Swarm) 임무 100% 완료! 세션 종료.")

if __name__ == "__main__":
    swarm_manager()
