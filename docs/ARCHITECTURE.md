# SWP Architecture (Post-Integration)
## Sovereign Workflow Protocol
**Date:** 2026-03-02  
**Version:** 2.0 (governance-system 통합)

---

## System Overview

SWP는 세 가지 핵심 계층으로 구성됩니다:
- **Tier 1 (Current):** 실시간 상태 및 실행 중인 작업
- **Tier 2 (Checklist):** 증명된 완료 상태
- **Tier 3 (Audit):** 검증된 이력 및 교정 기록

---

## Directory Structure

```
/home/hakkocap/.openclaw/workspace/
├── SKILL.md                    # SWP Core Manifesto
├── TOOLS.md                    # Local Environment Notes
├── AGENTS.md                   # Workspace Guidelines
├── MEMORY.md                   # Long-term Memory (Private)
├── ARCHITECTURE.md             # This Document
├── SOUL.md / USER.md           # Identity & User Context
├── 
└── memory/                     # Daily Session Logs
    └── YYYY-MM-DD.md

/home/hakkocap/다운로드/swp/
├── backend/
│   ├── main.py                 # FastAPI Server (Port 8080)
│   ├── data/
│   │   └── swp.db             # SQLite Database
│   └── hooks/
│       ├── __init__.py
│       ├── deputy_skill_manual.py   # Primary Agent Training
│       └── governance_bridge.py     # [NEW] Migrated from GS
├── frontend/
│   └── dashboard.html
└── requirements.txt
(Note: No separate governance-system hooks required)

/home/hakkocap/governance-system/
├── DEPRECATED.txt              # Migration Notice
├── .deprecated/                # [7-Day Quarantine]
│   ├── governance_daemon.py  # DEPRECATED - Use SWP Events
│   ├── governance_loop.py    # DEPRECATED - OpenClaw Runtime
│   └── auto_auditor.py       # DEPRECATED - SWP Audit
└── hook_manual.py            # [MIGRATED] → governance_bridge.py
```

---

## Hook Migration Mapping

| Legacy (governance-system) | SWP Replacement | Status |
|---------------------------|-----------------|--------|
| `governance_daemon.py` | SWP Scheduled Hooks + Dashboard | Deprecated |
| `governance_loop.py` | OpenClaw Core Runtime | Replaced |
| `auto_auditor.py` | `governance_bridge.py` (Triple-Check) | Migrated |
| `hook_manual.py` (original) | `deputy_skill_manual.py` | Migrated + Enhanced |

### governance_bridge.py (New)
**Location:** `/home/hakkocap/다운로드/swp/backend/hooks/governance_bridge.py`

**Purpose:** 구 hook_manual의 Anti-Hallucination 로직을 SWP 검증 시스템에 통합.

**Key Functions:**
- `verify_command_fulfillment()` - 명령 완수 검증
- `check_for_hallucinations()` - Hallucination 검출
- `extract_validation_metrics()` - 수치화된 검증
- `load_stats() / save_stats()` - 통신 기록

**Path Updates:**
- `LOG_FILE`: `governance-system/essence_log.txt` → `.openclaw/workspace/logs/swp_essence.log`
- `STATS_FILE`: `governance-system/.hallucination_stats.json` → `.openclaw/workspace/data/hallucination_stats.json`

---

## Verification Protocol

### Pre-Task Hook
1. Load relevant Skill Manual from hooks/
2. Parse intent and extract keywords
3. Create validation checklist

### Post-Task Hook (Anti-Hallucination)
1. **Fact Check:** System log presence
2. **Path Check:** Physical existence (ls, curl)
3. **Cost Check:** Minimize API calls

### Report Format
```
- [Current State]: 진행률과 Context
- [Checklist]: 완료/남은 항목
- [Audit Log]: 오류와 RCA
- [Next Step]: 승인 필요 단계
```

---

## Rollback Resources

**7-Day Quarantine:** `/home/hakkocap/governance-system/.deprecated/`

**Rollback Trigger:**
```bash
cd /home/hakkocap/governance-system/ && cp .deprecated/*.py . && ./governance_daemon.py
```

**Quarantine Expires:** 2026-03-09 (auto-delete scheduled)

---

## Captain's Room Structure

```
/home/hakkocap/캡틴스룸/
├── 인간의_정수/
│   ├── Captain_Philosophy.txt
│   ├── human_behavior_learning.md
│   ├── sync_strategy_3step.md
│   └── history/
└── 기술의_정수/
    ├── ghost_scraper.py
    ├── ai_trend_collector.py
    └── governance_bridge.py
```

---

## Future Integration Points

1. **Memory System:** `.openclaw/workspace/memory/` with SWP hooks
2. **Session Management:** OpenClaw subagents integration
3. **Dashboard:** `/docs` endpoint for API browser

---

## Signatory

**Agent:** Defid (데피디) - 하꼬 해적단 부관  
**Authority:** Surgeon (써전) - 캡틴 대리인  
**Integration Date:** 2026-03-02 20:48 KST  
**Protocol Version:** SWP-2.0
