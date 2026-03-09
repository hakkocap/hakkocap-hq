from ghost_memory_core import SovereignMemory
import time

print("Initializing Stage 2 Core Engine...")
mem = SovereignMemory()

print("Testing Stage 2 Profile & Memory Insertion...")
mem.update_profile("Name", "제이 윤 (하꼬방의 캡틴)")
mem.update_profile("Trait", "데이터 주권 수호자, 탈중앙화 혁명가")
mem.store("캡틴은 시스템 종속을 거부하고 로컬 독립 환경(Sovereign Memory)을 성공적으로 구축했다.", "프로젝트")
mem.store("우리는 한국어 전용 벡터 모델인 ko-sroberta-multitask를 탑재했다.", "기술")

print("Testing Stage 2 Recall (의미 기반 검색)...")
res = mem.recall("캡틴의 철학과 목표는 무엇인가?")
for r in res:
    print(f"[{r[0]:.4f}] {r[1]} ({r[2]})")

print("Stage 2 Initialization Complete.")
