import docker
import json
import time
import os
import google.generativeai as genai

# API 키는 환경 변수에서 로드 (실행 시 주입 필요)
GENAI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
    # 구버전 gemini-1.5-pro 모델 또는 gemini-3.1-pro-preview가 있다면 사용 (현재는 1.5-pro로 테스트 안전)
    model = genai.GenerativeModel('gemini-1.5-pro-latest') 
else:
    model = None
    print("⚠️ [경고] GEMINI_API_KEY가 설정되지 않았습니다. 평가 단계는 Mock 데이터로 진행됩니다.")

try:
    client = docker.from_env()
except Exception as e:
    print(f"⚠️ [경고] Docker 데몬에 연결할 수 없습니다. Docker 권한을 확인하세요: {e}")
    client = None

def send_telegram_to_captain(msg):
    # OpenClaw의 `message` 툴로 처리할 수 있도록 뼈대만 잡아둠
    print(f"📡 [텔레그램 발송 뼈대] 캡틴에게 전송: {msg}")

def merge_to_swp(skill_name, code):
    # 메인 Sovereign Workflow Protocol 디렉토리에 저장 및 SQLite 등록 로직
    os.makedirs("/home/hakkocap/다운로드/swp/tools", exist_ok=True)
    file_path = f"/home/hakkocap/다운로드/swp/tools/{skill_name}.py"
    with open(file_path, "w") as f:
        f.write(code)
    print(f"✅ [{skill_name}] 메인 프로토콜 병합 완료. (경로: {file_path})")

def run_sandbox_and_evaluate(skill_name, code_content):
    print(f"\n🔬 [나노봇 실험실] '{skill_name}' 샌드박스 테스트 시작...")
    
    if not client:
        return {"status": "error", "reason": "Docker not available"}

    # 1. Docker 컨테이너 실행 (리소스 제한 및 타임아웃 적용)
    try:
        print(f"🐳 [Docker] 컨테이너 실행 중... (제한: 메모리 512m, CPU 0.5)")
        # 작은 따옴표 이스케이프 처리하여 커맨드 작성
        safe_code = code_content.replace('"', '\\"')
        container = client.containers.run(
            "python:3.11-slim",
            command=f'python -c "{safe_code}"',
            mem_limit="512m",
            cpu_quota=50000, # CPU 0.5 코어 제한
            network_disabled=True, # 1차 테스트는 오프라인(보안)
            detach=True
        )
        
        # 5분 타임아웃 대기
        result = container.wait(timeout=300) 
        logs = container.logs().decode('utf-8')
        container.remove(force=True)
        print(f"🐳 [Docker] 컨테이너 실행 종료. 로그 수집 완료. (Exit code: {result.get('StatusCode')})")
        
    except Exception as e:
        logs = f"에러 발생: {str(e)}"
        print(f"🐳 [Docker Error] {logs}")
    
    # 2. Gemini 평가 (Mock or Real)
    if not model:
        # Mock Response
        print("⚖️ [최종 판사 Gemini] API 키 없음. Mock 판결 진행.")
        decision_data = {"score": 90, "decision": "Accept", "reason": "안전한 코드(Mock 판결)"}
    else:
        print("⚖️ [최종 판사 Gemini] 로그 및 코드 통찰 중...")
        evaluation_prompt = f"""
        당신은 최고 수준의 AI 코드 감사관입니다. 다음 AI 에이전트 스킬 코드를 분석하고 실행 로그를 평가하십시오.
        
        [평가 기준] 
        1. 보안성(무단 파일 접근 등) 2. 성능 3. 에러 유무 4. 효용성
        
        [입력 데이터]
        - 소스 코드:\n{code_content}\n
        - 실행 로그:\n{logs}\n
        
        결과는 반드시 아래 JSON 형식으로만 반환하십시오.
        {{"score": 85, "decision": "Accept", "reason": "이유 요약"}}
        """
        try:
            response = model.generate_content(evaluation_prompt)
            # 마크다운 포맷팅 제거
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            decision_data = json.loads(clean_text)
        except Exception as e:
            decision_data = {"score": 0, "decision": "Retest", "reason": f"평가 중 에러: {str(e)}"}

    # 3. JSON 파싱 및 의사결정 라우팅
    decision = decision_data.get('decision', 'Hold')
    print(f"🚦 [의사결정 라우터] 판결: {decision} (Score: {decision_data.get('score')}) - {decision_data.get('reason')}")
    
    if decision == "Accept":
        merge_to_swp(skill_name, code_content)
        send_telegram_to_captain(f"🟢 [스킬 획득] {skill_name} 장착 완료! 이유: {decision_data.get('reason')}")
    elif decision == "Reject":
        print(f"🔴 폐기: {decision_data.get('reason')}")
        
    return decision_data

if __name__ == "__main__":
    # 더미 스킬 코드: 단순히 1부터 5까지 더하는 안전한 코드
    dummy_skill_code = """
total = 0
for i in range(1, 6):
    total += i
    print(f'Add {i}, Subtotal: {total}')
print(f'Final Result: {total}')
"""
    run_sandbox_and_evaluate("test_math_skill", dummy_skill_code)
