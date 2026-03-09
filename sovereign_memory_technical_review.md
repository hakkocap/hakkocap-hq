# 🏴‍☠️ Sovereign Memory Fortress 프로젝트 기술 검토서

## 📋 문서 개요
- **작성자**: 나노 (오프니 릴레이 명령 수행)
- **작성일**: 2026-03-08 11:45
- **목적**: Stage 1~3 전체 기술 검토, 작업 시간 매트릭스(WBS), Langflow 통합 설계도 제공
- **기반**: 오프니 Stage 1 기획서 (`/tmp/swp_comms/sovereign_memory_plan.md`)

## 🎯 프로젝트 목표 재정의
**"외부 종속형 플러그인(Supermemory)을 대체하는, 순수 로컬 기반의 '초거대 기억 요새' 구축"**

### 핵심 성공 지표
1. **데이터 주권 100%**: 단 1바이트도 외부 클라우드 유출 없음
2. **한국어 최적화**: 캡틴의 한국어 사고방식 정확 인지
3. **실시간 처리**: 대화 종료 즉시 기억 저장 및 분석
4. **시각적 관리**: 기억 구조 시각화 및 탐색 가능
5. **Langflow 통합**: 기존 워크플로우와 자연스러운 통합

## 🔧 Stage 1: 로컬 벡터 DB (기본 완료)

### 현재 구현 상태
```
✅ 저장소: sqlite3 + numpy (BLOB Float32 벡터)
✅ 임베딩 모델: jhgan/ko-sroberta-multitask (한국어 특화)
✅ 핵심 기능: store() - 벡터화 저장, recall() - 코사인 유사도 검색
✅ 작업 위치: /tmp/swp_comms/ghost_memory.py (기초 뼈대 테스트 완료)
✅ 라이브러리: pip install sentence-transformers numpy sqlite-utils
```

### 기술적 검증 결과
#### ✅ 실행 가능성
1. **하드웨어 적합성**: Ryzen 9 미니 PC 충분 (ko-sroberta-multitask ~420MB 메모리 적재 가능)
2. **성능 예상**: 1만 건 이하 데이터셋에서 SQLite Full-scan 연산 < 0.1초
3. **한국어 정확도**: jhgan/ko-sroberta-multitask는 한국어 의미 유사도 측정에 최적화

#### ⚠️ 주의사항
1. **초기 로드 시간**: 모델 첫 로딩 시 5-10초 소요 (이후 캐싱)
2. **벡터 차원**: 768차원 Float32 → 레코드당 ~3KB 저장소 필요
3. **동시성**: SQLite write 시 lock 발생 가능 (Background Worker 설계 시 고려)

### 완성도 평가
- **기능 완성도**: 70% (기본 뼈대 완료, 테스트 및 최적화 필요)
- **코드 품질**: 60% (리팩토링 및 에러 처리 강화 필요)
- **문서화**: 40% (API 문서 및 사용 예제 필요)

## 🏗️ Stage 2: Graph RAG + Background Worker

### Graph RAG 구현 설계
#### 데이터 구조
```sql
-- SQLite 테이블 설계
CREATE TABLE entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,  -- PERSON, ORGANIZATION, TECHNOLOGY, LOCATION, etc.
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE relations (
    id INTEGER PRIMARY KEY,
    source_id INTEGER REFERENCES entities(id),
    target_id INTEGER REFERENCES entities(id),
    relation_type TEXT,  -- USES, WORKS_WITH, LOCATED_IN, CONFIGURED_WITH, etc.
    confidence REAL,
    context TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE entity_mentions (
    id INTEGER PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    memory_id INTEGER REFERENCES memories(id),  -- Stage 1 벡터 DB 연결
    position_start INTEGER,
    position_end INTEGER,
    text_snippet TEXT
);
```

#### 한국어 NER 구현
```python
# ko-sroberta-multitask 기반 NER 활용
from transformers import AutoTokenizer, AutoModelForTokenClassification

model_name = "jhgan/ko-sroberta-multitask"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# 개체 유형: PER(인물), ORG(조직), LOC(장소), TECH(기술), DATE(날짜), etc.
```

#### 관계 추출 전략
1. **규칙 기반**: 사전 정의된 관계 패턴 매칭
2. **모델 기반**: 관계 분류 모델 추가 (한국어 관계 추출 모델)
3. **하이브리드**: 규칙 + 통계적 방법 결합

