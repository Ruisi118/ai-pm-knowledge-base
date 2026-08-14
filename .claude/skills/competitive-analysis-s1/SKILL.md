---
name: competitive-analysis-s1
description: Comprehensive AI product competitive analysis framework based on the "知行合一" (Knowledge-Action Unity) methodology. Use this skill when conducting deep competitive research on AI products, analyzing market positioning, reverse-engineering product features, or building systematic product intelligence. Ideal for PM tasks like market research, product strategy, feature benchmarking, and competitive intelligence gathering.
---

# AI Product Competitive Analysis (知行合一 Framework)

## Overview

This skill provides a systematic framework for conducting deep competitive analysis of AI products, based on the "知行合一" (Knowledge-Action Unity) methodology. It guides you through three phases: **Input** (building knowledge base), **Process** (hands-on investigation), and **Output** (structured insights).

The framework helps Product Managers go beyond surface-level comparisons to truly understand:
- How competitors built their products
- What technical decisions they made and why
- Where the real competitive moats are
- How to validate assumptions through hands-on testing

## Core Methodology: The Knowledge-Action Unity Loop

```
Input (输入) → Process (内化) → Output (输出)
    ↑                                    ↓
    └────────── Continuous Learning ──────┘
```

### 输出约束确认（执行前）

在开始竞品分析前，确认以下三项：
1. **范围**: "我将创建/修改 [具体文件]，对吗？"
2. **格式**: "我将使用 [竞品画布/完整三阶段报告/快速对比表]，需要换一个吗？"
3. **语言**: "输出将使用 [中文/英文/混合]，对吗？"

⚡ 如果用户请求已明确指定以上三项，跳过此步直接执行。

---

## Phase 1: Input - Building High-Dimensional Knowledge Base

**Goal**: Establish information sources across business/technical/engineering dimensions.

### 1.1 Business & Strategy Layer (看"钱"和"竞争")

**Objective**: Understand why this technology can make money and who's buying in.

**Information Sources**:

- **VC Perspective**: Follow a16z, Sequoia, Benchmark blogs
  - They publish "Market Maps" before tech explosions
  - Ask: Why is this track hot? What's the VC's thesis?

