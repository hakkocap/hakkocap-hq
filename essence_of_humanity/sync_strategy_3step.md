# 나노봇 기반 essence_of_humanity → hakkocap-hq 동기화 3단계 전략

> 분석 엔진: deepseek/deepseek-r1:free (심층 추론 모드)

---

## 1단계: 스캔 & 분류 (Scan & Classify)

**목표:** essence_of_humanity 폴더 내 모든 자료를 자동으로 읽고 분류한다.

- 나노봇이 `/home/hakkocap/essence_of_humanity/` 를 주기적으로 스캔
- 파일별 메타데이터 추출: 파일명, 크기, 수정일, 키워드
- 주제별 태깅 자동화:
  - `philosophy` → Captain_Philosophy.txt 등
  - `tech_analysis` → 기술 분석 보고서
  - `fact_check` → 팩트체크 결과물
- 분류 결과를 `essence_of_humanity/INDEX.md` 에 자동 갱신
- **리소스 제한:** CPU 10% 이내, 1회 스캔 시 최대 50개 파일

---

## 2단계: 요약 & 변환 (Summarize & Transform)

**목표:** RAG 재료로 쓸 수 있도록 마크다운 형식으로 정교하게 가공한다.

- 각 파일의 핵심 내용을 3~5줄로 자동 요약
- 요약본을 `essence_of_humanity/summaries/` 하위에 저장
  - 예: `summaries/Captain_Philosophy_summary.md`
- Gemma(로컬) 또는 DeepSeek(무료)로 요약 생성
  - 단순 요약 → `google/gemini-2.0-flash-001` (저비용)
  - 심층 분석 → `deepseek/deepseek-r1:free` (고품질)
- 메타데이터 JSON 생성: `summaries/metadata.json`
  ```json
  {
    "file": "Captain_Philosophy.txt",
    "tags": ["philosophy", "captain", "principles"],
    "summary": "캡틴의 4대 핵심 철학 요약...",
    "last_synced": "2026-02-24T02:30:00+09:00"
  }
  ```

---

## 3단계: 안전한 푸시 (Secure Sync)

**목표:** hakkocap-hq 깃허브로 변경분만 정확히 전송한다.

- **차분 동기화(Diff Sync):**
  - `git diff --stat` 으로 변경된 파일만 감지
  - 불필요한 대량 푸시 방지
- **자동 커밋 정책:**
  - 커밋 메시지 형식: `[SYNC] YYYY-MM-DD: {변경 파일 수}개 동기화`
  - 하루 최대 3회 푸시 (오전/오후/심야)
- **보안 원칙:**
  - API 키, 토큰 등 민감 정보는 절대 커밋하지 않음
  - `.gitignore` 에 `*.key`, `*.token`, `config.json` 등록
  - SSH 키 인증만 사용 (HTTPS 토큰 URL 금지)
- **실행 명령 흐름:**
  ```bash
  cd /home/hakkocap/hakkocap-hq
  cp -r /home/hakkocap/essence_of_humanity/* ./essence_of_humanity/
  git add essence_of_humanity/
  git commit -m "[SYNC] $(date +%Y-%m-%d): essence 동기화"
  git push origin main
  ```

---

## 채산성 요약

| 항목 | 비용 |
|------|------|
| DeepSeek 요약 엔진 | 무료 (500만 토큰) |
| Gemini Flash 분류 | 무료/초저가 |
| 로컬 Gemma 스캔 | 전기세만 (월 ~11,000원) |
| GitHub 저장소 | 무료 (비공개) |
| **총 월 운영비** | **~11,000원** |

---

**결론:** 이 3단계 파이프라인으로 돈 한 푼 안 들이고 지식을 체계적으로 축적·동기화할 수 있다.