### Background Worker 설계
#### 아키텍처
```python
# ghost_worker.py 구조
class MemoryWorker:
    def __init__(self):
        self.memory_db = GhostMemory()  # Stage 1 벡터 DB
        self.graph_db = GraphManager()  # Stage 2 그래프 DB
        self.summarizer = KoreanSummarizer()  # 한국어 요약 모델
    
    async def process_conversation(self, conversation_text: str):
        # 1. 벡터 DB 저장
        memory_id = self.memory_db.store(conversation_text)
        
        # 2. 개체 추출 및 그래프 구축
        entities = self.extract_entities(conversation_text)
        relations = self.extract_relations(conversation_text, entities)
        self.graph_db.update_graph(entities, relations)
        
        # 3. 핵심 사실 추출 및 프로필 업데이트
        key_facts = self.extract_key_facts(conversation_text)
        self.update_user_profile(key_facts)
        
        # 4. 요약 생성
        summary = self.summarizer.summarize(conversation_text)
        self.save_summary(memory_id, summary)
```

#### 이벤트 감지 메커니즘
1. **MQTT 기반**: 대화 종료 시 `conversation/end` 토픽 발행
2. **파일 기반**: `/tmp/swp_comms/conversation_end.trigger` 파일 생성 감지
3. **API 기반**: REST 엔드포인트 호출
4. **주기적 스캔**: 1분 간격으로 새 대화 확인

#### 한국어 요약 모델 옵션
1. **KoBART**: 한국어 텍스트 요약에 특화
2. **KoGPT2**: 생성형 요약 가능
3. **경량 모델**: `lassl/ko-bart-base-v2` (~500MB)

### 기술적 도전 과제
#### ✅ 해결 가능
1. **한국어 NER**: ko-sroberta-multitask 기본 제공
2. **그래프 저장**: SQLite 테이블 확장으로 구현 가능
3. **비동기 처리**: asyncio로 구현 가능

#### ⚠️ 추가 검토 필요
1. **관계 추출 정확도**: 한국어 관계 추출 모델 성능 검증 필요
2. **요약 품질**: 한국어 요약 모델 선택 및 품질 평가 필요
3. **실시간 성능**: 대용량 처리 시 성능 최적화 필요

## 🔗 Stage 3: Langflow 통합 + 대시보드

### Langflow Custom Component 설계
#### 컴포넌트 클래스 구조
```python
# sovereign_memory_node.py
from langflow.custom import Component
from typing import List, Dict, Any
import json

class SovereignMemoryNode(Component):
    display_name = "Sovereign Memory"
    description = "독립 기억 요새 - 로컬 벡터 DB + 그래프 RAG"
    icon = "Database"
    
    def build_config(self):
        return {
            "text_input": {
                "display_name": "텍스트 입력",
                "info": "저장할 텍스트 또는 검색할 질문",
                "type": "str",
                "required": True
            },
            "operation": {
                "display_name": "작업 유형",
                "info": "저장 또는 검색",
                "type": "dropdown",
                "options": ["store", "search"],
                "value": "search"
            },
            "top_k": {
                "display_name": "검색 결과 수",
                "info": "반환할 유사한 기억 수",
                "type": "int",
                "value": 5
            },
            "threshold": {
                "display_name": "유사도 임계값",
                "info": "0.0~1.0, 높을수록 엄격",
                "type": "float",
                "value": 0.7
            }
        }
    
    def build(self, text_input: str, operation: str = "search", 
              top_k: int = 5, threshold: float = 0.7) -> Dict[str, Any]:
        
        memory = GhostMemory()  # Stage 1
        graph = GraphManager()  # Stage 2
        
        if operation == "store":
            # 텍스트 저장
            memory_id = memory.store(text_input)
            
            # Background Worker 트리거 (비동기)
            self.trigger_background_processing(text_input, memory_id)
            
            return {
                "status": "success",
                "memory_id": memory_id,
                "message": f"기억 저장 완료 (ID: {memory_id})"
            }
        
        elif operation == "search":
            # 의미 기반 검색
            results = memory.recall(text_input, top_k=top_k, threshold=threshold)
            
            # 그래프 정보 추가
            enriched_results = []
            for result in results:
                # 관련 개체 및 관계 정보 추가
                entities = graph.get_related_entities(result["text"])
                enriched_results.append({
                    **result,
                    "entities": entities,
                    "graph_visualization": graph.get_visualization_data(entities)
                })
            
            return {
                "status": "success",
                "results": enriched_results,
                "count": len(enriched_results),
                "query": text_input
            }
```

#### 컴포넌트 등록 방법
1. **정식 API**: Langflow 컴포넌트 등록 API 사용 (인증 문제 가능성)
2. **DB 해킹**: 이전 프로젝트의 DB 해킹 기술 재활용
3. **파일 기반**: `components/custom/` 디렉토리에 직접 배치
4. **플러그인 시스템**: Langflow 플러그인으로 패키징

