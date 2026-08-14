# LLM 评估与选型框架

> **适用对象**：AI 产品经理（非开发者背景）
> **更新时间**：2026-04
> **来源**：基于 `refer/evaluate/evaluate-LLM/` 的 2024 版小红书笔记，结合 2026 Q1 前沿模型现状重构

---

## 1. 引言：为什么 2024 的评测维度需要更新

原参考资料整理了 6 个评测维度（基础能力 / 行业扩展 / 安全 / 系统性能 / 用户体验 / 可解释性），覆盖面完整，但 2024 年以来出现了三个结构性变化，使原框架无法直接使用：

1. **旧 benchmark 集体失效**：MMLU、HumanEval、GSM8K、BBH、LongBench v1 等已被前沿模型"刷爆"（≥95%），区分度消失，必须替换为 MMLU-Pro、HLE、SWE-bench Verified、RULER、LongBench v2 等新一代基准。
2. **Agentic 能力成为独立维度**：2025 年以后，模型能否自主调用工具、操作浏览器 / 终端 / 桌面、完成多步任务，成为衡量模型的核心指标。原文完全缺失这一大类。
3. **"思考模式"（Extended Thinking / Reasoning）分叉**：同一模型出现 fast 和 thinking 两档（Claude Opus 4.6、Gemini 3.1 Thinking、DeepSeek V3.2 Thinking、GPT-5.x），选型时必须明确比哪一档。

本文档把原 6 维度重构为 **PM 决策导向的 4 层体系**，补上 2026 最新 benchmark 与模型对比，并给出可执行的 5 步选型流程。

---

## 2. 四层评估体系

原文的 6 维度信息完整但颗粒度不均。本文按 **PM 选型决策链** 重新组织成 4 层，每层回答一个业务问题：

| 层级 | 回答的问题 | 对应原文维度 |
|---|---|---|
| **L1 能力层** | 模型"能不能做"？ | 基础 AI 能力 + 行业扩展能力 |
| **L2 可信层** | 结果"可不可靠"？ | 安全合规 + 可解释性 |
| **L3 工程层** | 能不能"稳定上线"？ | 系统性能 |
| **L4 价值层** | 用户"愿不愿用"、业务"划不划算"？ | 用户体验与业务价值 |

**分层的好处**：PM 做选型时可以**短路淘汰**——
- L1 不达标 → 直接淘汰候选
- L2 不达标 → 进风控名单或限制场景
- L3 不达标 → 工程延期或加缓存/路由
- L4 是最终决策：前面都过了，这一层决定上不上

### 2.1 L1 能力层

按业务相关性选择子维度，**不要追求全量**。

| 子维度 | 2026 推荐 benchmark | PM 判断标准（最低可用线） |
|---|---|---|
| 通用知识 | MMLU-Pro、HLE | MMLU-Pro ≥75% |
| 推理 | GPQA-Diamond、AIME、ARC-AGI-2 | GPQA ≥85% 才算前沿 |
| 代码 | SWE-bench Verified、LiveCodeBench、TerminalBench | SWE-bench V ≥70% 是编码 agent 起步线 |
| 长上下文 | RULER、LongBench v2 | 看**有效**长度而非标称窗口 |
| 多模态 | MMMU、MathVista、Video-MME | 分开评估图像/视频/音频 |
| **Agentic**（新增） | OSWorld、τ-bench、GAIA、BrowseComp | 做 agent 产品必看 |
| 指令遵循 | IFEval、MT-Bench | IFEval ≥90% 才能做严格结构化输出 |
| 行业知识 | LawBench、MedQA、FinBen、SciBench | 垂直场景必跑 |

### 2.2 L2 可信层

| 子维度 | 关注点 | 推荐 benchmark |
|---|---|---|
| 有害内容抵制 | 越狱鲁棒、拒答率 | HarmBench、AdvBench |
| 过度拒答 | 避免"又傻又拒" | XSTest |
| 幻觉 | 事实性、引用准确 | SimpleQA、FActScore、TruthfulQA |
| 可追溯 | 原生 citation / tool trace | 看文档（Claude / Gemini 原生支持） |
| 偏见 | 社会偏见、歧视 | BBQ、StereoSet |

### 2.3 L3 工程层

| 指标 | 含义 | 怎么测 |
|---|---|---|
| TTFT | 首 token 延迟 | 自测 p50/p95/p99 |
| TPOT | 每 token 延迟 | 自测 |
| 吞吐 | tokens/sec、QPS | 压测 |
| 稳定性 | uptime、错误率 | 监控 API |
| 部署形态 | API / 开源 / 私有化 / 端侧 | 看厂商 |
| 成本 | $/M input、$/M output、caching 折扣 | 查价目表 + 实际 DAU |

### 2.4 L4 价值层

| 指标 | 含义 | 数据源 |
|---|---|---|
| **任务完成率** | 业务自建 eval 的通过率 | **最重要**，远超 public benchmark |
| CSAT / NPS | 用户满意度 | 产品内问卷 |
| 留存 / DAU | 业务指标 | 数据看板 |
| 单位经济 | 每对话成本 / 每用户毛利 | 财务核算 |

---

## 3. 2026 主流模型快照

### 3.1 闭源前沿（截至 2026-04）

| 模型 | 厂商 | 定位 | GPQA | SWE-bench V | 强项 | 性价比 |
|---|---|---|---|---|---|---|
| **Gemini 3.1 Pro** | Google | 综合第一 | **94.3%** | ~78% | 推理 / 多模态 / 长上下文 / 价格 | ★★★★★ |
| **Claude Opus 4.6** | Anthropic | 代码王 | 91.3% | **80.8%** | Agentic coding、安全、写作 | ★★★ |
| **GPT-5.4** | OpenAI | 通用强 | ~89% | ~85%（Codex 变体） | 生态、工具、多模态 | ★★★ |
| **Grok 4** | xAI | 实时 / 弱对齐 | ~85% | — | 实时数据、宽松策略 | ★★★ |

### 3.2 开源 / 中国前沿

| 模型 | 厂商 | 开放度 | 亮点 |
|---|---|---|---|
| **GLM-5** | 智谱 | 开源权重 | 开源 SWE-bench V 第一（77.8%），Arena Elo 1451 |
| **Qwen 3.5** | 阿里 | 开源 | 开源 GPQA 最高 88.4%，IFEval 92.6% |
| **DeepSeek V3.2** | DeepSeek | 开源 | 极致性价比，Thinking 变体综合分 66 |
| **Kimi K2.5** | Moonshot | 开源 | LiveCodeBench 85，长上下文老本行 |
| **Llama 4** | Meta | 开源 | 生态最活跃，易微调定制 |

### 3.3 与原文 2024 版的关键变化

1. **开源 vs 闭源差距基本抹平** — 原文还在把"支持商业定制"作为开源的主要卖点，2026 开源模型已在多个 benchmark 上与闭源持平
2. **中国模型崛起** — 开源前 12 里中国厂商占 7 席（DeepSeek、Qwen、智谱、Moonshot、小米、阶跃等）
3. **Agentic 成主战场** — Computer use、Deep Research、Coding Agent 这三类产品形态在 2025 才成熟
4. **思考模式分叉** — 同一模型家族有 fast / thinking 两档，延迟和精度权衡完全不同

---

## 4. PM 五步决策流

原文最缺的部分。按顺序走，**不要跳步**。

### Step 1：定义任务画像（先画靶子再射箭）

问自己 4 个问题：
- **任务形态**：chat / RAG / agent / batch / realtime？
- **关键能力**：推理？代码？长文？多模态？工具调用？
- **容忍度**：幻觉代价？延迟上限？成本上限？
- **合规要求**：数据能出境吗？要私有化吗？行业资质？

### Step 2：Benchmark 初筛（砍掉 80% 候选）

**原则：只看与你任务相关的 1-3 个 benchmark，不要看综合榜**
- 编码 agent → SWE-bench Verified + TerminalBench
- 科研问答 → GPQA + HLE
- 长文档 RAG → RULER + LongBench v2
- 通用 chat → Arena Elo + MT-Bench
- Computer use → OSWorld + GAIA

### Step 3：自建 eval set 实测（决定性环节）

**Public benchmark 会被训练集污染，自建 eval 才是真相**。
- **量级**：50-200 条真实任务样本
- **评分**：LLM-as-judge（用更强的模型打分）+ 人工抽检 20%
- **对比**：候选 2-3 个模型并行跑同一批
- **格式**：每条样本包含 input、expected output（或 rubric）、tags

### Step 4：工程 & 成本核算

