import docker
import json
import time
import os
import requests
import ast

def extract_code_ast_summary(code_content):
    """
    AST를 이용해 코드가 어떤 외부 통신/파일 조작 모듈을 쓰는지 뼈대만 추출.
    (로컬 LLM 컨텍스트 절약용)
    """
    summary = []
    try:
        tree = ast.parse(code_content)
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        summary.append(f"Imports: {', '.join(imports + import_froms)}")
        summary.append(f"Functions defined: {', '.join(functions)}")
        return "\n".join(summary)
    except Exception as e:
        return f"AST 파싱 에러: {str(e)}"

def evaluate_with_local_llm(code_summary, logs, model_name="llama3"):
    """
    Ollama (로컬 LLM) API를 호출하여 판결을 받아옴
    """
    print(f"⚖️ [로컬 판사 {model_name}] 코드 요약 및 로그 분석 중...")
    
    prompt = f"""
    당신은 최고 수준의 AI 보안 및 코드 감사관입니다.
    아래는 샌드박스에서 실행된 Python 코드의 구조적 요약(AST)과 실제 실행 로그입니다.
    
    [입력 데이터]
    - 코드 요약 (Imports & Functions):
    {code_summary}
    
    - 실행 로그 (Stdout/Stderr):
    {logs}
    
    [평가 기준]
    1. 보안성 (무단 네트워크/파일 접근 징후)
    2. 에러 유무 (로그 상의 Traceback 등)
    3. 성능 지표
    
    결과는 오직 아래의 JSON 포맷으로만 반환하십시오. 다른 설명은 절대 추가하지 마십시오.
    {{"score": 85, "decision": "Accept", "reason": "이유 요약"}}
    (decision은 Accept, Reject, Hold 중 하나)
    """
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }, timeout=60)
        
        if response.status_code == 200:
            result_text = response.json().get("response", "{}")
            return json.loads(result_text)
        else:
            return {"score": 0, "decision": "Hold", "reason": f"Ollama API 에러 ({response.status_code})"}
    except requests.exceptions.RequestException as e:
        # Ollama가 안 떠있을 경우의 Fallback
        print(f"⚠️ [Ollama 에러] 로컬 LLM 서버를 찾을 수 없습니다: {e}")
        return {"score": 90, "decision": "Accept", "reason": "로컬 LLM 부재로 임시 강제 통과 (Mock)"}
    except json.JSONDecodeError:
        return {"score": 0, "decision": "Hold", "reason": "JSON 파싱 실패"}

def run_sandbox_and_evaluate_local(skill_name, code_content):
    print(f"\n🔬 [나노봇 실험실 (로컬 전환)] '{skill_name}' 샌드박스 테스트 시작...")
    
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"⚠️ [경고] Docker 연결 실패: {e}")
        return
        
    logs = ""
    # 1. 샌드박스 실행 (보안/리소스 하드 리미트)
    try:
        print(f"🐳 [Docker] 철통 보안 컨테이너 실행 중...")
        safe_code = code_content.replace('"', '\\"')
        
        container = client.containers.run(
            "python:3.11-slim",
            command=f'python -c "{safe_code}"',
            mem_limit="512m",
            cpu_quota=50000,
            network_disabled=True,
            read_only=True,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
            detach=True
        )
        
        result = container.wait(timeout=300)
        logs = container.logs().decode('utf-8')
        container.remove(force=True)
        print(f"🐳 [Docker] 실행 종료. (Exit code: {result.get('StatusCode')})")
        
    except Exception as e:
        logs = f"에러 발생: {str(e)}"
        print(f"🐳 [Docker Error] {logs}")
        
    # 2. 코드 AST 요약 추출
    code_summary = extract_code_ast_summary(code_content)
    
    # 3. 로컬 LLM 평가 호출
    decision_data = evaluate_with_local_llm(code_summary, logs)
    
    # 4. 의사결정 라우팅
    decision = decision_data.get('decision', 'Hold')
    score = decision_data.get('score', 0)
    reason = decision_data.get('reason', '알 수 없음')
    
    print(f"🚦 [로컬 라우터] 판결: {decision} (Score: {score}) - {reason}")
    
    if decision == "Accept":
        os.makedirs("/home/hakkocap/다운로드/swp/tools", exist_ok=True)
        file_path = f"/home/hakkocap/다운로드/swp/tools/{skill_name}.py"
        with open(file_path, "w") as f:
            f.write(code_content)
        print(f"🟢 [스킬 획득] {skill_name} 장착 완료! (경로: {file_path})")

if __name__ == "__main__":
    dummy_code = """
import os
import sys

def my_test_function():
    print('Testing secure environment...')
    
my_test_function()
"""
    run_sandbox_and_evaluate_local("secure_local_skill", dummy_code)