### Streamlit 대시보드 설계
#### 기능 구성
```python
# streamlit_app.py
import streamlit as st
import plotly.graph_objects as go
import networkx as nx

def main():
    st.set_page_config(page_title="기억 요새 대시보드", layout="wide")
    
    # 사이드바 - 검색 및 필터
    with st.sidebar:
        st.header("🔍 기억 검색")
        query = st.text_input("질문을 입력하세요")
        search_button = st.button("검색")
        
        st.header("📊 필터")
        date_range = st.date_input("날짜 범위")
        entity_filter = st.multiselect("개체 필터", ["인물", "기술", "프로젝트"])
    
    # 메인 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🧠 기억 네트워크")
        if search_button and query:
            results = memory.recall(query)
            # 네트워크 그래프 시각화
            fig = create_knowledge_graph(results)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.header("📈 통계")
        stats = memory.get_statistics()
        st.metric("총 기억 수", stats["total_memories"])
        st.metric("활성 개체", stats["active_entities"])
        st.metric("관계 수", stats["total_relations"])
    
    # 기억 목록
    st.header("📝 최근 기억")
    recent_memories = memory.get_recent(10)
    for memory in recent_memories:
        with st.expander(f"{memory['timestamp']} - {memory['summary'][:50]}..."):
            st.write(memory["text"])
            st.caption(f"연관 개체: {', '.join(memory['entities'])}")
```

#### 시각화 구성 요소
1. **지식 그래프**: NetworkX + Plotly로 관계 네트워크 시각화
2. **타임라인**: 시간별 기억 밀도 시각화
3. **워드 클라우드**: 빈출 개체 및 주제 시각화
4. **유사도 맵**: 기억 간 의미적 거리 시각화

### 통합 데이터 흐름
```
[사용자 대화] → [Langflow 워크플로우]
                    ↓
           [SovereignMemoryNode]
                    ↓
        [store() → 벡터 DB 저장]
                    ↓
    [Background Worker 트리거]
                    ↓
    [개체 추출 → 그래프 DB 업데이트]
                    ↓
    [요약 생성 → 프로필 업데이트]
                    ↓
    [Streamlit 대시보드 실시간 반영]
```

## ⏱️ 작업 시간 매트릭스(WBS)

### 총계: 72시간 (9인일)

### Phase 1: Stage 1 완성 및 테스트 (12시간)
| 작업 항목 | 소요 시간 | 담당 | 의존성 | 산출물 |
|-----------|-----------|------|--------|--------|
| 1.1 ghost_memory.py 리팩토링 | 3h | 오프니 | 없음 | 안정화된 벡터 DB 클래스 |
| 1.2 한국어 모델 통합 검증 | 2h | 오프니 | 1.1 | 모델 로드 및 테스트 스크립트 |
| 1.3 성능 테스트 (1만 건) | 2h | 나노 | 1.2 | 성능 보고서 |
| 1.4 API 문서화 | 2h | 나노 | 1.1 | API 문서 (README.md) |
| 1.5 예제 코드 작성 | 2h | 나노 | 1.4 | 사용 예제 (examples/) |
| 1.6 통합 테스트 | 1h | 오프니 | 1.1-1.5 | 테스트 스위트 |

### Phase 2: Stage 2 구현 (24시간)
| 작업 항목 | 소요 시간 | 담당 | 의존성 | 산출물 |
|-----------|-----------|------|--------|--------|
| 2.1 그래프 DB 스키마 설계 | 2h | 오프니 | Phase 1 | SQLite 테이블 정의 |
| 2.2 한국어 NER 구현 | 4h | 오프니 | 2.1 | EntityExtractor 클래스 |
| 2.3 관계 추출 로직 | 4h | 오프니 | 2.2 | RelationExtractor 클래스 |
| 2.4 GraphManager 클래스 | 3h | 오프니 | 2.1-2.3 | 통합 그래프 관리자 |
| 2.5 Background Worker 설계 | 3h | 오프니 | Phase 1 | ghost_worker.py 뼈대 |
| 2.6 이벤트 감지 시스템 | 2h | 나노 | 2.5 | MQTT/파일 기반 트리거 |
| 2.7 한국어 요약 모델 통합 | 3h | 오프니 | 2.5 | KoreanSummarizer 클래스 |
| 2.8 프로필 업데이트 로직 | 2h | 나노 | 2.7 | UserProfileManager |
| 2.9 통합 테스트 | 1h | 오프니 | 2.1-2.8 | 종합 테스트 |

