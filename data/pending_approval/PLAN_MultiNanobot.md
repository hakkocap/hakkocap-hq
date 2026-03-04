# 다중 나노봇 아키텍처 계획서
# Multi-Nanobot Architecture for Cost Optimization
# 작성: 2026-03-04 11:49
# 목표: 로컬 AI (Ollama) + 저렴한 외부 API (DeepSeek) 조합으로 비용 획기적 절감

---

## I. 현황 분석 [VERIFIED]

### 1. 현재 자원 상태

**하드웨어** [RAW]:
- CPU: Ryzen 9 (고성능)
- RAM: 28GB total, 20GB available
- Disk: 824GB 여유
- GPU: (확인 필요)

**Ollama 모델** [VERIFIED|ollama list]:
```
qwen2.5-coder:14b       9.0 GB    코딩 특화
kimi-k2.5:cloud         -         OpenClaw 무료 티어용
gemma3-pirate:latest    8.1 GB    해적 모드 (실험용)
gemma3:12b              8.1 GB    범용
```

**현재 운영 중인 Nanobot** [VERIFIED]:
- **Nanobot #0 (전령)**: Port 18790, DeepSeek API, Telegram @hakkoclaw_bot
- 역할: 캡틴 직속 전령, 독립 개체 유지

### 2. 비용 구조 분석

**외부 API 비용** (DeepSeek 기준):
- 입력: $0.14 / 1M tokens
- 출력: $0.28 / 1M tokens
- 현재 잔고: API 키당 제한 가능성

**로컬 AI 비용**:
- 전기료만 (1시간 약 100~200원 추정)
- 무제한 토큰
- 응답 속도: 외부 API보다 느림 (하지만 무료)

---

## II. 다중 나노봇 아키텍처 설계

### 핵심 전략: **하이브리드 라우팅**

```
┌─────────────────────────────────────────────┐
│          캡틴 (Telegram)                      │
└──────────────┬──────────────────────────────┘
               │
        ┌──────▼──────┐
        │  Nanobot #0  │ (전령, DeepSeek, Port 18790)
        │  독립 개체   │ 캡틴 직속, 항상 대기
        └──────────────┘
               │
        ┌──────▼──────────────────────────────┐
        │     데피디 (라우팅 허브)              │
        │  작업 유형 분석 → 최적 봇 배정        │
        └──┬──────┬──────┬──────────────────┘
           │      │      │
    ┌──────▼───┐ ┌▼─────┐ ┌▼──────────┐
    │Nanobot #1│ │#2    │ │#3         │
    │로컬 중심 │ │혼합형│ │API 중심   │
    └──────────┘ └──────┘ └───────────┘
```

### 3개 가상환경 나노봇 구성

#### **Nanobot #1: 로컬 중심형** (Port 18791)
- **가상환경**: `/home/hakkocap/nanobot-env-local/`
- **주 모델**: Ollama (qwen2.5-coder, gemma3)
- **보조**: DeepSeek (복잡한 추론만)
- **용도**:
  - 코드 생성 (qwen2.5-coder)
  - 간단한 질문 응답 (gemma3)
  - 파일 읽기/쓰기 (로컬 처리)
  - 반복 작업 (무제한 토큰)
- **비용 절감**: 80%
- **단점**: 느린 응답

#### **Nanobot #2: 혼합형** (Port 18792)
- **가상환경**: `/home/hakkocap/nanobot-env-hybrid/`
- **주 모델**: Ollama (초안) → DeepSeek (정제)
- **전략**: 
  1. Ollama로 초안 생성
  2. DeepSeek로 검증/정제
  3. 최종 응답 출력
- **용도**:
  - 문서 작성 (초안 로컬, 교정 API)
  - 계획 수립 (로컬 브레인스토밍, API 정리)
  - 분석 작업 (로컬 데이터 처리, API 요약)
- **비용 절감**: 60%
- **장점**: 속도와 품질 균형

#### **Nanobot #3: API 중심형** (Port 18793)
- **가상환경**: `/home/hakkocap/nanobot-env-api/`
- **주 모델**: DeepSeek (100%)
- **보조**: Ollama (긴급 백업)
- **용도**:
  - 복잡한 추론
  - 실시간 대화 (빠른 응답 필요)
  - 중요한 결정 (높은 정확도)
- **비용 절감**: 0% (하지만 필요한 작업만)
- **장점**: 최고 품질

---

## III. 작업 라우팅 매트릭스

| 작업 유형 | 최적 봇 | 이유 | 예상 비용 |
|----------|---------|------|----------|
| 코드 생성 (Python) | #1 (로컬) | qwen2.5-coder 특화 | $0 |
| 간단한 질문 | #1 (로컬) | gemma3 충분 | $0 |
| 파일 분석 | #1 (로컬) | 로컬 처리 빠름 | $0 |
| 문서 작성 | #2 (혼합) | 초안 무료, 교정만 유료 | $0.05 |
| 계획 수립 | #2 (혼합) | 브레인스토밍 무료, 정리 유료 | $0.10 |
| 복잡한 추론 | #3 (API) | DeepSeek 고품질 | $0.20 |
| 실시간 대화 | #3 (API) | 빠른 응답 | $0.15 |
| 긴급 작업 | #0 (전령) | 캡틴 직속, 최고 우선순위 | $0.20 |

---

## IV. 시간별 구축 계획

### Phase 1: 환경 구축 (예정: 2026-03-05)

**소요 시간**: 4시간

**TASK NB-001: 가상환경 3개 생성**
```bash
# Nanobot #1 (로컬 중심)
python3 -m venv /home/hakkocap/nanobot-env-local
source /home/hakkocap/nanobot-env-local/bin/activate
pip install nanobot-ai

# Nanobot #2 (혼합형)
python3 -m venv /home/hakkocap/nanobot-env-hybrid
source /home/hakkocap/nanobot-env-hybrid/bin/activate
pip install nanobot-ai

# Nanobot #3 (API 중심)
python3 -m venv /home/hakkocap/nanobot-env-api
source /home/hakkocap/nanobot-env-api/bin/activate
pip install nanobot-ai
```

**TASK NB-002: Config 파일 생성**
- `/home/hakkocap/.nanobot-local/config.json` (Ollama 중심)
- `/home/hakkocap/.nanobot-hybrid/config.json` (혼합)
- `/home/hakkocap/.nanobot-api/config.json` (DeepSeek)

### Phase 2: 라우터 구축 (예정: 2026-03-06)

**소요 시간**: 6시간

**TASK NB-003: 데피디 라우터 작성**
```python
# /home/hakkocap/다운로드/swp/backend/services/nanobot_router.py

class NanobotRouter:
    """
    작업 유형 분석 후 최적 나노봇 선택
    """
    
    BOTS = {
        "local": "http://localhost:18791",
        "hybrid": "http://localhost:18792",
        "api": "http://localhost:18793",
        "herald": "http://localhost:18790"  # 전령
    }
    
    @staticmethod
    def route(task_description: str) -> str:
        """
        작업 설명 → 최적 봇 선택
        """
        keywords = {
            "code": "local",
            "python": "local",
            "파일": "local",
            "문서": "hybrid",
            "계획": "hybrid",
            "추론": "api",
            "긴급": "herald"
        }
        
        for kw, bot in keywords.items():
            if kw in task_description.lower():
                return BOTS[bot]
        
        return BOTS["hybrid"]  # 기본값
```

**TASK NB-004: Gateway 통합**
- 데피디가 작업 받으면 → 라우터 호출
- 최적 봇으로 전달 → 응답 수신
- 캡틴에게 결과 보고

### Phase 3: 모델 설정 (예정: 2026-03-07)

**TASK NB-005: Ollama 최적화**
```json
// .nanobot-local/config.json
{
  "agents": {
    "defaults": {
      "model": "ollama/qwen2.5-coder:14b",
      "provider": "ollama",
      "fallback": "deepseek/deepseek-chat"
    }
  }
}
```

**TASK NB-006: 혼합 전략 설정**
```json
// .nanobot-hybrid/config.json
{
  "agents": {
    "defaults": {
      "model": "ollama/gemma3:12b",
      "provider": "ollama",
      "refinement": "deepseek/deepseek-chat"
    }
  }
}
```

