# 체크리스트: AI 스킬 컬렉션
# Checklist: Skill Collection Task
# 생성: 2026-03-04 13:11

---

## CP-1: Brave 검색 (13:10-13:15)

### 검색 실행
- [ ] 키워드 1: "AI agent skills repository"
- [ ] 키워드 2: "LLM agent tools collection"
- [ ] 키워드 3: "OpenAI function calling skills"
- [ ] 키워드 4: "AI assistant capabilities marketplace"
- [ ] 키워드 5: "agent workflow templates github"

### 결과 기록
- [ ] 검색 결과 10개 이상 수집
- [ ] GitHub 링크 추출
- [ ] CONTEXT 업데이트

---

## CP-2: URL 선별 (13:15-13:20)

### 분석 작업
- [ ] GitHub Star 수 확인
- [ ] 최근 업데이트 확인 (6개월 이내)
- [ ] README 품질 평가
- [ ] 라이선스 확인 (MIT/Apache 선호)

### 선별 기준
- [ ] 우선순위 A: 5개 선정
- [ ] 우선순위 B: 5개 선정
- [ ] 제외 대상 표시

### 완료 확인
- [ ] URL 목록 정리
- [ ] CONTEXT 업데이트
- [ ] 시간 확인 (13:20)

---

## CP-3: 나노봇 지시 (13:20-13:25)

### 명령 준비
- [ ] /tmp/skill_collection/ 폴더 생성
- [ ] 명령 템플릿 작성 (5개)
- [ ] Telegram API로 전달

### 지시 내용
- [ ] URL 1 → 나노봇 명령 1
- [ ] URL 2 → 나노봇 명령 2
- [ ] URL 3 → 나노봇 명령 3
- [ ] URL 4 → 나노봇 명령 4
- [ ] URL 5 → 나노봇 명령 5

### 완료 확인
- [ ] 5개 명령 전달 완료
- [ ] 나노봇 응답 확인
- [ ] CONTEXT 업데이트
- [ ] 시간 확인 (13:25)

---

## CP-4: 수집 감시 (13:25-13:35)

### 진행 감시
- [ ] 나노봇 로그 확인 (매 2분)
- [ ] skill_*.json 생성 확인
- [ ] 오류 발생 시 재지시

### 수집 확인
- [ ] skill_1.json 생성
- [ ] skill_2.json 생성
- [ ] skill_3.json 생성
- [ ] skill_4.json 생성
- [ ] skill_5.json 생성

### 완료 확인
- [ ] 5개 파일 검증
- [ ] JSON 형식 확인
- [ ] CONTEXT 업데이트
- [ ] 시간 확인 (13:35)

---

## CP-5: 카탈로그 작성 (13:35-13:40)

### 데이터 통합
- [ ] 5개 JSON 파일 읽기
- [ ] 정보 통합 (Markdown 테이블)
- [ ] 분류 체계 적용

### 문서 작성
- [ ] SKILL_CATALOG.md 생성
  - [ ] 헤더 & 소개
  - [ ] 분류별 스킬 목록
  - [ ] 각 스킬 설명
  - [ ] GitHub 링크
- [ ] INSTALL_PRIORITY.md 생성
  - [ ] 우선 설치 3개 선정
  - [ ] 설치 이유
  - [ ] 설치 방법
  - [ ] 예상 소요 시간

### 최종 보고
- [ ] 캡틴께 보고
- [ ] TASK 완료 표시
- [ ] 시간 확인 (13:40)

---

## 전체 진행률

```
완료: 0/5 체크포인트 (0%)
```

---

## 셀프 명령 스크립트

```bash
#!/bin/bash
# self_command_skill_collection.sh

echo "[13:10] CP-1 시작: Brave 검색"
# Brave search 5회 실행

echo "[13:15] CP-2 시작: URL 선별"
# 결과 분석 및 우선순위 매김

echo "[13:20] CP-3 시작: 나노봇 지시"
# Telegram API로 명령 전달

echo "[13:25] CP-4 시작: 수집 감시"
# 10분간 감시 루프

echo "[13:35] CP-5 시작: 카탈로그 작성"
# Markdown 문서 생성

echo "[13:40] TASK 완료"
```

---

**마지막 업데이트**: 2026-03-04 13:11 [RAW]