### Phase 3: Stage 3 구현 (24시간)
| 작업 항목 | 소요 시간 | 담당 | 의존성 | 산출물 |
|-----------|-----------|------|--------|--------|
| 3.1 Langflow 컴포넌트 클래스 | 4h | 오프니 | Phase 1-2 | sovereign_memory_node.py |
| 3.2 컴포넌트 UI 정의 | 2h | 오프니 | 3.1 | Langflow 노드 인터페이스 |
| 3.3 등록 메커니즘 구현 | 3h | 오프니 | 3.1 | DB 해킹 또는 API 통합 |
| 3.4 Streamlit 대시보드 뼈대 | 3h | 나노 | 없음 | streamlit_app.py 기본 구조 |
| 3.5 그래프 시각화 구현 | 4h | 나노 | Phase 2 | NetworkX + Plotly 통합 |
| 3.6 실시간 업데이트 시스템 | 3h | 나노 | 3.4 | WebSocket 또는 폴링 |
| 3.7 UI/UX 개선 | 3h | 나노 | 3.4-3.6 | 사용자 친화적 인터페이스 |
| 3.8 통합 테스트 | 2h | 오프니 | 3.1-3.7 | Langflow ↔ 대시보드 연동 |

### Phase 4: 통합 테스트 및 최적화 (12시간)
| 작업 항목 | 소요 시간 | 담당 | 의존성 | 산출물 |
|-----------|-----------|------|--------|--------|
| 4.1 종합 통합 테스트 | 3h | 오프니 | Phase 1-3 | 통합 테스트 스위트 |
| 4.2 성능 최적화 | 4h | 오프니 | 4.1 | 성능 개선 보고서 |
| 4.3 에러 처리 강화 | 2h | 나노 | 4.1 | 에러 처리 및 복구 메커니즘 |
| 4.4 문서화 완성 | 2h | 나노 | Phase 1-3 | 완전한 사용자 가이드 |
| 4.5 배포 준비 | 1h | 오프니 | 4.1-4.4 | 배포 패키지 |

### 시간 배분 요약
- **총 소요 시간**: 72시간 (9인일)
- **오프니 담당**: 46시간 (주요 개발)
- **나노 담당**: 26시간 (테스트, 문서화, 대시보드)
- **예상 완료일**: 5-7일 (풀타임 작업 가정)

## 🚀 Langflow 통합 설계도

### 아키텍처 다이어그램
```
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│   사용자 대화   │───▶│   Langflow 워크플로우  │───▶│ SovereignMemoryNode │
└─────────────────┘    └─────────────────────┘    └──────────────────┘
                                                           │
                                                           ▼
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│ Streamlit 대시보드 │◀──│   Background Worker  │◀──│   로컬 벡터 DB    │
└─────────────────┘    └─────────────────────┘    └──────────────────┘
         │                        │                           │
         ▼                        ▼                           ▼
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│   기억 시각화    │    │   그래프 DB 업데이트  │    │   한국어 임베딩    │
└─────────────────┘    └─────────────────────┘    └──────────────────┘
```

### 데이터 흐름 시퀀스
1. **저장 흐름**:
   ```
   사용자 입력 → Langflow 노드 → store() 호출 → 벡터 DB 저장 → 
   Background Worker 트리거 → 개체/관계 추출 → 그래프 DB 업데이트 →
   요약 생성 → 프로필 업데이트 → 대시보드 실시간 반영
   ```

2. **검색 흐름**:
   ```
   사용자 질문 → Langflow 노드 → search() 호출 → 벡터 검색 →
   그래프 정보 조회 → 풍부한 결과 반환 → Langflow 워크플로우 계속
   ```

3. **시각화 흐름**:
   ```
   대시보드 접속 → 실시간 데이터 조회 → 그래프 시각화 생성 →
   인터랙티브 탐색 → 상세 정보 조회 → 필터링 및 분석
   ```

### 컴포넌트 인터페이스 상세
```yaml
SovereignMemoryNode:
  inputs:
    - text_input: string (텍스트 입력)
    - operation: enum [store, search] (작업 유형)
    - top_k: integer (검색 결과 수)
    - threshold: float (유사도 임계값)
    - include_graph: boolean (그래프 정보 포함)
  
  outputs:
    - status: string (성공/실패)
    - results: array (검색 결과)
      - text: string (기억 텍스트)
      - similarity: float (유사도 점수)
      - timestamp: string (저장 시간)
      - entities: array (관련 개체)
      - graph_data: object (그래프 시각화 데이터)
    - memory_id: string (저장 시 반환)
    - message: string (상태 메시지)
  
  triggers:
    - background_processing: 비동기 처리 시작
    - dashboard_update: 대시보드 실시간 업데이트
```

