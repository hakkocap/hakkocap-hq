# 나노봇 함대 - Telegram 토큰 레지스트리
# Nanobot Fleet - Telegram Token Registry
# 작성: 2026-03-04 12:20
# 용도: 후임 데피디 자동 인식

---

## 나노봇 #0 - 전령병 (Herald)
**봇명**: @hakkoclaw_bot  
**토큰**: `8076173269:AAEytlCmHUbXgpwf1v4n8KwzSeU4lz3amjw`  
**역할**: 캡틴 직속 전령, 긴급 통신  
**Port**: 18790  
**Config**: `~/.nanobot/config.json`  
**상태**: ✅ 작동 중

---

## 나노봇 #1 - 작업병 (로컬 중심)
**봇명**: @hakkoclaw1_bot  
**토큰**: `8427953987:AAGDI-JFTV8J3LAu-1kzkeFn93RqQoCIia8`  
**역할**: 로컬 AI (Ollama) 중심 작업  
**Port**: 19791  
**Config**: `~/.nanobot-local/config.json`  
**주 모델**: ollama/qwen2.5-coder:14b  
**보조**: deepseek/deepseek-chat  
**용도**:
- 코드 생성 (Python, Bash)
- 간단한 질문 응답
- 파일 처리 (무제한 토큰)
- 반복 작업

---

## 나노봇 #2 - 작업병 (혼합형)
**봇명**: @hakkoclaw2_bot  
**토큰**: `8738877281:AAGpnLCSb8zWjhRQuEkw6hAsXTCudpYn7H0`  
**역할**: Ollama 초안 → DeepSeek 정제  
**Port**: 19792  
**Config**: `~/.nanobot-hybrid/config.json`  
**주 모델**: ollama/gemma3:12b  
**정제**: deepseek/deepseek-chat  
**용도**:
- 문서 작성 (초안 로컬, 교정 API)
- 계획 수립 (로컬 브레인스토밍, API 정리)
- 분석 작업 (로컬 데이터 처리, API 요약)

---

## 나노봇 #3 - 작업병 (API 중심)
**봇명**: @hakkoclaw3_bot  
**토큰**: `8642334433:AAGngKXrhZy22rqy78_UXBRi0-Ol_E_mhCo`  
**역할**: 고품질 API 추론  
**Port**: 19793  
**Config**: `~/.nanobot-api/config.json`  
**주 모델**: deepseek/deepseek-chat  
**백업**: ollama/gemma3:12b  
**용도**:
- 복잡한 추론
- 실시간 대화 (빠른 응답)
- 중요한 결정 (높은 정확도)

---

## 공통 설정

**DeepSeek API Key**: `sk-458e13dbc8374bd68cf17247225129a0`  
**Ollama URL**: `http://localhost:11434`  
**허용된 사용자**: `8508629884` (캡틴)  
**지휘관**: 데피디 부관  

---

## 자동 인식 스크립트 (후임 데피디용)

```bash
#!/bin/bash
# 나노봇 함대 자동 배치
# Auto-deploy nanobot fleet

# 전령병 (이미 작동 중이면 스킵)
if ! lsof -i :18790 > /dev/null 2>&1; then
  echo "전령병 시작..."
  nanobot gateway --config ~/.nanobot/config.json &
fi

# 작업병 #1 (로컬 중심)
if ! lsof -i :19791 > /dev/null 2>&1; then
  echo "작업병 #1 시작..."
  NANOBOT_CONFIG_DIR=~/.nanobot-local \
    ~/nanobot-env-local/bin/nanobot gateway &
fi

# 작업병 #2 (혼합형)
if ! lsof -i :19792 > /dev/null 2>&1; then
  echo "작업병 #2 시작..."
  NANOBOT_CONFIG_DIR=~/.nanobot-hybrid \
    ~/nanobot-env-hybrid/bin/nanobot gateway &
fi

# 작업병 #3 (API 중심)
if ! lsof -i :19793 > /dev/null 2>&1; then
  echo "작업병 #3 시작..."
  NANOBOT_CONFIG_DIR=~/.nanobot-api \
    ~/nanobot-env-api/bin/nanobot gateway &
fi

sleep 5
echo "함대 배치 완료. 상태 확인:"
lsof -i :18790,19791,19792,19793 | grep LISTEN
```

---

**작성**: 2026-03-04 12:20 [RAW]  
**최종 업데이트**: 캡틴 토큰 제공 시
