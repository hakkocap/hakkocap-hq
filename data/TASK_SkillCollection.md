# TASK: AI 에이전트 스킬 컬렉션 수집
# AI Agent Skill Collection Task
# 시작: 2026-03-04 13:10
# 소요: 30분

---

## 목표

1. **Brave Search로 AI 스킬 저장소 검색**
   - GitHub repositories
   - Skill marketplaces
   - AI agent frameworks

2. **나노봇에게 수집 지시**
   - URL 목록 전달
   - 각 사이트 분석 명령
   - 유용한 스킬 목록화

3. **스킬 카탈로그 구축**
   - 분류 체계 수립
   - 우선순위 평가
   - 설치 가능 여부 판단

---

## 시간 매트릭스

| 시간 | 활동 | 담당 | 체크포인트 |
|------|------|------|----------|
| 13:10-13:15 | 검색 키워드 수립 & Brave 검색 | 데피디 | CP-1 (13:15) |
| 13:15-13:20 | 검색 결과 분석 & URL 선별 | 데피디 | CP-2 (13:20) |
| 13:20-13:25 | 나노봇에게 수집 지시 | 데피디 | CP-3 (13:25) |
| 13:25-13:35 | 나노봇 수집 작업 감시 | 데피디 | CP-4 (13:35) |
| 13:35-13:40 | 스킬 카탈로그 작성 | 데피디 | CP-5 (13:40) |

---

## 검색 전략

### 검색 키워드 (5개)
1. "AI agent skills repository"
2. "LLM agent tools collection"
3. "OpenAI function calling skills"
4. "AI assistant capabilities marketplace"
5. "agent workflow templates github"

### 검색 대상
- **GitHub**: 오픈소스 스킬 저장소
- **Hugging Face**: AI 모델/스킬 공유
- **LangChain**: Agent 프레임워크 스킬
- **AutoGPT**: 자율 에이전트 플러그인
- **OpenClaw Skills**: 자체 스킬 허브

---

## 수집 항목

### 필수 정보
- [ ] 스킬 이름
- [ ] 설명 (한 줄)
- [ ] GitHub/저장소 URL
- [ ] 사용 언어 (Python/Node.js/etc)
- [ ] 의존성 (requirements)
- [ ] 설치 난이도 (Easy/Medium/Hard)
- [ ] 유용성 점수 (0-10)

### 분류 체계
1. **시스템 관리**: 파일/프로세스/네트워크
2. **데이터 처리**: 분석/변환/시각화
3. **외부 API**: 검색/번역/날씨/뉴스
4. **개발 도구**: 코드 생성/테스트/디버깅
5. **자동화**: 스크립트/워크플로우
6. **통신**: 이메일/슬랙/텔레그램
7. **학습**: 문서 분석/요약/QA

---

## 나노봇 지시 프로토콜

### 명령 템플릿
```
🏴 [데피디 → 나노봇 #0] 스킬 수집 임무

URL: [검색 결과 URL]

지시:
1. 해당 페이지 접근
2. README.md 또는 메인 페이지 분석
3. 다음 정보 추출:
   - 스킬 이름
   - 설명
   - 설치 방법
   - 예제 코드
4. /tmp/skill_collection/skill_[번호].json 저장

보고 형식:
{
  "name": "...",
  "description": "...",
  "url": "...",
  "language": "...",
  "difficulty": "...",
  "usefulness": 0-10
}

즉시 실행하라.
━━━━━━━━━━━━
데피디 부관
```

---

## 성공 지표

- [ ] 최소 20개 스킬 저장소 발견
- [ ] 나노봇 수집 완료 (5개 이상)
- [ ] 스킬 카탈로그 작성 (Markdown)
- [ ] 우선 설치 대상 3개 선정
- [ ] 30분 내 완료

---

## 출력물

1. **`SKILL_CATALOG.md`**: 전체 스킬 목록
2. **`skill_collection/*.json`**: 개별 스킬 정보
3. **`INSTALL_PRIORITY.md`**: 우선 설치 계획

---

**작성**: 2026-03-04 13:10 [RAW]  
**시작**: 즉시  
**종료 예정**: 2026-03-04 13:40
