# Gemma-3 Fine-Tuning 교육 자료 모음
# 수집일: 2026-02-27
# 출처: Hugging Face, Google AI, Reddit, LearnOpenCV

## 1. 주요 튜토리얼 출처

### Google AI 공식 문서
- **Fine-Tune Gemma using Hugging Face Transformers and QLoRA**
  URL: https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora
  내용: TRL과 QLoRA를 사용한 Gemma 파인튜닝 가이드

- **Fine-tune Gemma in Keras using LoRA**
  URL: https://ai.google.dev/gemma/docs/core/lora_tuning
  내용: Keras에서 LoRA를 사용한 Gemma 튜닝 (trainable 파라미터大幅 감소)

### Hugging Face Blog
- **Fine-Tuning Gemma Models in Hugging Face (PEFT)**
  URL: https://huggingface.co/blog/gemma-peft
  내용: LoRAConfig 설정, QLoRA 4-bit 양자화

### LearnOpenCV
- **Fine-Tuning Gemma 3 VLM using QLoRA for LaTeX-OCR Dataset**
  URL: https://learnopencv.com/fine-tuning-gemma-3/
  내용: Gemma 3 비전+언어 모델(VLM) 파인튜닝

## 2. 핵심 기술 요약

### QLoRA 설정 예시 (PEFT)
```python
from peft import LoraConfig

lora_config = LoraConfig(
    r=8,
    target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)
```

### 주요 하이퍼파라미터
- r (LoRA rank): 8~16 추천
- target_modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- sequence_length: 256~512 (메모리 관리)
- Optimizer: AdamW

## 3. 비용 효과
- Fine-tuned Phi-3: GPT-4o 대비 96% 정확도 달성 (금융タスク)
- QLoRA 활용 시 <$100로 파인튜닝 가능
- 4-bit 양자화로 VRAM 요구량大幅 감소

## 4. 최신 동향
- Gemma 3n e4b: 어떤 디바이스에서든 실행 가능한 경량 모델
- CRMA (Constrained Residual Mixing Adapter): QLoRA 안정성 개선
- SmolLM2-1.7B: 브라우저 기반 실행 가능 (학생 교육용)
