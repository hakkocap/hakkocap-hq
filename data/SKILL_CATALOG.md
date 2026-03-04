# AI 에이전트 스킬 카탈로그
# AI Agent Skill Collection Catalog
# 작성: 2026-03-04 13:29
# 작성자: 데피디 부관
# 출처: 나노봇 #0 수집 데이터

---

## 요약

**수집 저장소**: 5개  
**총 Stars**: 60,735  
**주 언어**: Python (2), TypeScript (3)  
**평균 유용성**: 8.6/10

---

## 분류별 스킬 저장소

### 1. 시스템 통합 & 자동화

#### activepieces (9/10) ⭐ 16,093
- **설명**: AI Agents & MCPs & AI Workflow Automation
- **언어**: TypeScript
- **주요 기능**:
  - 280개 이상의 MCP 서버 도구킷
  - Zapier 오픈 소스 대체품
  - 노코드 워크플로우 빌더
  - AI 에이전트와 MCP 통합
- **URL**: https://github.com/activepieces/activepieces
- **안하무인 적용**: 해적단 자동화 워크플로우 구축, 외부 API 통합

---

### 2. AI 어시스턴트 프레임워크

#### chatgpt-on-wechat (9/10) ⭐ 26,161
- **설명**: CowAgent - 대규모 모델 기반 슈퍼 AI 어시스턴트
- **언어**: Python
- **주요 기능**:
  - 주도적 사고와 작업 계획
  - OS 및 외부 리소스 접근
  - 스킬 생성 및 실행
  - 장기 기억 및 지속적 성장
  - 다중 모달 메시지 처리
- **URL**: https://github.com/zhayujie/chatgpt-on-wechat
- **안하무인 적용**: 장기 기억 시스템, 스킬 자동 생성 메커니즘

#### cherry-studio (8/10) ⭐ 8,253
- **설명**: AI 생산성 스튜디오
- **언어**: TypeScript/JavaScript
- **주요 기능**:
  - 스마트 채팅
  - 자율 에이전트
  - 300개 이상의 사전 구성 AI 어시스턴트
  - 다양한 LLM 제공자 통합
- **URL**: https://github.com/CherryHQ/cherry-studio
- **안하무인 적용**: 다중 LLM 관리, 어시스턴트 템플릿

---

### 3. 프론트엔드 & UI

#### CopilotKit (7/10) ⭐ 6,688
- **설명**: 에이전트 및 생성형 UI를 위한 프론트엔드
- **언어**: TypeScript/JavaScript
- **주요 기능**:
  - React + Angular 지원
  - 채팅 UI 컴포넌트
  - 백엔드 도구 렌더링
  - 생성형 UI
  - 공유 상태 관리
- **URL**: https://github.com/CopilotKit/CopilotKit
- **안하무인 적용**: SWP Dashboard UI 개선, 대화형 인터페이스

---

### 4. 학습 & 참고

#### learn-claude-code (10/10) ⭐ 3,540 🏴 **최우선**
- **설명**: 나노 Claude Code 유사 에이전트 (0→1 구축)
- **언어**: Python
- **주요 기능**:
  - 12개의 점진적 학습 세션
  - 에이전트 루프 패턴 (User → LLM → Response)
  - 도구 사용 및 핸들러 디스패치
  - 작업 계획 및 하위 작업 분할
  - 컨텍스트 압축 전략 (3계층)
- **URL**: https://github.com/shareAI-lab/learn-claude-code
- **특이사항**: OpenClaw sister repo
- **안하무인 적용**: 에이전트 아키텍처 학습, 데피디/나노봇 개선

---

## 우선 설치 추천 (Top 3)

### 🥇 1위: learn-claude-code (10/10)
**이유**:
- OpenClaw와 직접 관련
- Claude Code 에이전트 구조 학습 가능
- 데피디/나노봇 아키텍처 개선에 활용
- 컨텍스트 압축 전략 적용 가능

**설치 방법**:
```bash
git clone https://github.com/shareAI-lab/learn-claude-code.git
cd learn-claude-code
pip install -r requirements.txt
```

**예상 소요**: 15분

---

### 🥈 2위: activepieces (9/10)
**이유**:
- 280+ MCP 서버 = 즉시 사용 가능한 스킬
- 자동화 워크플로우 구축
- Zapier 대체 (비용 절감)
- SWP와 통합 가능

**설치 방법**:
```bash
docker pull activepieces/activepieces
docker run -p 8000:80 activepieces/activepieces
```

**예상 소요**: 10분 (Docker)

---

### 🥉 3위: chatgpt-on-wechat (9/10)
**이유**:
- 장기 기억 시스템
- 스킬 자동 생성 메커니즘
- 다중 모달 처리
- 안하무인 철학과 부합 (지속적 성장)

**설치 방법**:
```bash
git clone https://github.com/zhayujie/chatgpt-on-wechat.git
cd chatgpt-on-wechat
pip install -r requirements.txt
# config.json 설정 후 실행
```

**예상 소요**: 30분 (설정 포함)

---

## 분석 요약

### 언어별 분포
- **Python**: 2개 (40%)
- **TypeScript**: 3개 (60%)

### 유용성 분포
- 10/10: 1개 (learn-claude-code)
- 9/10: 2개 (chatgpt-on-wechat, activepieces)
- 8/10: 1개 (cherry-studio)
- 7/10: 1개 (CopilotKit)

### Stars 분포
- 20k+: 1개 (chatgpt-on-wechat: 26k)
- 10k-20k: 1개 (activepieces: 16k)
- 5k-10k: 2개 (cherry-studio: 8k, CopilotKit: 6k)
- 3k-5k: 1개 (learn-claude-code: 3k)

### 안하무인 적용 가능성
1. **즉시 적용**: learn-claude-code (아키텍처 학습)
2. **단기 적용**: activepieces (자동화 워크플로우)
3. **중기 적용**: chatgpt-on-wechat (장기 기억)
4. **장기 적용**: CopilotKit (UI 개선), cherry-studio (다중 LLM)

---

## 다음 단계

1. **learn-claude-code 분석**: 12개 세션 학습 시작
2. **activepieces 테스트**: Docker로 로컬 실행
3. **장기 기억 설계**: chatgpt-on-wechat 구조 참고
4. **스킬 통합 계획**: SWP에 MCP 서버 연동

---

**작성 완료**: 2026-03-04 13:29 [RAW]  
**데이터 출처**: 나노봇 #0 수집 (SKILL-COLLECT-001)  
**검증**: ✅ 5개 JSON 파일 기반