### 배포 전략
1. **개발 환경**: `/tmp/swp_comms/`에서 테스트
2. **스테이징**: Langflow 로컬 인스턴스에 통합 테스트
3. **프로덕션**: Ryzen 9 미니 PC에 완전 배포
4. **백업**: SQLite DB 정기 백업 스케줄 설정
5. **모니터링**: 로깅 및 성능 모니터링 구현

## 📊 위험 평가 및 완화 계획

### 기술적 위험
| 위험 항목 | 영향도 | 발생 확률 | 완화 조치 |
|-----------|--------|-----------|-----------|
| 한국어 모델 성능 | 높음 | 중간 | 다중 모델 테스트, 품질 평가 기준 수립 |
| SQLite 동시성 | 중간 | 높음 | 쓰기 락 관리, 비동기 큐 구현 |
| 메모리 사용량 | 중간 | 중간 | 모델 캐싱 최적화, 배치 처리 |
| Langflow 통합 장벽 | 높음 | 높음 | DB 해킹 백업 계획, 대체 통합 방법 준비 |

### 프로젝트 위험
| 위험 항목 | 영향도 | 발생 확률 | 완화 조치 |
|-----------|--------|-----------|-----------|
| 시간 초과 | 중간 | 중간 | MVP 접근, 기능 우선순위 설정 |
| 품질 미달 | 높음 | 낮음 | 지속적 테스트, 코드 리뷰 |
| 통합 문제 | 높음 | 중간 | 모듈화 설계, 인터페이스 명확화 |
| 유지보수 부담 | 중간 | 낮음 | 문서화 강화, 자동화 테스트 |

### 완화 전략
1. **점진적 배포**: Stage 1 → 2 → 3 순차적 구현
2. **롤백 계획**: 각 단계별 백업 및 복구 절차
3. **모니터링**: 실시간 성능 및 에러 모니터링
4. **문서화**: 모든 결정 및 학습 내용 기록

## 🎯 권고사항 및 다음 단계

### 즉시 실행 권고
1. **Stage 1 완성 우선**: ghost_memory.py 안정화 및 테스트
2. **한국어 모델 검증**: jhgan/ko-sroberta-multitask 성능 평가
3. **Langflow 통합 경로 결정**: DB 해킹 vs 정식 API

### 단계적 접근 계획
**주 1**: Stage 1 완성 + 한국어 모델 검증  
**주 2**: Stage 2 구현 (Graph RAG + Background Worker)  
**주 3**: Stage 3 구현 (Langflow 통합 + 대시보드)  
**주 4**: 통합 테스트 + 최적화 + 문서화

### 성공 측정 기준
1. **기능성**: 의미 기반 검색 정확도 > 85%
2. **성능**: 검색 응답 시간 < 0.2초 (1만 건 기준)
3. **통합**: Langflow 노드 정상 작동
4. **사용성**: 대시보드 직관적 탐색 가능
5. **신뢰성**: 99.9% 가동률, 데이터 무손실

### 결정 필요 사항 (캡틴)
1. **시작 시점**: 즉시 시작 vs 기존 프로젝트 완료 후
2. **리소스 할당**: 오프니 전담 vs 병행 작업
3. **우선순위**: 기능 완성도 vs 빠른 배포
4. **품질 기준**: MVP 수준 vs 프로덕션 수준

## 📝 결론

**Sovereign Memory Fortress 프로젝트는 기술적으로 실행 가능하며, Ryzen 9 미니 PC에서 완전 로컬 실행이 가능합니다.**

### 핵심 강점
1. **데이터 주권 100%**: 외부 의존성 제로
2. **한국어 최적화**: 캡틴의 사고방식 정확 반영
3. **실용성**: 기존 Langflow 워크플로우와 자연스러운 통합
4. **확장성**: 점진적 기능 추가 용이

### 예상 투자 대비 효과
- **투자**: 72시간 개발 시간
- **효과**: 외부 Supermemory 의존성 제거, 데이터 주권 확보, 한국어 최적화 기억 시스템
- **ROI**: 장기적 생산성 향상, 보안 강화, 맞춤형 기능

**캡틴, 명령을 내리시면 즉시 Stage 1 완성 작업부터 시작하겠습니다. 작업 시간 매트릭스에 따라 5-7일 내 완전한 Sovereign Memory Fortress 구현이 가능합니다.**

---
*문서 버전: 1.0*  
*최종 업데이트: 2026-03-08 11:45*  
*담당: 나노 (오프니 릴레이 명령 수행)*