### Phase 4: 테스트 & 최적화 (예정: 2026-03-08)

**TASK NB-007: 성능 벤치마크**
- 응답 속도 측정
- 품질 평가 (캡틴 판정)
- 비용 추적

**TASK NB-008: 라우팅 알고리즘 튜닝**
- 키워드 추가
- 우선순위 조정
- 실전 데이터 기반 개선

---

## V. 비용 절감 시뮬레이션

### 현재 상태 (All DeepSeek)
| 작업 | 횟수/일 | 토큰/회 | 비용/일 |
|------|---------|---------|---------|
| 코드 생성 | 20 | 2,000 | $0.11 |
| 질문 응답 | 50 | 500 | $0.07 |
| 문서 작성 | 10 | 3,000 | $0.08 |
| 복잡한 추론 | 5 | 4,000 | $0.06 |
| **합계** | **85** | - | **$0.32/일** |

**월간**: $9.60

### 다중 나노봇 (하이브리드)
| 작업 | 최적 봇 | 비용/일 |
|------|---------|---------|
| 코드 생성 | #1 (로컬) | $0 |
| 질문 응답 | #1 (로컬) | $0 |
| 문서 작성 | #2 (혼합) | $0.02 |
| 복잡한 추론 | #3 (API) | $0.06 |
| **합계** | - | **$0.08/일** |

**월간**: $2.40

**절감액**: $7.20/월 (75% 절감)
**연간**: $86.40 절감

---

## VI. 위험 요소 및 대응

| 위험 | 확률 | 영향 | 대응 |
|------|------|------|------|
| Ollama 응답 느림 | 높음 | 중 | 혼합형으로 우회 |
| 로컬 모델 품질 낮음 | 중 | 높음 | API 백업, 정제 단계 추가 |
| RAM 부족 (여러 모델 동시) | 중 | 높음 | 순차 로드, swap 활용 |
| 라우팅 오판 | 낮 | 중 | 수동 오버라이드 기능 |

---

## VII. 성공 지표

- [ ] 월간 API 비용 75% 절감 ($9.60 → $2.40)
- [ ] 평균 응답 시간 5초 이내 유지
- [ ] 품질 점수 (캡틴 평가) 8/10 이상
- [ ] 3개 나노봇 안정적 운영 (uptime 95%+)
- [ ] 로컬 모델 활용률 60% 이상

---

## VIII. 체크리스트

### NB-001: 가상환경 생성 (2026-03-05)
- [ ] nanobot-env-local 생성
- [ ] nanobot-env-hybrid 생성
- [ ] nanobot-env-api 생성
- [ ] 각각 nanobot-ai 설치

### NB-002: Config 생성 (2026-03-05)
- [ ] .nanobot-local/config.json
- [ ] .nanobot-hybrid/config.json
- [ ] .nanobot-api/config.json
- [ ] DeepSeek API 키 설정

### NB-003: 라우터 구축 (2026-03-06)
- [ ] nanobot_router.py 작성
- [ ] 키워드 매칭 로직
- [ ] 테스트 케이스 작성

### NB-004: Gateway 통합 (2026-03-06)
- [ ] 데피디에 라우터 연결
- [ ] 3개 포트 확인 (18791/2/3)
- [ ] 통합 테스트

### NB-005~008: 모델 설정 & 최적화 (2026-03-07~08)
- [ ] Ollama 모델 설정
- [ ] 혼합 전략 구현
- [ ] 벤치마크 실행
- [ ] 튜닝 완료

---

## IX. 다음 단계

**즉시** (지금):
1. 캡틴 승인 대기
2. 승인 시 Phase 1 착수

**내일** (2026-03-05):
- NB-001: 가상환경 3개 생성
- NB-002: Config 파일 작성

**모레** (2026-03-06):
- NB-003: 라우터 구축
- NB-004: Gateway 통합

---

**작성 완료**: 2026-03-04 11:49 [RAW]
**작성자**: 데피디
**캡틴 승인 대기 중** 🏴‍☠️
