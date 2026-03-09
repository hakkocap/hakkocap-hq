import zmq
import json
import time
import psutil
import os

def memory_usage_test():
    """ZeroMQ 메모리 사용량 테스트"""
    context = zmq.Context()
    
    # 서버 프로세스
    server_pid = os.getpid()
    print(f"✅ 서버 PID: {server_pid}")
    
    server = context.socket(zmq.PAIR)
    server.bind("tcp://127.0.0.1:5557")
    
    # 초기 메모리 사용량
    initial_memory = psutil.Process(server_pid).memory_info().rss / 1024 / 1024  # MB
    
    poller = zmq.Poller()
    poller.register(server, zmq.POLLIN)
    
    messages_processed = 0
    memory_samples = []
    
    # 클라이언트 연결 대기
    print("클라이언트 연결 대기 중...")
    
    while messages_processed < 50:
        socks = dict(poller.poll(1000))
        if server in socks:
            msg = server.recv_string()
            messages_processed += 1
            
            # 메모리 사용량 샘플링
            if messages_processed % 10 == 0:
                current_memory = psutil.Process(server_pid).memory_info().rss / 1024 / 1024
                memory_samples.append(current_memory)
                print(f"  메시지 {messages_processed} 처리 후: {current_memory:.2f}MB")
            
            # 응답
            server.send_string(json.dumps({"status": "processed", "count": messages_processed}))
    
    # 최종 메모리 사용량
    final_memory = psutil.Process(server_pid).memory_info().rss / 1024 / 1024
    
    print(f"\n=== 메모리 사용량 결과 ===")
    print(f"초기 메모리: {initial_memory:.2f}MB")
    print(f"최종 메모리: {final_memory:.2f}MB")
    print(f"메모리 증가: {final_memory - initial_memory:.2f}MB")
    print(f"평균 메모리: {sum(memory_samples)/len(memory_samples):.2f}MB" if memory_samples else "샘플 없음")
    
    server.close()
    context.term()

if __name__ == "__main__":
    memory_usage_test()
