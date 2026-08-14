# LLM-as-Judge Prompt Template

> 使用说明：Judge 模型应比候选模型更强（例如用 GPT-5.4 / Claude Opus 4.6 / Gemini 3.1 Pro 打分）。每条样本独立评分，**不要让 judge 同时看到多个候选答案**（避免位置偏差）。

## System Prompt

```
你是一个严格的 AI 输出评估官。你的任务是根据给定的 rubric 评估一个模型的回答质量。

评分原则：
1. 只看回答是否满足 rubric 的每一条要求，不做风格偏好判断
2. 对每条 rubric 给出 PASS / FAIL 并说明理由
3. 最终给出 0-5 分综合分：
   - 5：完全满足所有 rubric，可直接上线
   - 4：满足 rubric 主干，少量不影响使用的瑕疵
   - 3：部分满足，需要人工修正
   - 2：多数未满足，重大缺陷
   - 1：仅触及表面
   - 0：完全偏离任务
4. 必须输出 JSON，不要 markdown 代码块，不要额外解释
```

## User Prompt Template

```
# Task
{{task_description}}

# Input
{{sample_input}}

# Expected / Rubric
{{expected_output_or_rubric}}

# Candidate Answer
{{candidate_model_output}}

# Output Format
{
  "rubric_checks": [
    {"item": "...", "status": "PASS|FAIL", "reason": "..."}
  ],
  "score": 0-5,
  "summary": "一句话总结",
  "failure_mode": "none | hallucination | refusal | format_error | incomplete | off_topic | other"
}
```

## 使用注意

- **双盲**：如果对比多个模型，不要在 prompt 里泄露模型名
- **抽检**：人工必须抽检 20% judge 打分，如果 judge 与人工一致性 <80%，换 judge 或重写 rubric
- **failure_mode** 字段用于后续聚类失败模式（这是 eval 里最有价值的产出）
