# 스킬 설치 우선순위 계획
# Skill Installation Priority Plan
# 작성: 2026-03-04 13:30
# 기간: 2026-03-05 ~ 2026-03-10 (6일)

---

## 🥇 1순위: learn-claude-code (최우선)

### 설치 일정
**날짜**: 2026-03-05  
**소요 시간**: 2시간  
**담당**: 데피디 + 나노봇 협업

### 설치 단계
1. **저장소 복제** (5분)
   ```bash
   cd /home/hakkocap/다운로드/
   git clone https://github.com/shareAI-lab/learn-claude-code.git
   cd learn-claude-code
   ```

2. **의존성 설치** (10분)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **12개 세션 학습** (90분)
   - Session 01: 단순 루프
   - Session 02: 도구 사용
   - Session 03: 핸들러 디스패치
   - Session 04: 작업 계획
   - Session 05-12: 고급 패턴

4. **안하무인 적용** (15분)
   - 에이전트 루프 패턴 → SWP 통합
   - 컨텍스트 압축 → 메모리 최적화
   - 도구 핸들러 → 나노봇 스킬 확장

### 예상 성과
- ✅ Claude Code 아키텍처 완전 이해
- ✅ 데피디/나노봇 개선 방향 도출
- ✅ 3계층 컨텍스트 압축 적용

---

## 🥈 2순위: activepieces (자동화)

### 설치 일정
**날짜**: 2026-03-06  
**소요 시간**: 1시간  
**담당**: 나노봇 (Docker 배포)

### 설치 단계
1. **Docker 실행** (5분)
   ```bash
   docker pull activepieces/activepieces:latest
   docker run -d -p 8000:80 \
     -e AP_ENCRYPTION_KEY=$(openssl rand -hex 32) \
     --name activepieces \
     activepieces/activepieces
   ```

2. **초기 설정** (10분)
   - http://localhost:8000 접속
   - 관리자 계정 생성
   - Workspace 생성

3. **MCP 서버 탐색** (30분)
   - 280개 서버 목록 확인
   - 안하무인 필요 서버 선별:
     - GitHub (코드 관리)
     - Telegram (메시지)
     - Gmail (이메일)
     - Google Calendar (일정)
     - Weather (날씨)
     - RSS (뉴스)

4. **첫 워크플로우 구축** (15분)
   - 트리거: GitHub issue 생성
   - 액션: Telegram 알림 → 나노봇 할당

### 예상 성과
- ✅ 자동화 워크플로우 5개 구축
- ✅ SWP와 MCP 연동
- ✅ 월 $20 Zapier 비용 절감

---

## 🥉 3순위: chatgpt-on-wechat (장기 기억)

### 설치 일정
**날짜**: 2026-03-07~08  
**소요 시간**: 4시간  
**담당**: 데피디 (아키텍처 분석)

### 설치 단계
1. **저장소 복제** (5분)
   ```bash
   cd /home/hakkocap/다운로드/
   git clone https://github.com/zhayujie/chatgpt-on-wechat.git
   cd chatgpt-on-wechat
   ```

2. **코드 분석** (2시간)
   - 장기 기억 구현 메커니즘
   - 스킬 자동 생성 로직
   - 다중 모달 처리 방법
   - 작업 계획 알고리즘

3. **컨셉 추출** (1시간)
   - 안하무인 MEMORY.md 개선안
   - 나노봇 스킬 자동 생성 시스템
   - SWP 메모리 계층 구조

4. **프로토타입** (1시간)
   - `/home/hakkocap/다운로드/swp/memory/` 구조 설계
   - Tier 1/2/3 메모리 분리
   - 자동 consolidation 스크립트

### 예상 성과
- ✅ 장기 기억 시스템 설계
- ✅ 스킬 자동 생성 메커니즘
- ✅ SWP 메모리 개선

---

## 보류: CopilotKit & cherry-studio

### CopilotKit (7/10)
**보류 이유**:
- UI 개선은 현재 우선순위 낮음
- SWP Dashboard 안정화 먼저

**재검토 시기**: 2026-03-15 (Dashboard 리뉴얼 시)

### cherry-studio (8/10)
**보류 이유**:
- 다중 LLM 관리는 DeepSeek 단일 사용 중이라 불필요
- 300+ 어시스턴트는 오버스펙

**재검토 시기**: 2026-04-01 (다중 모델 전략 수립 시)

---

## 타임라인

```
2026-03-05 (Day 1)
├─ 09:00-11:00 | learn-claude-code 설치 & 학습
└─ 완료: 에이전트 아키텍처 이해

2026-03-06 (Day 2)
├─ 10:00-11:00 | activepieces Docker 배포
└─ 완료: 자동화 워크플로우 5개

2026-03-07 (Day 3)
├─ 09:00-13:00 | chatgpt-on-wechat 분석 (Part 1)
└─ 완료: 장기 기억 메커니즘 이해

2026-03-08 (Day 4)
├─ 09:00-11:00 | chatgpt-on-wechat 분석 (Part 2)
└─ 완료: SWP 메모리 개선안

2026-03-09 (Day 5)
├─ 전일   | 통합 테스트
└─ 완료: 3개 스킬 시스템 연동

2026-03-10 (Day 6)
├─ 전일   | 문서화 & 최종 보고
└─ 완료: 스킬 컬렉션 프로젝트
```

---

## 성공 지표

- [ ] learn-claude-code 12개 세션 완료
- [ ] activepieces 워크플로우 5개 구축
- [ ] chatgpt-on-wechat 장기 기억 설계 완료
- [ ] SWP 메모리 시스템 개선 적용
- [ ] 나노봇 스킬 3개 이상 추가
- [ ] 월 자동화 비용 $20 절감

---

## 리스크 & 대응

### 리스크 1: 시간 부족
- **확률**: 중간
- **대응**: CopilotKit/cherry-studio 보류로 시간 확보

### 리스크 2: 호환성 이슈
- **확률**: 낮음
- **대응**: Docker 사용으로 격리

### 리스크 3: 학습 곡선
- **확률**: 중간
- **대응**: 나노봇 협업, 단계별 진행

---

**작성 완료**: 2026-03-04 13:30 [RAW]  
**예산**: $0 (오픈소스)  
**예상 ROI**: 높음 (자동화 절감 + 아키텍처 개선)
