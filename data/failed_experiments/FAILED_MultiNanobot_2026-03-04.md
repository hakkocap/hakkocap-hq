# FAILED EXPERIMENT: 다중 나노봇 함대 배치
# Failed Task: Multi-Nanobot Fleet Deployment
# 실패일: 2026-03-04 12:25
# 보관일: 2026-03-04 12:32

---

## 실험 목표

**캡틴의 구상**: 데피디(정찰병) → 실행병(나노봇들) 계층 구조  
**목적**: 로컬 AI 활용 + 저렴한 API 조합으로 비용 75% 절감

---

## 시도한 방법

### 1. 가상환경 3개 생성 ✅
```bash
~/nanobot-env-local
~/nanobot-env-hybrid
~/nanobot-env-api
```

### 2. Config 파일 3개 작성 ✅
```
~/.nanobot-local/config.json  (Port 19791)
~/.nanobot-hybrid/config.json (Port 19792)
~/.nanobot-api/config.json    (Port 19793)
```

### 3. Telegram 봇 토큰 3개 획득 ✅
- @hakkoclaw1_bot: `8427953987:AAGDI-JFTV8J3LAu-1kzkeFn93RqQoCIia8`
- @hakkoclaw2_bot: `8738877281:AAGpnLCSb8zWjhRQuEkw6hAsXTCudpYn7H0`
- @hakkoclaw3_bot: `8642334433:AAGngKXrhZy22rqy78_UXBRi0-Ol_E_mhCo`

### 4. Gateway 실행 시도 ❌

---

## 실패 원인

### 근본적 한계: Nanobot 아키텍처
1. **Config 우선순위**: `NANOBOT_CONFIG_DIR` 환경변수를 사용해도 `~/.nanobot/config.json`을 우선 읽음
2. **Telegram 충돌**: 하나의 봇 토큰 = 하나의 getUpdates만 허용
3. **채널 강제 활성화**: Config에서 channels 섹션을 제거해도 Nanobot이 자동으로 Telegram 시도

### 기술적 증거
```
telegram.error.Conflict: Conflict: terminated by other getUpdates request; 
make sure that only one bot instance is running
```

**증상**: 
- Nanobot #1~3 모두 전령병(@hakkoclaw_bot) 토큰으로 연결 시도
- 각자의 토큰(@hakkoclaw1/2/3_bot)을 무시함

---

## 학습한 교훈

1. **Nanobot은 단일 인스턴스 설계**: 여러 봇을 독립 실행하려면 구조 변경 필요
2. **환경변수 한계**: `NANOBOT_CONFIG_DIR`이 완전히 작동하지 않음
3. **Telegram API 제약**: 동시 polling 불가

---

## 대안 탐색 (향후 실험)

### Option A: NullClaw / PicoClaw
- 캡틴 언급: "초간단 나노봇 대안"
- 조사 필요: 이런 프로젝트가 존재하는지 확인
- 또는 직접 구현: 최소 기능 봇 (Telegram + LiteLLM)

### Option B: LiteLLM Proxy
- 장점: 여러 모델을 하나의 OpenAI 호환 API로 통합
- 구조: Depidi → LiteLLM Proxy → Ollama/DeepSeek
- 독립성: Telegram 없이 HTTP API만 사용

### Option C: 직접 구현
```python
# mini_bot.py
class MiniBot:
    """
    최소 기능 봇
    - Telegram 수신
    - LiteLLM 호출
    - 응답 전송
    """
```

### Option D: Webhooks 대신 Polling
- 문제: 현재 모든 봇이 Polling 모드
- 해결: Webhook 모드로 전환 (하지만 도메인/SSL 필요)

---

## 보관된 자원

### 파일 위치
- **토큰 레지스트리**: `/home/hakkocap/다운로드/swp/data/NANOBOT_REGISTRY.md`
- **계획서**: `/home/hakkocap/다운로드/swp/data/pending_approval/PLAN_MultiNanobot.md`
- **가상환경**: `~/nanobot-env-{local,hybrid,api}/`
- **Config**: `~/.nanobot-{local,hybrid,api}/config.json`

### 보존 이유
- Telegram 토큰 3개는 유효함
- 가상환경 재사용 가능
- Config 템플릿 재활용 가능

---

## 재실험 조건

**언제 다시 시도할 것인가**:
1. Nanobot 업데이트 시 (다중 인스턴스 지원)
2. 대안 프레임워크 발견 시 (NullClaw/PicoClaw)
3. 직접 구현 여력 생길 시 (Python 간단한 봇)

**필요한 자원**:
- ✅ Telegram 토큰 3개 (보관 중)
- ✅ DeepSeek API 키 (활성)
- ✅ Ollama 모델 4개 (설치됨)
- ✅ 가상환경 (준비됨)

---

## 중단 시점 상태

**작동 중**:
- ✅ Nanobot #0 (전령병, @hakkoclaw_bot, Port 18790)
- ✅ OpenClaw (데피디, Port 18789)
- ✅ SWP Dashboard (Port 8080)

**실패**:
- ❌ Nanobot #1~3 (Telegram 충돌)

**정리 완료**:
- 모든 중복 프로세스 종료
- Config 파일 보존
- 토큰 레지스트리 기록

---

## 다음 단계 (보류)

1. **단기** (필요 시):
   - LiteLLM Proxy 조사
   - 직접 구현 가능성 평가

2. **중기** (여유 시):
   - NullClaw/PicoClaw 존재 여부 확인
   - 최소 봇 프로토타입 제작

3. **장기** (언젠가):
   - Nanobot 구조 개선 기여 (오픈소스)
   - 다중 인스턴스 지원 PR 제출

---

**실패 기록**: 2026-03-04 12:25 [RAW]  
**보관 완료**: 2026-03-04 12:32 [RAW]  
**작성자**: 데피디 부관  
**교훈**: "실패는 성공의 어머니. 하지만 기록하지 않으면 그냥 실패." 🏴‍☠️
