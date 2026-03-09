import zmq
import json
import time

def test_basic_zmq():
    """기본 ZeroMQ 통신 테스트"""
    context = zmq.Context()
    
    # 서버 (ROUTER 패턴)
    server = context.socket(zmq.ROUTER)
    server.bind("tcp://127.0.0.1:5557")
    
    # 클라이언트 (DEALER 패턴)
    client = context.socket(zmq.DEALER)
    client.identity = b"TestClient"
    client.connect("tcp://127.0.0.1:5557")
    
    # 클라이언트 메시지 전송
    client.send_string("Hello from Client")
    
    # 서버 응답 수신
    poller = zmq.Poller()
    poller.register(server, zmq.POLLIN)
    
    socks = dict(poller.poll(1000))
    if server in socks:
        identity = server.recv()
        message = server.recv_string()
        print(f"✅ 서버 수신: 클라이언트 {identity.decode()} -> {message}")
        
        # 응답 전송
        server.send(identity, zmq.SNDMORE)
        server.send_string("Hello from Server")
        print("✅ 서버 응답 전송")
    
    # 클라이언트 응답 수신
    poller = zmq.Poller()
    poller.register(client, zmq.POLLIN)
    
    socks = dict(poller.poll(1000))
    if client in socks:
        response = client.recv_string()
        print(f"✅ 클라이언트 수신: {response}")
    
    server.close()
    client.close()
    context.term()
    print("✅ 기본 ZeroMQ 통신 테스트 완료")

if __name__ == "__main__":
    test_basic_zmq()