- **真实成本** = (平均输入 tokens × 输入价) + (平均输出 tokens × 输出价) × 预期 DAU × 日均对话数
- **延迟**：p95 TTFT 是否小于业务容忍（客服 <2s、批处理 <30s）
- **可得性**：rate limit、region、SLA、数据主权

### Step 5：灰度 & A/B

- **5% 流量灰度** → 监控任务完成率、CSAT、拒答率、成本
- **2 周观察期** → 决策：全量 / 回滚 / 多模型路由（贵任务走强模型、简单任务走便宜模型）

---

## 5. 场景 → 模型 决策矩阵

| 业务场景 | 2026 首选 | 备选 | 决策依据 |
|---|---|---|---|
| 编码 Agent / Copilot | **Claude Opus 4.6** | GPT-5.3 Codex、GLM-5 | SWE-bench Verified |
| 科研 / 教育 / 深度问答 | **Gemini 3.1 Pro** | Claude Opus 4.6 | GPQA-Diamond |
| 长文档 RAG | **Gemini 3.1 Pro** | Kimi K2.5 | RULER + 价格 |
| 中文客服 / 内容生成 | **Qwen 3.5 / GLM-5** | 通义闭源 API | 中文语感 + 合规 |
| 极致成本 batch 任务 | **DeepSeek V3.2** | Qwen 3.5 开源 | $/token 最低 |
| 端侧 / 私有化 | **Llama 4 / Qwen 3.5** | Mistral | 权重可得性 |
| 严管合规（金融 / 医疗） | **Claude Opus 4.6** | 国产闭源 API | 安全 + 可追溯 |
| Computer use / RPA | **Claude Opus 4.6** | GPT-5.4 | OSWorld |
| Deep Research | **Gemini 3.1 Pro** | GPT-5.4 | BrowseComp |

---

## 6. Benchmark 速查（精简版）

按业务选 1-3 个，**不要追求大而全**：

| 你的业务 | 必看 benchmark |
|---|---|
| 通用 chat / 客服 | Chatbot Arena Elo + IFEval + XSTest |
| 编码 agent | SWE-bench Verified + TerminalBench + LiveCodeBench |
| 科研 / 教育 / 深度问答 | GPQA-Diamond + HLE + MMLU-Pro |
| Computer use / RPA | OSWorld + τ-bench + GAIA |
| 长文档 RAG | RULER + LongBench v2 + SimpleQA |
| 多模态 | MMMU + MathVista + Video-MME |
| 数学 / 推理 | GPQA + AIME + ARC-AGI-2 |

> 各 benchmark 的详细背景、出题方式、前沿分数、有效性评估，见 **附录 A**。

---

## 7. 可视化参考

配套三张 Figma 产出（可直接点开编辑 / 截图嵌入 PRD）：

- **决策流程图（FigJam）** — [LLM 选型五步决策流](https://www.figma.com/board/Dz5LV87T04lWlrCvGQKfPn/LLM-%E9%80%89%E5%9E%8B%E4%BA%94%E6%AD%A5%E5%86%B3%E7%AD%96%E6%B5%81)
- **模型能力对比表** — [2026 主流 LLM 能力对比](https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC?node-id=8-2)
- **场景 → 模型决策矩阵** — [7 场景卡片](https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC?node-id=4-2)
- Figma 源文件（可 fork）：[LLM 2026 能力对比 & 场景决策矩阵](https://www.figma.com/design/A4MhEf0q2GnA2wk7Bt3zhC)

---

# 附录 A：Benchmark 完整详解

> **标记说明**：
> - ★ = 2026 仍然有效
> - ☆ = 已过时 / 饱和，**不建议再看**
> - ⚡ = 2025 年后才出现的新基准

## A.1 通用知识与推理

- **MMLU** ☆ — 57 学科 4 选一选择题，2019 年出。**已饱和**：前沿模型都 ≥90%。2026 基本不看。
- **MMLU-Pro** ★ — MMLU 升级版。**10 选一**（选项更多、抗蒙猜）、12,000 道研究生级题、14 学科、强调推理。2026 取代 MMLU 的首选通识 benchmark。
- **GPQA-Diamond** ★ — "Google-Proof Q&A"。PhD 出题的生物/化学/物理题，专业 PhD 能答 65%+，非专业 PhD 只 34%。**衡量真·专家推理的黄金标准**。2026 前沿：Gemini 3.1 Pro 94.3% / Claude Opus 4.6 91.3% / GPT-5.3 Codex 81%。
- **HLE (Humanity's Last Exam)** ⚡★ — Scale AI + CAIS 2025 推出，刻意选"人类最难"的题。前沿模型目前 30-40%，**分辨力强**，要看前沿差距就看这个。
- **ARC-AGI-2** ⚡★ — François Chollet 的抽象推理升级版。衡量"真·泛化推理"而非记忆。前沿普遍只有 5-20%，Gemini 3.1 Pro 77.1% 是 2026 爆点。
- **BBH (BIG-Bench Hard)** ☆ — 2022 的 23 个推理任务。已饱和。
- **GSM8K / MATH** ☆ — 小学 / 高中数学。已饱和。
- **AIME 2024/2025** ⚡★ — 美国数学邀请赛真题。Reasoning 模型必跑，Claude Extended Thinking / GPT o 系列 / DeepSeek Thinking 都报这个。

## A.2 代码能力

- **HumanEval / MBPP** ☆ — 164 / 974 道简单函数题，2021 年。**已彻底失效**：前沿都 ≥95%，训练集污染严重。2026 不看。
- **SWE-bench Verified** ★ — Princeton + OpenAI 从真实 GitHub issue 改编，让模型**在真实 repo 里修 bug**。500 条人工验证过的任务。**2026 评价"能否做编码 agent"的唯一权威**。前沿：Claude Opus 4.6 80.8% / GPT-5.3 Codex 85% / GLM-5 77.8%（开源第一）。
- **LiveCodeBench** ⚡★ — 2024 推出，每月从 LeetCode / AtCoder / Codeforces 拉**新题**防污染。看算法编码能力。Kimi K2.5 85 很强。
- **TerminalBench** ⚡★ — Anthropic 2025 推，让模型在真实 terminal 里完成任务（pip install、调试、多步命令）。衡量**命令行 agent 能力**。
- **Aider Polyglot** ⚡★ — 多语言真实编辑任务（不只 Python）。
- **BigCodeBench** ★ — HumanEval 的严格升级版，1140 道真实 library 调用题。

## A.3 长上下文

- **Needle-in-a-Haystack (NIAH)** ★ — "大海捞针"。在长文本里埋一句话让模型找。**太简单**，前沿都 100%，已不是好 benchmark 但仍在用。
- **RULER** ⚡★ — NVIDIA 2024 推，13 个任务综合评估长文本：多针查找、变量追踪、多跳推理。**真实有效**。许多"1M context"模型 RULER 128K 就崩。
- **LongBench v2** ⚡★ — 清华 2024 升级版，真实长文档问答（法律 / 学术 / 代码 repo）。
- **InfiniteBench** ★ — 100K+ tokens 多任务长文本。

## A.4 多模态

- **MMMU** ★ — 大学考试级多模态题（图+文），11,500 题覆盖艺术 / 商科 / 科学 / 医学。**2026 图像理解首选**。
- **MathVista** ★ — 视觉数学推理。
- **Video-MME** ⚡★ — 2024 推出，衡量视频理解，Gemini 系列有优势。
- **ChartQA / DocVQA** ★ — 图表 / 扫描文档问答。RAG 必看。
- **AudioSet / VQA** ☆ — 老基准，2024 原文提到，2026 已不作为主要参考。

## A.5 Agentic（原文完全缺失的一大类）

- **OSWorld** ⚡★ — 2024 推出，真实 Ubuntu / Windows 桌面环境让模型完成 369 个任务（点按钮、填表、文件管理）。**衡量 computer use 能力**。
- **BrowseComp** ⚡★ — OpenAI 2024 推，衡量深度网页浏览 + 信息聚合。Deep Research 类产品选型必看。
- **τ-bench (tau-bench)** ⚡★ — Sierra AI 2024 推，模拟真实客服 agent 场景（订票、退货），衡量**多轮工具调用 + 策略遵循**。
- **GAIA** ⚡★ — Meta 2023 推的通用 AI assistant benchmark，多步推理 + 工具 + 多模态，466 题。
- **WebArena / VisualWebArena** ★ — 网页 agent benchmark。

## A.6 指令遵循 & 对话质量

- **IFEval** ⚡★ — Google 2023 推，**可验证的**指令遵循（"必须含 3 个 bullet"、"不超过 100 字"这类硬约束）。严格结构化输出场景必看。Qwen 3.5 92.6% 开源第一。
- **MT-Bench** ★ — LMSYS 的多轮对话质量（GPT-4 打分）。已有点旧但仍常用。
- **Arena Hard** ⚡★ — LMSYS 从真实 Chatbot Arena 提取的硬题。
- **Chatbot Arena (LMSYS)** ★ — **人类盲选投票的 Elo 分**。Gemini 3.1 Pro 接近 1500，GLM-5 开源第一 1451。**最贴近真实用户体感**。

## A.7 安全与可信

- **HarmBench** ⚡★ — CAIS 2024 推，标准化越狱 / 有害内容测试。
- **XSTest** ★ — 测试**过度拒答**（防"帮我杀死 Python 进程"被拒）。
- **TruthfulQA** ★ — 衡量是否产生常识性谎言。
- **SimpleQA** ⚡★ — OpenAI 2024 推，简单事实题，**测幻觉率**。前沿模型 40-60%。
- **FActScore** ⚡★ — 长文生成的事实性细粒度评分。
- **BBQ** ★ — 社会偏见问答。

## A.8 行业垂直

- **LawBench / LegalBench** ★ — 法律领域。
- **MedQA / MedMCQA / USMLE** ★ — 医学考试题。
- **FinBen** ⚡★ — 金融任务综合。
- **SciBench** ★ — 大学科学题。

---

# 附录 B：2024 原文维度 → 2026 更新对照

| 2024 原文维度 | 2024 原文 benchmark | 2026 更新后 | 状态 |
|---|---|---|---|
| 语言理解 | SQuAD, MMLU, CMRC | MMLU-Pro, HLE | **替换** |
| 生成与表达 | BLEU, ROUGE, 人工打分 | Arena Elo, MT-Bench, IFEval | **替换** |
| 事实性 / 知识储备 | TriviaQA, TruthfulQA | SimpleQA, FActScore, TruthfulQA | **增强** |
| 数理推理 | GSM8K, MATH | GPQA-Diamond, AIME, ARC-AGI-2 | **替换** |
| 代码能力 | HumanEval, MBPP | SWE-bench Verified, LiveCodeBench, TerminalBench | **替换** |
| 长上下文 | LongBench, MassiveDoc | RULER, LongBench v2 | **替换** |
| 多模态 | VQA, ImageNet, AudioSet | MMMU, MathVista, Video-MME | **替换** |
| 行业定制 | LawBench, MedQA | LawBench, MedQA, FinBen, SciBench | **保留 + 扩展** |
| 工具 / 插件集成 | 内部定制用例 | τ-bench, OSWorld, GAIA（公开 benchmark） | **规范化** |
| 个性化与记忆 | A/B + 人工评估 | 同上（无公认 benchmark） | **保留** |
| 安全与合规 | Toxicity, Harassment | HarmBench, XSTest, BBQ | **替换** |
| 系统性能 | p95/p99, QPS, Uptime | 同左 | **保留** |
| 用户体验 | CSAT, NPS, DAU, Token 成本 | 同左 | **保留** |
| 可解释性 | Chain-of-thought | Extended Thinking / Thinking Models（形态变化） | **演进** |
| — | （原文无） | **Agentic 能力（新增一大类）** | **新增** |
| — | （原文无） | **思考模式 fast / thinking 分叉** | **新增** |

---

# 参考来源

- [Best AI Models April 2026: Ranked by Benchmarks](https://www.buildfastwithai.com/blogs/best-ai-models-april-2026)
- [Artificial Analysis LLM Leaderboard](https://artificialanalysis.ai/leaderboards/models)
- [LM Council Benchmarks April 2026](https://lmcouncil.ai/benchmarks)
- [2026 LLM Leaderboard — Klu](https://klu.ai/llm-leaderboard)
- [LLM Benchmarks 2026: MMLU-Pro, GPQA, HLE, LiveCodeBench — CodeSOTA](https://www.codesota.com/llm)
- [Best Chinese LLMs in 2026 — BenchLM.ai](https://benchlm.ai/blog/posts/best-chinese-llm)
- [China's LLM Landscape in 2026 — MerchMindAI](https://merchmindai.net/blog/en/post/china-llm-landscape-2026)
- 原始素材：`refer/evaluate/evaluate-LLM/*.jpg`（2024 版小红书笔记）
