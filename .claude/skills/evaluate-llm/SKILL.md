---
name: evaluate-llm
description: LLM 评估与选型工具包。双模式：查询模式（帮 PM 快速选型、对比模型、解答 2026 主流 LLM 能力问题）和执行模式（引导自建 eval set、用 LLM-as-judge 评分、核算 token 成本）。触发关键词：“帮我选模型”、“X 和 Y 对比”、“哪个 LLM 适合 X 场景”、“2026 最新模型”、“做一次模型评估”、“跑 eval”、“算一下模型成本”、“评估 LLM”。
---

# Evaluate LLM

本 skill 把《LLM 评估与选型框架》的知识和工作流封装成可直接调用的工具，帮 PM 在两种高频场景下做决策：

1. **查询模式（What / Which）** — 快速回答"用哪个模型"、"X vs Y 对比"、"2026 主流 LLM 现状"。
2. **执行模式（How）** — 引导自建 eval set、跑评分、算成本、出决策报告。

完整知识资产在 `docs/LLM_evaluation_framework.md`（同项目根目录下），本 skill 的行为必须与该文档保持一致。

---

## Mode Selection（用户意图 → 模式映射）

收到请求后，**先判断意图**：

| 用户说的话 | 模式 | 行为 |
|---|---|---|
| "帮我选个模型做 X" | 查询 | 走"查询 5 步" |
| "X 和 Y 哪个好" | 查询 | 对比关键 benchmark + 价格 + 场景适配 |
| "2026 最新 LLM 排名" | 查询 | 读 framework.md §3，给快照表 |
| "解释一下 GPQA / SWE-bench" | 查询 | 读 framework.md 附录 A |
| "给我做个 eval" | 执行 | 走"执行 5 步" |
| "帮我跑一下测试集" | 执行 | 用 `resources/eval_template.csv` + `judge_prompt.md` |
| "算一下模型成本" | 执行 | 用 `resources/cost_calculator.py` |

如果用户意图**不明确**，先用一句话反问：“你是想让我**帮你挑一个模型**，还是**帮你跑一次评估**？”

---

## 查询模式：5 步决策流

**必读**：`docs/LLM_evaluation_framework.md` 第 4 章和第 5 章。本模式下你是 PM 的**选型顾问**，不写代码，只给结论。

### Step 1：澄清任务画像（如果用户没说清）

必须追问到以下 4 点（缺什么问什么，不要全问）：
1. **任务形态**：chat / RAG / agent / batch / realtime？
2. **关键能力**：推理？代码？长文？多模态？工具调用？中文？
3. **硬约束**：预算上限？延迟要求？私有化？合规？
4. **现状**：已在用什么模型？为什么想换？

### Step 2：查决策矩阵（framework.md §5）

对照场景 → 模型矩阵给初步推荐。**必须**给首选 + 备选 + 决策依据。

### Step 3：查 benchmark 分数（framework.md §3、附录 A）

引用**具体数字**，不要说"表现不错"。例：
> Claude Opus 4.6 在 SWE-bench Verified 80.8%，是当前闭源第一；GLM-5 77.8% 是开源第一，价格约 1/5。

### Step 4：列出权衡

每个推荐都要写清**代价**：成本？延迟？合规？
例：Gemini 3.1 Pro 性价比高，但国内访问需代理。

### Step 5：给下一步建议

推荐执行模式下一步：
> 建议你用 50-100 条真实业务样本跑一次自建 eval，我可以帮你生成模板——要继续吗？

---

## 执行模式：5 步自建 eval 流程

**核心主张**：Public benchmark 有污染，**自建 eval 才是真相**。

### Step 1：定义 eval 目标

追问用户：
- 测几个模型？（建议 2-3 个）
- 测什么任务？（一次只测一种任务，不要混）
- 评分标准是什么？（二元对错 / 5 分 rubric / LLM-as-judge 自由打分）

### Step 2：生成 eval set 模板

使用 `resources/eval_template.csv`，列：
```
id, input, expected_output_or_rubric, tags, difficulty
```
引导用户填 50-200 条真实业务样本。告诉用户：
- **少而精 > 多而杂**——50 条高质量样本胜过 500 条随机样本
- 必须覆盖：典型任务 60% + 边界情况 30% + 已知失败 case 10%

### Step 3：跑评分（LLM-as-judge）

使用 `resources/judge_prompt.md` 作为评分官 prompt。建议：
- Judge 用比候选模型**更强**的模型（避免偏袒）
- 每条样本由 judge 输出：score + reason
- **人工抽检 20%** 校准 judge 质量

### Step 4：算真实成本

使用 `resources/cost_calculator.py`：
```
输入：平均 input tokens、平均 output tokens、日均调用数、模型选择
输出：月度成本、单次成本、TCO 对比表
```

### Step 5：出决策报告

结构化输出：
```
1. 任务画像
2. 候选模型与 benchmark 得分
3. 自建 eval 结果（通过率、失败模式分析）
4. 成本对比
5. 推荐决策（全量 / 灰度 / 多模型路由）
6. 风险点
```

---

## 知识边界与注意事项

- **时效性**：本 skill 的模型数据截至 **2026-04**。如果用户问"最近出的 X 模型"，**必须先用 WebSearch 验证**，不要凭记忆瞎答。
- **不要推荐 2024 已过时的 benchmark**（MMLU、HumanEval、GSM8K）作为主要依据——见 framework.md 附录 A 的 ☆ 标记。
- **中文场景特殊**：Qwen、GLM、DeepSeek、Kimi 在中文任务上常常超过闭源英文首选，不要默认推闭源。
- **思考模式（Thinking / Extended Thinking）**是同一模型的不同档位，**必须说清你在比哪一档**。
- **不要给"综合榜第一名"作为推荐**——总是按具体任务匹配具体 benchmark。

---

## Resources

- `resources/framework_pointer.md` — 指向 `docs/LLM_evaluation_framework.md` 的快速索引
- `resources/eval_template.csv` — 自建 eval set 模板
- `resources/judge_prompt.md` — LLM-as-judge 评分官 prompt 模板
- `resources/cost_calculator.py` — Token 成本核算脚本
- `resources/decision_checklist.md` — 五步决策流的打印友好版

## Related Skills

- `brainstorming`：当用户对任务目标模糊时先用此 skill 澄清
- `competitive-analysis-s1`：当需要对比多个 AI 产品（而非模型）时用此 skill
- `ai-product-manager-toolkit`：PRD、LLM 失败模式等配套模板

## Visual References

- 决策流程图（FigJam）：https://www.figma.com/board/Dz5LV87T04lWlrCvGQKfPn/LLM-%E9%80%89%E5%9E%8B%E4%BA%94%E6%AD%A5%E5%86%B3%E7%AD%96%E6%B5%81
- 模型能力对比表：https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC?node-id=8-2
- 场景 → 模型决策矩阵：https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC?node-id=4-2
- Figma 源文件：https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC
