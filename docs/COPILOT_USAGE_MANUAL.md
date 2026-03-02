# COPILOT_USAGE_MANUAL
## GitHub Copilot CLI Integration

### Installation
```bash
gh extension install github/gh-copilot
gh auth login  # GitHub 계정 연결
```

### Commands

#### 1. Explain
```bash
gh copilot explain "def fib(n): return fib(n-1) + fib(n-2)"
```
코드 동작 원리 설명

#### 2. Suggest
```bash
echo "merge two sorted lists" | gh copilot suggest -t shell
```
쉘 명령 제안

#### 3. SWP Integration
```python
from hooks.copilot_interface import copilot_explain, copilot_audit

# Self-Audit with Copilot
result = copilot_audit(generated_code)
```

### Use Cases
- **Stuck?**: copilot_suggest()로 라이브러리 문법 확인
- **Review**: copilot_audit()으로 자체 코드 검토
- **Learning**: copilot_explain()으로 낯선 코드 분석

### Security
- `--exclude`: 민감한 키/토큰 제외
- Local only: 코드가 GitHub로 전송되지 않음 (explain 제외)

---
**Agent**: Defid  
**Added**: 2026-03-02
