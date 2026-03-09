import zmq
import json
import time
import threading

def performance_test():
    """ZeroMQ 성능 측정 테스트"""
    context = zmq.Context()
    
    # 서버 스레드
    def server_thread():
        server = context.socket(zmq.PAIR)
        server.bind("tcp://127.0.0.1:5556")
        
        poller = zmq.Poller()
        poller.register(server, zmq.POLLIN)
        
        messages_received = 0
        start_time = time.time()
        
        while messages_received < 100:
            socks = dict(poller.poll(1000))
            if server in socks:
                msg = server.recv_string()
                messages_received += 1
                # 즉시 응답
                server.send_string(json.dumps({"response": "ok", "count": messages_received}))
        
        end_time = time.time()
        print(f"✅ 서버: {messages_received} 메시지 처리")
        print(f"   처리 시간: {end_time - start_time:.3f}초")
        print(f"   평균 지연: {(end_time - start_time) / messages_received * 1000:.2f}ms")
    
    # 클라이언트 스레드
    def client_thread():
        client = context.socket(zmq.PAIR)
        client.connect("tcp://127.0.0.1:5556")
        
        messages_sent = 0
        latencies = []
        
        for i in range(100):
            start = time.time()
            client.send_string(json.dumps({"message": f"test_{i}"}))
            
            # 응답 대기
            poller = zmq.Poller()
            poller.register(client, zmq.POLLIN)
            socks = dict(poller.poll(1000))
            if client in socks:
                response = client.recv_string()
                end = time.time()
                latencies.append((end - start) * 1000)  # ms 단위
                messages_sent += 1
        
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
            max_latency = max(latencies)
            min_latency = min(latencies)
            print(f"✅ 클라이언트: {messages_sent} 메시지 전송")
            print(f"   평균 지연: {avg_latency:.2f}ms")
            print(f"   최대 지연: {max_latency:.2f}ms")
            print(f"   최소 지연: {min_latency:.2f}ms")
    
    # 테스트 실행
    print("=== ZeroMQ 성능 측정 시작 ===")
    server = threading.Thread(target=server_thread)
    client = threading.Thread(target=client_thread)
    
    server.start()
    time.sleep(1)  # 서버 준비 대기
    client.start()
    
    server.join()
    client.join()
    print("=== 성능 측정 완료 ===")

if __name__ == "__main__":
    performance_test()
