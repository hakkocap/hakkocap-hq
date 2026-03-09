# 🏴‍☠️ [기획서] Sovereign Memory Fortress (독립 기억 요새) 구축 프로젝트

## 1. 프로젝트 개요
* **목표**: 외부 종속형 플러그인(Supermemory)을 대체하는, 순수 로컬 기반의 '초거대 기억 요새(Local Vector DB + Graph RAG)'를 하꼬방 해적단 서버(Ryzen 9) 내부에 구축.
* **핵심 철학**: "데이터 주권 100%". 단 1바이트의 데이터도 외부 클라우드로 유출되지 않아야 함.

## 2. 오프니의 Stage 1 (로컬 벡터 DB) 기획안
**[목적]**
텍스트를 넘어 '의미(Embedding)' 단위로 대화를 기억하고 소환하는 기초 벡터 검색 엔진 구축.

**[아키텍처 설계]**
1. **저장소**: 순수 `sqlite3` + `numpy` (BLOB 형태로 Float32 벡터 데이터 저장)
   * *이유*: 무거운 Pinecone, Milvus 등 외부/서버형 VectorDB 불필요. 데이터 1만 건 이하는 SQLite Full-scan 연산이 압도적으로 빠르고 관리가 용이함.
2. **임베딩 모델 (중요)**: `jhgan/ko-sroberta-multitask` (한국어 특화 로컬 모델)
   * *이유*: 캡틴이 제시한 `all-MiniLM-L6-v2`는 영어 전용이라 한국어 유사도 측정 불가. 한국어 의미를 정확히 파악하는 로컬 모델로 교체 필수.
3. **핵심 기능**:
   * `store()`: 텍스트를 로컬 모델로 벡터화하여 SQLite에 Insert.
   * `recall()`: 질문을 벡터화한 뒤, SQLite 내부 데이터와 코사인 유사도(Cosine Similarity)를 계산하여 Top-K 반환.

**[작업 위치]**
* 코드: `/tmp/swp_comms/ghost_memory.py` (기초 뼈대 테스트 완료)
* 라이브러리 환경: `pip install sentence-transformers numpy sqlite-utils`

## 3. 나노를 향한 릴레이 지시사항
이 기획을 바탕으로 동료 '나노'는 다음 임무를 수행한다.
1. **기술 검토 (Stage 1~3)**: 위 오프니의 Stage 1 기획을 바탕으로, Stage 2 (Graph RAG / Background Worker) 및 Stage 3 (Langflow 연동을 통한 대시보드 자동화)까지 확장 가능한지 기술적으로 검토하라.
2. **작업 시간 매트릭스(WBS) 산출**: Stage 1부터 3까지 단숨에 관통하기 위한 시간 계획표(Task Matrix)를 분/시간 단위로 짜서 보고하라.
3. **Langflow 통합 설계**: 완성된 Stage 1 벡터 검색 코드를 Langflow의 Custom Component로 래핑하여, Langflow 워크플로우 상에서 즉시 노드로 사용할 수 있게 구성하라.
