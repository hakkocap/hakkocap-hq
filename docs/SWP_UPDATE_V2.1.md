# SWP Module: Persistent Context & Strategic Matrix (PCSM)

## 1. 개요 (Overview)
본 모듈은 캡틴의 장기 계획을 잊지 않고, 중단된 시점부터 즉시 재개할 수 있도록 하는 '맥락 보존(Context Preservation)'과 '달성 매트릭스(Matrix)'를 SWP 핵심 프로토콜에 이식합니다.

## 2. 핵심 기능 (Core Functions)

### A. 전략적 달성 매트릭스 (Strategic Matrix)
- **시간별 달성 지표:** 작업별 예상 시간과 실제 달성도를 매트릭스 형태로 추적합니다.
- **상태 전파:** `swp.db`의 `task_status` 테이블과 연동하여 실시간 진행률을 대시보드에 표시합니다.

### B. 맥락 노트 시스템 (Context Note / Breadcrumbs)
- **Checkpointing:** 매 작업 종료 시 또는 오류 발생 시, 현재의 '생각의 흐름'과 '다음 단계'를 `last_context.json`에 강제 기록합니다.
- **Auto-Resume:** 새로운 세션 시작 시 `last_context.json`을 최우선으로 로드하여 중단된 지점부터 사고를 재개합니다.

### C. 셀프 명령 및 체크리스트 (Self-Command)
- **잡다한 체크리스트:** 기술적 부채, 사소한 버그, 캡틴의 지나가는 지시사항을 `MISC_CHECKLIST.md`에 아카이빙하고 주기적으로 리마인드합니다.

## 3. 업데이트된 SWP 구조 (Updated Structure)

```
/home/hakkocap/다운로드/swp/
├── plans/                      # [NEW] 장기 계획 및 전략 매트릭스 저장
│   ├── MASTER_PLAN.md          # 캡틴의 대지침
│   └── MATRIX_2026-03.md      # 월간 달성 매트릭스
├── context/                    # [NEW] 맥락 보존 데이터
│   ├── last_context.json       # 마지막 작업 스냅샷
│   └── breadcrumbs.log         # 사고의 흐름 기록
└── reports/
    └── CHECKLIST/              # [NEW] 잡다한 체크리스트 및 셀프 명령
        └── MISC_CHECKLIST.md
```

## 4. 실행 프로토콜 (Execution Protocol)

1. **Pre-Task:** `context/last_context.json`을 읽어 중단점 확인.
2. **In-Task:** 15분 간격으로 `breadcrumbs.log`에 현재 상태 기록.
3. **Post-Task:** 달성 매트릭스 업데이트 및 `MISC_CHECKLIST.md` 갱신.

---
**Signatory:** 부관 데피디 🏴‍☠️
**Date:** 2026-03-06
**Version:** SWP-2.1 (Context Enhanced)
