import docker
import time

def test_docker_sandbox():
    """간단한 Docker 샌드박스 테스트"""
    try:
        client = docker.from_env()
        print(f"✅ Docker 연결 성공: {client.version()}")
        
        # 간단한 컨테이너 실행 테스트
        container = client.containers.run(
            "python:3.11-slim",
            command="python -c \"print('나노봇 실험실 테스트 성공!')\"",
            mem_limit="256m",
            cpu_quota=25000,
            network_disabled=True,
            detach=True
        )
        
        # 결과 대기
        result = container.wait(timeout=10)
        logs = container.logs().decode('utf-8')
        container.remove()
        
        print(f"✅ 컨테이너 실행 성공: {logs.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Docker 테스트 실패: {str(e)}")
        return False

if __name__ == "__main__":
    test_docker_sandbox()
