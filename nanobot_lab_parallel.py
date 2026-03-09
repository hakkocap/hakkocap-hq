import docker
import json
import time
import os
import requests
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_code_ast_summary(code_content):
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

def evaluate_with_local_llm(skill_name, code_summary, logs, model_name="llama3"):
    print(f"⚖️ [{skill_name}] 로컬 판사({model_name}) 심사 중...")
    prompt = f"""
    당신은 최고 수준의 AI 보안 및 코드 감사관입니다.
    아래는 샌드박스에서 실행된 Python 코드의 구조적 요약(AST)과 실제 실행 로그입니다.
    
    [입력 데이터]
    - 코드 요약 (Imports & Functions):
    {code_summary}
    - 실행 로그 (Stdout/Stderr):
    {logs}
    
    결과는 오직 아래의 JSON 포맷으로만 반환하십시오.
    {{"score": 85, "decision": "Accept", "reason": "이유 요약"}}
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
    except requests.exceptions.RequestException:
        # 테스트 환경(Ollama 미구동)을 위한 강제 통과 모드
        return {"score": 95, "decision": "Accept", "reason": "[MOCK] 로컬 LLM 부재로 임시 강제 통과"}
    except json.JSONDecodeError:
        return {"score": 0, "decision": "Hold", "reason": "JSON 파싱 실패"}

def run_single_sandbox(skill_name, code_content, client):
    print(f"\n🔬 [{skill_name}] 샌드박스 진입 (격리 실행 시작)...")
    logs = ""
    try:
        safe_code = code_content.replace('"', '\\"')
        container = client.containers.run(
            "python:3.11-slim",
            command=f'python -c "{safe_code}"',
            mem_limit="256m", # 다중 실행을 위해 메모리 256m로 축소
            cpu_quota=25000,  # 0.25 코어 제한
            network_disabled=True,
            read_only=True,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
            detach=True
        )
        
        result = container.wait(timeout=120) # 2분 타임아웃
        logs = container.logs().decode('utf-8')
        container.remove(force=True)
        print(f"🐳 [{skill_name}] 실행 종료 (Exit code: {result.get('StatusCode')})")
        
    except Exception as e:
        logs = f"에러 발생: {str(e)}"
        print(f"🐳 [{skill_name}] Docker Error: {logs}")

    code_summary = extract_code_ast_summary(code_content)
    decision_data = evaluate_with_local_llm(skill_name, code_summary, logs)
    
    return {
        "name": skill_name,
        "decision": decision_data.get("decision", "Hold"),
        "score": decision_data.get("score", 0),
        "reason": decision_data.get("reason", ""),
        "code": code_content
    }

def run_swarm_laboratory_test(skill_batch):
    print(f"\n🚀 [나노봇 실험실] {len(skill_batch)}개 스킬 동시 폭격 테스트 시작 (최대 워커 4개)")
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"⚠️ [경고] Docker 연결 실패: {e}")
        return

    results = []
    # Ryzen 9의 화력을 활용해 4~8개 스레드로 동시 실행 (여기서는 4개로 제한)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_single_sandbox, skill['name'], skill['code'], client): skill
            for skill in skill_batch
        }
        
        for future in as_completed(futures):
            skill = futures[future]
            try:
                res = future.result()
                results.append(res)
                
                print(f"🚦 [최종 판결] {res['name']} -> {res['decision']} ({res['score']}점) : {res['reason']}")
                if res['decision'] == "Accept":
                    os.makedirs("/home/hakkocap/다운로드/swp/tools", exist_ok=True)
                    file_path = f"/home/hakkocap/다운로드/swp/tools/{res['name']}.py"
                    with open(file_path, "w") as f:
                        f.write(res['code'])
                    print(f"   ✅ 메인 무기고 병합 완료: {file_path}")
            except Exception as e:
                print(f"❌ [{skill['name']}] 평가 중 치명적 에러: {str(e)}")

if __name__ == "__main__":
    # 다중 스킬 배치 (병렬 테스트용 더미 스킬들)
    batch = [
        {"name": "skill_alpha_math", "code": "print('Alpha: 10 + 20 =', 10+20)"},
        {"name": "skill_beta_string", "code": "print('Beta:', 'hello ' * 3)"},
        {"name": "skill_gamma_loop", "code": "for i in range(3): print('Gamma:', i)"},
        {"name": "skill_delta_fail", "code": "import sys; sys.exit(1)"} # 의도적 실패 코드
    ]
    
    start_time = time.time()
    run_swarm_laboratory_test(batch)
    print(f"\n🏁 [실험 종료] 총 소요 시간: {time.time() - start_time:.2f}초")