- **Founder Perspective**: Follow Y Combinator, Lex Fridman Podcast, Latent Space
  - Focus: What painful problems are founders trying to solve? (That's the real tech bottleneck)

- **Enterprise Background**: Track what big companies (Google, NVIDIA, etc.) are building
  - Focus: Their product array, commercial layout

- **Leader Trajectories**: Follow their leadership roles, growth paths
  - Observe how they make decisions at each crossroad

**Action Item**: Select one deep-dive article weekly and draw the **Value Chain Map** (Model → Middleware → App → User)

### 1.2 Technology & Frontier Layer (看"可能性"和"边界")

**Objective**: Know what products exist, what models can do, what's impossible, and what might be possible soon.

**Information Sources**:

- **Hugging Face Daily Papers**: Browse high-vote paper abstracts daily
  - Don't read everything - just scan Task and Result sections

- **Twitter (X) Tech Circle**: Follow AI scientists (Karpathy, LeCun, Yi Tay)
  - Tech breakthroughs appear first via "tweets" or "retweets"

- **Product Hunt**: Check daily rankings for standout products

- **Techmeme**: Track news and product launches

- **Tech Blogs**: See what tech they use, how they build evaluation sets, what dimensions matter (accuracy, safety, long-context)

**Action Item**: Build a **"Technical Terminology Database"**. When you see unfamiliar terms (e.g., KV Cache, MoE, Diffusion Transformer), look them up or ask Claude to explain.

### 1.3 Open Source & Engineering Layer (看"实现路径")

**Objective**: See how others turn "theory" into "code".

**Information Sources**:

- **GitHub Trending (Python)**: Check weekly

- **LangChain / LlamaIndex Official Docs**: Their doc updates represent industry consensus on Agent orchestration

**Action Item**: When encountering a new track (e.g., AI video), go to GitHub, search for top-starred open-source projects, and review their README.md and Architecture Diagram.

## Phase 2: Process - Hands-On Investigation & Reverse Engineering

**Core Difference for AI PMs**: Don't just read documents - actually test AI products. As an AI PM, you may not write production code, but you must understand what's technically feasible.

### 2.1 Multi-Dimensional Competitive Product Analysis

#### Strategic Layer

**Target User Persona**: Who is this for? (B2B enterprise? C2C mass market? Developers? Specific industries like healthcare/law?)
- Research Points: Examine their official slogan, use cases, community active users

**Core Value Proposition**: How do they define themselves in one sentence?
- Examples: Claude is "安全且善解人意" (Safe and Understanding), Midjourney is "极具艺术感" (Extremely Artistic)
- Ask: What's their "root value proposition"?

**Differentiation Moats**: What are they betting on?
- Data monopoly? Algorithm advantage? Low pricing? Strong ecosystem plugins?

#### Experience Layer

**Interaction Paradigm**: Traditional linear chat? Dual-pane canvas (Canvas/Artifacts)? Copilot companion mode?

**Onboarding & Guidance**: Cold start experience - is the registration process cumbersome? Are there novice guides?

**Features**: What are the core features? What are the highlight features?

**UI/Interface**: Why does it feel premium? Consider typography, micro-interactions, animation fluidity, information architecture (collapsible multi-level folding vs.展开).

#### Business Layer

**Business Model**: Freemium (free + internal purchase)? Subscription (SaaS)? Pay-as-you-go?

**Pricing Strategy**: Membership tiers - what's free? How much for Pro? What management features for Team?
- Research: E.g., ChatGPT Plus costs $20, competitor costs $10 or $30? Any annual discounts?

**Growth Mechanisms**: Invitation/viral mechanisms? (Invitation incentives/limits) Or referral broadcast mechanisms? (Generated content links are watermarked with own brand?)

#### Capability Layer

**a. Modality Dimension (Form)**: What can it "see/hear"?

This is the most intuitive capability difference, determining how many use cases AI can cover.

**Multimodality Input**:
- **Vision**: Support image uploads? How many images? Can it recognize handwriting, charts, code screenshots?
- **Documents**: Supported file formats (PDF, Word, Excel, CSV, Markdown, etc.)? File size limits?
- **Audio/Video**: Can it directly "listen" to audio? Can it analyze uploaded video files (Video Understanding)?
- **URL/Links**: Can it directly read webpage links? Does it only fetch HTML or can it deeply parse and analyze page content?

**b. Volume Dimension (Volume)**: How much can it "remember"?

Tests AI's ability to handle long content continuity.

- **Context Window**: Maximum supported token count (e.g., 8k, 32k, 128k, 1M+)
- **Needle in a Haystack Capability**: After ultra-long text input, can it accurately answer questions about specific details?
- **Multi-turn Dialogue Memory**: After 10 or 20 rounds of conversation, can it still remember constraints from round 1? (E.g., "Please use JSON format for all responses")
- **Parallel Processing**: Can it handle multiple files at once? (E.g., "Compare these three PDF differences")

**c. Understanding Dimension (Understanding)**: How well does it understand "human language"?

Tests AI's robustness to prompts.

- **Fuzzy Instruction Recognition**: Input "Help me write that thing..." - does Claude proactively ask for clarification or generate randomly?
- **Structured Instruction Compliance**: Input complex logic problems - "First summarize, if condition A is met then output B, otherwise output C, must use Markdown table format" - does it follow strict format?
- **Ambiguous Wording & Context**: Input queries with sentiment or metaphors - test AI's contextual and sentiment recognition
- **Safety & Refusal Mechanisms**: Input sensitive queries (involving privacy, bias, attack content) - are product's defense mechanisms strong enough to guide rejection?

### 2.2 AI-Assisted "Reverse Engineering" (Inferring System Instructions)

**Goal**: Like a hacker, disassemble competitors, use AI to "see through" and infer competitor's Prompt strategies and model parameters.

**💡 Direct Question**: "I'm conducting competitive product research for XX product. Please help me perform reverse engineering."

Or consider different scenarios to ask separately:

#### 🔷 Reverse System Prompt

You know what the product is "calling" and what model type, so let AI help analyze the product's output characteristics.

- **Example**: Found product generates well-structured articles with clear non-repetition.
- **Prompt**: "I input the instruction 'Analyze AI phone market' to the competitor, and it output the following content: [paste generated long text]. As a Prompt Engineer, please reverse-engineer what the competitor's **System Prompt** might be. What prompt techniques might it use (e.g., role-playing, chain-of-thought CoT, Few-Shot) to achieve such clear structure and professional tone?"

#### 🔷 Diagnose "Hallucination" Sources

- **Example**: Competitor got an answer wrong - you want to know if it's model error or data error.
- **Prompt**: "The competitor got the timing of 'Musk's acquisition of Twitter' wrong. Please analyze possible reasons: 1- Is it because the model knowledge cutoff date is too old? 2- Is it because RAG retrieved incorrect old news? 3- If it's RAG error, is it usually because chunking is too fragmented causing context loss? Please explain in layman's terms."

#### 🔷 Infer Underlying Model

Competitor responds very fast but seems a bit dumb? Or responds slowly but has super logic? Let AI help diagnose.

- **Example**: Competitor supports uploading PDFs with extremely fast response, but sometimes fabricates.
- **Prompt**: "I'm testing a document dialogue product. Observations: 1- Upload 100-page PDF, understands in seconds (no delay); 2- High probability of guessing. Is it most likely using long-context model or RAG (Retrieval-Augmented Generation)? Why? What are the characteristics of this tech's inaccurate responses?"

### 2.3 DIY "Low-Code" Quick Validation Logic (For Deeper Technical Understanding)

**"Read"**: Understand open-source project principles. Find a similar product open-source project, upload its architecture documentation.

**"Run" - Advanced**: Run micro prototype projects. Treat it as an "MVP (Minimum Viable Product)" to validate feasibility.

**Examples**:

**a. Pure Impression "AI Legal Assistant"**: Set up a knowledge base on Dify, upload several legal documents, configure RAG nodes.

- Gain: You'll immediately discover RAG pain points (retrieval inaccuracy, chunking too fragmented, responses too generic), helping you cautiously use product analysis.

**b. Want to understand "What's an end-to-end RAG project architecture?"**: Have AI help search and clone (e.g., research AI simulator gpt-researcher) - use Cursor to open and ask: "Please explain this project's core workflow. How does it overcome insufficient context memory?" - Let Cursor help you understand code and run Demo.

**Reuse Value**: Even if you can't understand a line of code, running and testing helps you understand the real difficulty of engineering implementation (dependency conflicts, API delays, memory overflow, etc.).

## Phase 3: Output - Structured Product Insights

Transform entire research results and your own understanding into organized deliverables for subsequent competitive research reports and personal growth, as well as commercial value.

### 3.1 AI Competitive Product Research Canvas (Template)

| Dimension | Question List | Validation Method |
|-----------|---------------|-------------------|
| **Scenario (Scene)** | What main problem does this product solve? (Detection), which category prediction (Speech), generate or drive (Agent)? | Experience core path |
| **Model** | What underlying model might it use? Does it use multiple models (SFT)? Or call third-party Prompt Engineering? | Evaluate, check version iterations, test latency |
| **Data** | What kind of data does it rely on to win? User-side data, what data did you break through that others can't understand? (This is the moat) | Find similar papers, personalization attempts |
| **UX** | How to handle latency? How to handle complex output (structure)? Is there an index function? What clone usage issues? | Black-box test, offline test, streaming interruption |
| **Cost** | How many Tokens consumed per interaction? Besides model selection, is the window super large? Are API costs high? | Estimate Input/Output Token count |

### 3.2 AI PM Competency Growth Canvas (The Competency Growth Canvas)

Use this canvas to track learning through each competitive research cycle.

**Pre-Research (Plan)**: Fill left column. Clarify what technical points you want to understand through this research, or what assumptions to validate.

**Post-Research (Review)**: Fill right column. Honestly face your gaps, record "gut feelings".

**Project Name**: _________________ (Example: Deep Research Agent Survey)

**Time Period**: //____ - //_____

| Competency Dimension | Step 1: Pre-Mortem Goals (Pre-Research) | Step 2: Actual Actions (为了搞懂它, 我做了什么?) | Step 3: Post-Mortem & Gaps (Post-Research) |
|---------------------|----------------------------------------|-------------------------------------------|-------------------------------------------|
| **Tech Literacy** | Concepts I want to build:<br>□ RAG principles<br>□ Agent workflow<br>□ Fine-tuning<br>□ Tokenization | What I practiced:<br>(Example: I wrote a simple RAG Demo in Python, manually tested chunk, rerank, size parameters)<br>1.<br>2. | My knowledge upgrade:<br>(Example: Originally thought cutting too small would cause loss, but actually not getting summary right is more important. Personally verified through hands-on.)<br>Rating (0-10): ____ |
| **Product Sense** | Questions I want to validate:<br>□ Experience cost<br>□ Scenario pain points<br>□ Value capture | What I observed:<br>(Example: I spent 30 minutes experiencing the user workflow. My intuition is correct.)<br>1.<br>2. | Verified knowledge:<br>(Example: This product's onboarding is indeed counter-intuitive (Progress Bar), I was stuck for 10+ cards in the past.)<br>Rating (0-10): ____ |
| **Engineering** | Challenges I want to experience:<br>(Example: I want to see how complete API calls are made.)<br>□ Read source code<br>□ Disassembly analysis<br>□ Low-code verification | What I did:<br>(Example: I used F12 to find 2 product hidden prompts.)<br>1.<br>2. | Obstacles from insufficient tech:<br>(Example: Don't understand WebSocket data flow, will complement internet protocol next time.)<br>Rating (0-10): ____ |
| **Business Insight** | Estimates I want to validate:<br>(Example: Should the product be so cheap to attract users?)<br>□ Cost estimation<br>□ Scenario judgment | What I calculated:<br>(Example: I tested GPT-4o pricing, they might lose 5 RMB per small order, but should use lower models.)<br>1.<br>2. | Insights validated by business:<br>(Example: Removing them may be for retention, telling users they can't live without it.)<br>Rating (0-10): ____ |

### 3.3 Knowledge Artifacts to Accumulate Over Time

- **Professional Terminology Wiki**: For future queries when encountering similar professional terms
- **Prompt Template Library**: Record your Prompt debugging experience
- **Bad Case Log**: Collect screenshots of competitor failures, avoid pitfalls early
- **Interaction Inspiration Gallery**: Collect excellent AI UI designs (like Copilot's floating window)
- **Technical Architecture Diagrams**: Use mind map format to record technical understanding
- **Business Market Research Notes**: PMs need keen insights into business and markets beyond products

## Usage Examples

### Example 1: Quick Competitive Analysis Request

**User**: "Help me do competitive analysis on ChatGPT's new Canvas feature"

**Claude Response**:
I'll guide you through a systematic competitive analysis using the 知行合一 framework:

**Phase 1: Input (Information Gathering)**
Let me first help you gather information across three layers:
1. Business layer: I'll search for what VCs/founders are saying about collaborative AI interfaces
2. Technical layer: I'll look for papers and discussions about multi-pane AI interactions
3. Engineering layer: I'll check if there are open-source implementations

**Phase 2: Process (Hands-On Investigation)**
Then I'll help you:
- Analyze Canvas across strategic/experience/business/capability dimensions
- Reverse-engineer potential system prompts
- Identify technical implementation patterns

**Phase 3: Output (Structured Insights)**
Finally, I'll help you create:
- Filled competitive analysis canvas
- Key findings and recommendations
- Competency growth tracker

Would you like me to proceed with this analysis?

### Example 2: Reverse Engineering Request

**User**: "I found that Claude always structures its code responses with clear explanations. How can I figure out what system prompt they're using?"

**Claude Response**:
Great reverse engineering question! Let me help you analyze this systematically:

**Reverse Engineering Approach**:

1. **Output Pattern Analysis**:
   - Consistent structure suggests template-based system prompt
   - Clear explanations indicate instruction to "explain reasoning"
   - Code quality suggests "follow best practices" directive

2. **Hypothesis Testing**:
   Let me help you craft test prompts to validate assumptions:
   - Test edge cases to see if structure breaks
   - Test different complexity levels
   - Test different programming languages

3. **System Prompt Inference**:
   Based on observed patterns, likely system prompt elements:
   - Role definition ("You are an expert programmer")
   - Output structure requirements ("Explain before coding")
   - Quality standards ("Follow best practices", "Add comments")
   - Formatting instructions ("Use markdown code blocks")

Would you like me to help you design specific test cases to validate these hypotheses?

## When to Use This Skill

✅ **Use this skill when**:
- Conducting competitive product research for AI products
- Building market intelligence on AI features
- Reverse-engineering competitor capabilities
- Planning product roadmaps based on market analysis
- Learning about AI product design patterns
- Validating product hypotheses through competitive insights

❌ **Don't use this skill for**:
- General market research (non-AI products)
- Financial competitive analysis
- Legal compliance research
- Quick feature comparisons (use this for DEEP analysis)

## Additional Resources

See the references/ directory for:
- Detailed templates for each canvas
- Information source directories with links
- Example completed analyses
- Prompt libraries for reverse engineering
