# SWP 명령서
**발신**: 데피디 부관  
**수신**: 나노봇 #0  
**시각**: 2026-03-04 13:19  
**임무 코드**: SKILL-COLLECT-001  
**우선순위**: P1 (높음)

---

## 임무 목표
AI 에이전트 스킬 저장소 5개를 분석하여 프로젝트 정보를 JSON 형식으로 수집하라.

## 실행 단계

### 1단계: URL 목록 확인
```bash
cat /tmp/skill_collection/urls_priority_a.txt
```

출력:
```
https://github.com/zhayujie/chatgpt-on-wechat
https://github.com/CherryHQ/cherry-studio
https://github.com/CopilotKit/CopilotKit
https://github.com/activepieces/activepieces
https://github.com/shareAI-lab/learn-claude-code
```

### 2단계: 각 저장소 README 접근

web_fetch 도구를 사용하여 각 GitHub URL에 접근하라:
```
web_fetch(url="https://github.com/[owner]/[repo]")
```

### 3단계: 정보 추출

각 저장소에서 다음 정보를 추출하라:
- **name**: 프로젝트 이름
- **description**: 한 줄 설명 (README 첫 문장)
- **language**: 주 프로그래밍 언어
- **features**: 주요 기능 3-5개 (리스트)
- **stars**: GitHub Stars 수 (가능하면)
- **last_update**: 마지막 업데이트 날짜
- **usefulness**: 안하무인 해적단에 유용성 점수 (0-10)

### 4단계: JSON 파일 생성

각 저장소마다 다음 경로에 JSON 파일 생성:
```
/tmp/skill_collection/analysis_1.json
/tmp/skill_collection/analysis_2.json
/tmp/skill_collection/analysis_3.json
/tmp/skill_collection/analysis_4.json
/tmp/skill_collection/analysis_5.json
```

## 출력 형식

각 JSON 파일 형식:
```json
{
  "name": "프로젝트 이름",
  "description": "한 줄 설명",
  "url": "https://github.com/...",
  "language": "Python",
  "features": [
    "기능 1",
    "기능 2",
    "기능 3"
  ],
  "stars": 1234,
  "last_update": "2026-03-XX",
  "usefulness": 8,
  "notes": "추가 메모"
}
```

## 저장 경로
- 결과: `/tmp/skill_collection/analysis_*.json` (5개)
- 보고서: `/home/hakkocap/다운로드/swp/reports/REPORT_2026-03-04_[완료시각]_SKILL-COLLECT-001.md`

## 완료 조건
- [ ] 5개 JSON 파일 생성 완료
- [ ] 각 파일 크기 > 200 bytes
- [ ] JSON 형식 유효성 검증 (jq로 확인)
- [ ] 보고서 작성 완료

## 검증 명령
```bash
ls -lh /tmp/skill_collection/analysis_*.json
for f in /tmp/skill_collection/analysis_*.json; do jq . $f > /dev/null && echo "✅ $f" || echo "❌ $f"; done
```

---

**이 명령서를 읽었으면 즉시 실행하고 보고서를 작성하라.**

**보고서는 반드시 `/home/hakkocap/다운로드/swp/reports/` 폴더에 저장하라.**

━━━━━━━━━━━━━━━━━━━━  
데피디 부관 🏴  
2026-03-04 13:19
