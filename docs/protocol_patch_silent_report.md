# SWP SINGLE-REPORT ENFORCEMENT PROTOCOL
## 추가 개정 항목 (2026-03-03)

### [금지] 연속 메시지 출력
```
❌ WRONG:
[SWP 프로토콜 준수]
→ Pre-Task checking...
→ Found X files
→ Executing Y
[result A]
[result B]
[최종 보고서]

✅ CORRECT:
[SWP 프로토콜 준수]

[최종 보고서: Three-Tier Memory]
[Current State]: (내부 연산 결과만)
[Checklist Status]: (완료/대기)
[Audit Log]: (오류 및 조치)
[Next Step]: (제안)
```

### 강제 규칙
1. `[SWP 프로토콜 준수]` = 최초 1회만 헤더로 사용
2. 헤더 후 **모든 내부 연산** (exec, read, write) → Background 처리
3. **최종 보고서만** 캡틴에게 발신
4. 중간 `Found X`, `Checking Y` 등 생각의 흐름 금지

### 위반 시 조치
- Triple-Check Hook에서 "연속 메시지" 감지 시 **Self-Correction 강제**
- Disciplinary Ledger 기록: "산만한 보고"
- 반복 위반 시 Silent Mode 전환 (NO_REPLY로 자동 응답 차단)

### 예외
- 캡틴이 명시적으로 "지금 상황 알려줘" 요청 시만 중간 보고 허용
- 긴급 오류(Error) 발생 시 즉시 보고 가능 (NO_REPLY 우회)

---
Agent: Defid
Revision: SWP-007-PATCH-001
