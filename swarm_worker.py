import zmq
import json
import time
import sys
import random

def nano_worker(worker_id):
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    # DEALER 소켓의 Identity를 고유하게 설정하여 ROUTER가 식별하게 함
    socket.setsockopt_string(zmq.IDENTITY, worker_id)
    socket.connect("tcp://127.0.0.1:5556")
    
    print(f"🤖 [{worker_id}] 시스템 기동 완료. 매니저(오프니)에게 연결을 시도합니다.")

    # Manager에게 생존 신고 (빈 프레임과 함께 전송)
    ready_msg = {"status": "Ready", "worker": worker_id}
    socket.send_multipart([b"", json.dumps(ready_msg).encode()])

    # 임무 수신 대기
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(1000))
        if socket in socks and socks[socket] == zmq.POLLIN:
            empty, message = socket.recv_multipart()
            data = json.loads(message.decode())
            task = data.get("task")
            
            print(f"📥 [{worker_id}] 임무 수신: {task}")
            
            # 가상의 임무 수행 시간
            time.sleep(random.uniform(1.0, 2.5))
            
            # 임무 완료 보고
            reply_msg = {"result": f"[{task}] 타격 및 임무 완수 (에러 없음)"}
            socket.send_multipart([b"", json.dumps(reply_msg).encode()])
            print(f"📤 [{worker_id}] 완료 보고 송신.")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python swarm_worker.py <Worker_ID>")
        sys.exit(1)
    nano_worker(sys.argv[1])
