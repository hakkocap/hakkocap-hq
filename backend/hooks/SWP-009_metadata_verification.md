# SWP-009: Metadata Verification Protocol
## 메타데이터 캐시 오염 방지

**문제:** CHAT_ARCHIVE_PLAN.md의 추정값(추후 허위로 판명)이 순환 참조되어사실처럼 사용됨

**원인:**
1. HTML 파싱 → 날짜/수치 추출 (추정)
2. 문서화 → "확정된 사실"로 기록
3. 재사용 → 원본 재확인 없이 문서 신뢰
4. 할루시네이션 전파

**해결책:**

```markdown
### 메타데이터 표기법

[RAW]        원본에서 직접 추출
[EXTRACTED]  파싱 후 미검증  
[VERIFIED]   exec/read로 확인 완료 (날짜 첨부)
[CACHED]     문서화된 값 - 사용 시 주의

**사용 규칙:**
- CACHED 레벨을 소스로 사용 시 반드시 재검증
- 24시간 이상 된 CACHED 메타데이터는 불신
- 모든 보고서는 RAW 레벨 재확인 권장
```

**적용 예시:**
```python
# WRONG
dates = "2025-12-09 ~ 2026-03-02"  # CHAT_ARCHIVE_PLAN.md에서 복사

# CORRECT
dates = grep_extract()  # 원본 HTML에서 직접 추출
verified_dates = verify_dates(dates)  # [VERIFIED|2026-03-03]
```

Agent: Defid  
Error: 2025-12-09 할루시네이션  
Fix: SWP-009 Protocol 적용
