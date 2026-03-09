import asyncio
import websockets
import json
import zmq
import zmq.asyncio
from datetime import datetime

class RealtimeSyncManager:
    def __init__(self, websocket_port=8765, zmq_port=5556):
        self.connections = set()
        self.ws_port = websocket_port
        
        # ZeroMQ 비동기 컨텍스트 설정 (오프니 매니저의 라우터 포트 감청용)
        self.context = zmq.asyncio.Context()
        self.zmq_socket = self.context.socket(zmq.SUB)
        self.zmq_socket.connect(f"tcp://127.0.0.1:{zmq_port}")
        self.zmq_socket.setsockopt_string(zmq.SUBSCRIBE, "") # 모든 메시지 수신
        
        print(f"📡 [SyncManager] WebSocket 서버 ({self.ws_port}) 및 ZMQ 리스너 ({zmq_port}) 초기화 완료.")

    async def register(self, websocket):
        self.connections.add(websocket)
        print(f"✅ [SyncManager] 클라이언트 접속. (현재 {len(self.connections)}명)")

    async def unregister(self, websocket):
        self.connections.remove(websocket)
        print(f"❌ [SyncManager] 클라이언트 연결 해제. (현재 {len(self.connections)}명)")

    async def ws_handler(self, websocket, path):
        await self.register(websocket)
        try:
            async for message in websocket:
                # 클라이언트에서 수동 트리거 등의 메시지가 오면 처리
                data = json.loads(message)
                print(f"📩 [WS 수신] 클라이언트 요청: {data}")
                
                # 테스트 응답
                await websocket.send(json.dumps({"status": "ack", "msg": "요청 접수 완료"}))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def zmq_to_ws_bridge(self):
        """ZMQ 네트워크에서 스웜/SWP 이벤트가 발생하면 웹소켓 클라이언트들에게 뿌림"""
        while True:
            # ZMQ에서 메시지 비동기 수신 대기
            message = await self.zmq_socket.recv_string()
            
            # 통합 데이터 패키징 (UI에 즉시 반영될 데이터)
            update_package = {
                "timestamp": datetime.now().isoformat(),
                "event_source": "ZMQ_Swarm",
                "payload": message
            }
            
            # 접속된 모든 프론트엔드/대시보드에 브로드캐스트
            if self.connections:
                await asyncio.gather(
                    *[ws.send(json.dumps(update_package)) for ws in self.connections]
                )
                print(f"📤 [WS 발신] {len(self.connections)}개의 클라이언트에 실시간 이벤트 브로드캐스트 완료.")

    async def start(self):
        # 1. 웹소켓 서버 시작
        ws_server = await websockets.serve(self.ws_handler, "localhost", self.ws_port)
        print(f"🚀 [SyncManager] WebSocket 브로드캐스터 가동 중... (ws://localhost:{self.ws_port})")
        
        # 2. ZMQ 감청 브릿지 태스크 병렬 실행
        await asyncio.gather(
            self.zmq_to_ws_bridge()
        )

if __name__ == "__main__":
    manager = RealtimeSyncManager()
    asyncio.run(manager.start())
