import subprocess
import time
import requests

def restart_and_check():
    print("🔄 Langflow 서버 재시작 시도 중...")
    
    # 프로세스 찾아서 죽이기 (langflow 실행 프로세스)
    try:
        pids = subprocess.check_output(["pgrep", "-f", "langflow"]).decode("utf-8").split()
        for pid in pids:
            subprocess.run(["kill", "-9", pid])
        print("✅ 기존 Langflow 프로세스 종료 완료.")
    except Exception:
        print("ℹ️ 실행 중인 Langflow 프로세스가 없거나 종료할 수 없습니다.")
        
    time.sleep(2)
    
    # 백그라운드로 다시 실행
    try:
        # venv 환경 내의 langflow 실행
        cmd = "nohup /home/hakkocap/.openclaw/workspace/langflow_dir/.venv/bin/langflow run > /tmp/swp_comms/langflow_restart.log 2>&1 &"
        subprocess.run(cmd, shell=True)
        print("✅ Langflow 백그라운드 재시작 명령 하달 완료.")
    except Exception as e:
        print(f"❌ 재시작 실패: {e}")
        return

    print("⏳ 서버 기동 대기 중 (10초)...")
    for i in range(10):
        time.sleep(1)
        try:
            res = requests.get("http://localhost:7860")
            if res.status_code == 200:
                print(f"✅ Langflow 서버 정상 접속 확인! (소요시간: {i+1}초)")
                return
        except requests.exceptions.ConnectionError:
            pass
    print("⚠️ 서버 접속 대기 시간 초과. 로그를 확인하세요.")

if __name__ == "__main__":
    restart_and_check()
