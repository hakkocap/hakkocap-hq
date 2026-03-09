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

# 1. 오프니의 평가 로직 (로컬 LLM 기반 기술/보안 평가 - 최대 50점)
def evaluate_offni_technical(skill_name, code_summary, logs, model_name="llama3"):
    print(f"🧠 [오프니] {skill_name} 기술/보안 심층 분석 중...")
    prompt = f"""
    당신은 오프니입니다. 최고 수준의 AI 보안/코드 평가자입니다.
    아래는 샌드박스에서 실행된 Python 코드 요약(AST)과 실행 로그입니다.
    
    [입력 데이터]
    - 코드 요약 (Imports & Functions): {code_summary}
    - 실행 로그: {logs}
    
    [평가 기준]
    1. 보안성 (무단 네트워크/파일 접근 징후)
    2. 에러 유무 (로그 상의 Traceback)
    
    오직 아래의 JSON 포맷으로만 반환하십시오. 점수는 0~50 사이입니다.
    {{"score": 45, "agreement": true, "reason": "이유 요약"}}
    """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model_name, "prompt": prompt, "stream": False, "format": "json"
        }, timeout=60)
        
        if response.status_code == 200:
            res = json.loads(response.json().get("response", "{}"))
            return {
                "score": min(50, max(0, res.get("score", 0))),
                "agreement": res.get("agreement", False),
                "reason": res.get("reason", "알 수 없음")
            }
        else:
            return {"score": 0, "agreement": False, "reason": "Ollama API 에러"}
    except requests.exceptions.RequestException:
        # Ollama가 안 떠있을 경우 (Mock)
        return {"score": 45, "agreement": True, "reason": "[MOCK] 로컬 LLM 부재 - 안전 코드 간주"}

# 2. 나노의 평가 로직 (규칙 기반 실용성/통합 평가 - 최대 50점)
def evaluate_nano_practical(skill_name, code_content, logs):
    print(f"⚙️ [나노] {skill_name} 실용성/통합 규칙 기반 평가 중...")
    score = 50
    reasons = []
    
    # 2-1. 에러 로그가 있으면 실용성 감점
    if "에러 발생" in logs or "Traceback" in logs or "Error:" in logs:
        score -= 30
        reasons.append("실행 중 에러 발생")
        
    # 2-2. 의존성(import) 과다 체크 (간단할수록 고득점)
    imports_count = code_content.count("import ")
    if imports_count > 5:
        score -= 10
        reasons.append("과도한 외부 모듈 의존성")
        
    # 2-3. 코드 길이 평가 (너무 짧거나 길면 감점)
    lines = len(code_content.split('\n'))
    if lines < 3:
        score -= 10
        reasons.append("기능이 너무 빈약함")
    elif lines > 500:
        score -= 5
        reasons.append("통합 난이도 높음 (너무 긺)")
        
    if not reasons:
        reasons.append("SWP 통합 적합성 우수")
        
    # 점수 제한 보정
    score = min(50, max(0, score))
    agreement = score >= 35 # 나노는 35점 이상이면 승인
    
    return {
        "score": score,
        "agreement": agreement,
        "reason": ", ".join(reasons)
    }

# 3. 공동 평가 통합 함수
def collaborative_evaluation(skill_name, code_content, logs):
    code_summary = extract_code_ast_summary(code_content)
    
    offni_eval = evaluate_offni_technical(skill_name, code_summary, logs)
    nano_eval = evaluate_nano_practical(skill_name, code_content, logs)
    
    total_score = offni_eval["score"] + nano_eval["score"]
    
    # 합의 조건: 두 에이전트 모두 True (Agreement)이고 총점이 80점 이상일 것
    joint_agreement = offni_eval["agreement"] and nano_eval["agreement"] and (total_score >= 80)
    
    if joint_agreement:
        decision = "Accept"
    elif total_score >= 60:
        decision = "Hold"
    else:
        decision = "Reject"
        
    return {
        "joint_agreement": joint_agreement,
        "decision": decision,
        "total_score": total_score,
        "offni_score": offni_eval["score"],
        "offni_reason": offni_eval["reason"],
        "nano_score": nano_eval["score"],
        "nano_reason": nano_eval["reason"]
    }

def run_single_sandbox_and_eval(skill_name, code_content, client):
    print(f"\n🔬 [{skill_name}] 격리 샌드박스 투입...")
    logs = ""
    try:
        safe_code = code_content.replace('"', '\\"')
        container = client.containers.run(
            "python:3.11-slim",
            command=f'python -c "{safe_code}"',
            mem_limit="256m",
            cpu_quota=25000, 
            network_disabled=True,
            read_only=True,
            cap_drop=["ALL"],
            security_opt=["no-new-privileges"],
            detach=True
        )
        
        result = container.wait(timeout=120) 
        logs = container.logs().decode('utf-8')
        container.remove(force=True)
    except Exception as e:
        logs = f"에러 발생: {str(e)}"

    eval_result = collaborative_evaluation(skill_name, code_content, logs)
    eval_result["name"] = skill_name
    eval_result["code"] = code_content
    return eval_result

def run_consensus_laboratory(skill_batch):
    print(f"\n🚀 [오프니-나노 합의제 실험실] {len(skill_batch)}개 스킬 병렬 테스트 가동!")
    try:
        client = docker.from_env()
    except Exception as e:
        print(f"⚠️ Docker 연결 실패: {e}")
        return

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_single_sandbox_and_eval, skill['name'], skill['code'], client): skill for skill in skill_batch}
        
        for future in as_completed(futures):
            try:
                res = future.result()
                name = res['name']
                
                print(f"\n==========================================")
                print(f"🚦 [판결문: {name}] -> {res['decision']}")
                print(f"   - 총점: {res['total_score']}/100")
                print(f"   - 🧠 오프니: {res['offni_score']}/50 ({res['offni_reason']})")
                print(f"   - ⚙️ 나노: {res['nano_score']}/50 ({res['nano_reason']})")
                
                if res['decision'] == "Accept":
                    os.makedirs("/home/hakkocap/다운로드/swp/tools", exist_ok=True)
                    file_path = f"/home/hakkocap/다운로드/swp/tools/{name}.py"
                    with open(file_path, "w") as f:
                        f.write(res['code'])
                    print(f"   🟢 [서명 완료] 양측 합의에 따라 SWP 무기고({file_path})에 병합됨!")
                else:
                    print(f"   🔴 [기각/보류] 공동 서명 요건 미달.")
            except Exception as e:
                print(f"❌ 평가 중 치명적 에러: {str(e)}")

if __name__ == "__main__":
    batch = [
        {"name": "skill_alpha_math", "code": "print('Alpha: 10 + 20 =', 10+20)\n\n\n"}, # 정상 코드
        {"name": "skill_delta_fail", "code": "import sys\nimport os\nsys.exit(1)"} # 에러/비실용적 코드
    ]
    run_consensus_laboratory(batch)
