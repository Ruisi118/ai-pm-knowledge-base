# AI Product Frameworks Reference

Complete fill-in templates for building LLM/Agent-driven products. Organized by development lifecycle phase.

## Table of Contents

- [Phase 1: Architecture Design](#phase-1-architecture-design)
  - [Agent Design Canvas](#agent-design-canvas)
  - [Conversation State Machine](#conversation-state-machine)
- [Phase 2: Behavior Specification](#phase-2-behavior-specification)
  - [AI Feature Spec Sheet](#ai-feature-spec-sheet)
  - [Prompt Engineering Specification](#prompt-engineering-specification)
  - [Evaluation Rubric Design](#evaluation-rubric-design)
- [Phase 3: Risk & Cost](#phase-3-risk--cost)
  - [AI Failure Mode Taxonomy](#ai-failure-mode-taxonomy)
  - [AI Cost Control](#ai-cost-control)
- [Phase 4: Quality Verification](#phase-4-quality-verification)
  - [AI Quality Testing](#ai-quality-testing)

---

## Phase 1: Architecture Design

### Agent Design Canvas

**When to Use**: Your AI product has an LLM that needs to play multiple roles, handle multi-step reasoning, or produce structured outputs combining different concerns (e.g., conversation + analysis, generation + evaluation).

#### Template

**1. Role Decomposition**

```
[Product Name] Agent System
├── [Role 1] ([emoji])
│   └── Responsibility: [one sentence]
│   └── Triggered by: [when this role activates]
│   └── Output: [what it produces]
│
├── [Role 2] ([emoji])
│   └── Responsibility: [one sentence]
│   └── Triggered by: [when this role activates]
│   └── Output: [what it produces]
│
└── [Role N] ([emoji])
    └── Responsibility: [one sentence]
    └── Triggered by: [when this role activates]
    └── Output: [what it produces]
```

**2. Context Flow**

Define how information passes between roles:

```
[Role 1] ──output──→ [Role 2] ──output──→ [Role 3]
              │                     │
              └── shared context: [what's preserved across roles]
```

**3. Guidance Strategy Table**

| User State | Detection Method | Agent Behavior | Example Response |
|-----------|-----------------|---------------|-----------------|
| [State 1] | [How to detect] | [What agent does] | [Actual example] |
| [State 2] | [How to detect] | [What agent does] | [Actual example] |

**4. Output Schema**

```json
{
  "[role_1_output]": {
    "[field]": "[type] — [description]",
    "[field]": "[type] — [description]"
  },
  "[role_2_output]": {
    "[field]": "[type] — [description]"
  }
}
```

#### Example

A language learning app with dual-role AI (Conversation Partner + Expression Coach):

```
LangCoach Agent System
├── 🎭 Conversation Partner
│   └── Responsibility: Respond in-character as the scene role
│   └── Triggered by: Every user message
│   └── Output: Natural conversational reply
│
└── 🧠 Expression Coach
    └── Responsibility: Analyze user's language and suggest improvements
    └── Triggered by: Every user message (parallel to Partner)
    └── Output: Corrections, highlights, improved version
```

Both roles execute in a single LLM call, with output separated via JSON structure:
```json
{
  "reply": {"text": "...", "emotion": "friendly"},
  "feedback": {"corrections": [...], "highlights": [...]}
}
```

Guidance strategies:
| User State | Detection | Agent Behavior | Example |
|-----------|-----------|---------------|---------|
| Silent >10s | No input received | Offer rephrased question | "Would you like me to rephrase that?" |
| Too brief | Response < 5 words | Ask follow-up to expand | "Could you elaborate on that?" |
| Off-topic | Semantic drift detected | Gentle redirect | "Interesting. Going back to our discussion..." |
| Performing well | No corrections needed | Increase difficulty | Ask harder follow-up questions |

#### Tips

- **Resist the urge to create too many roles**. Start with 2-3. Each additional role increases prompt complexity and token cost.
- **Single-call multi-role is cheaper** than chaining multiple API calls. Design roles that can coexist in one prompt when possible.
- **Output schema is your contract** between PM and engineering. Define it early, iterate rarely.
- **Guidance strategies are a state machine** — think of them as if-then rules, not free-form instructions.

---

### Conversation State Machine

**When to Use**: Your product has a real-time AI interaction with distinct phases the user can perceive (recording, processing, responding, reviewing), and the UI needs to reflect these states.

#### Template

**State Diagram**:
```
[initial_state] → [state_2] → [state_3] → ... → [initial_state]
                                                        ↓
Special transitions: any → [paused], any → [ended]
```

**State Definition Table**:

| State | UI Display | Entry Condition | Exit Condition | User Actions Allowed |
|-------|-----------|----------------|---------------|---------------------|
| [state_1] | [What user sees] | [What triggers entry] | [What triggers exit] | [Buttons/actions available] |
| [state_2] | [What user sees] | [What triggers entry] | [What triggers exit] | [Buttons/actions available] |

**Transition Rules**:
- [state_1] → [state_2]: [Trigger event]
- [state_2] → [state_3]: [Trigger event]
- [any] → [paused]: [Trigger event]

#### Example

A voice-based AI tutor:

```
idle → user_recording → transcribing → ai_thinking → ai_speaking → feedback_shown → idle
                                                                          ↓
Special: any → paused, any → ended
```

| State | UI Display | Entry | Exit | User Actions |
|-------|-----------|-------|------|-------------|
| idle | Mic button pulsing | AI finishes / feedback dismissed | User taps mic | Tap mic, end session |
| user_recording | Waveform animation + timer | User taps mic | User taps stop | Stop recording |
| transcribing | "Recognizing..." spinner | Recording stops | Text returned | Cancel (→ idle) |
| ai_thinking | "Thinking..." animation | Transcript ready | LLM response ready | Cancel (→ idle) |
| ai_speaking | Audio playing + text | TTS starts | Audio ends | Interrupt (→ user_recording) |
| feedback_shown | Feedback card expanded | AI finishes speaking | User dismisses | Dismiss, save, next |

#### Tips

- **Every state must have a timeout fallback**. If `transcribing` takes >10s, auto-transition to an error recovery state.
- **"Interrupt" transitions are critical for conversational AI**. Users must be able to cut in while AI is speaking.
- **Map your state machine to CSS classes or component variants** early — it simplifies frontend implementation enormously.

---

## Phase 2: Behavior Specification

### AI Feature Spec Sheet

**When to Use**: Your product has 3+ distinct AI-powered features and you need PM ↔ engineering alignment on what each feature does, its constraints, and its technical requirements.

#### Template

| Feature | Agent Role | LLM Task | Input Constraints | Output Constraints | Technical Notes |
|---------|-----------|----------|-------------------|-------------------|----------------|
| [Feature name] | [Which agent role handles this] | [What the LLM does in plain language] | [Format, max size, required fields] | [JSON schema, field limits, required fields] | [Model choice, latency target, cost note] |

#### Example

| Feature | Agent Role | LLM Task | Input | Output | Notes |
|---------|-----------|----------|-------|--------|-------|
| Chat reply + feedback | Partner + Coach | Respond in-character AND analyze user expression | User text + history (≤20 turns) + scene context | strict JSON: reply{text, emotion} + feedback{corrections[], highlights[]} | Single LLM call; GPT-4o; stream first sentence for TTS overlap |
| Session report | Evaluator | Synthesize full conversation into 5-dimension assessment | All turns + all per-turn feedback | 5 scores + top_issues[] + highlights[] + recommendations[] | Separate call at session end; reference rubric in prompt |
| Material analysis | Analyst | Extract useful phrases and generate practice scenarios | Raw text (≤15K chars) + content_type hint | summary + key_phrases[] + terminology[] + suggested_scenes[] | Async; truncate with warning if >15K |

#### Tips

- **Input constraints prevent cost blowups**. Always define max token/character limits.
- **Output constraints prevent parsing failures**. Use `strict JSON mode` and define every field.
- **"Technical Notes" column is for engineering-critical info** that PM should know: which model, sync vs async, streaming behavior, etc.

---

### Prompt Engineering Specification

**When to Use**: Your product's core value depends on AI output quality, and prompts are a product deliverable (not just an engineering implementation detail).

#### Template

**1. Prompt Structure**

```
[System Role Definition]
  What character/identity the LLM assumes

[Dynamic Configuration]
  Variables injected at runtime:
  - {variable_1}: [description, source]
  - {variable_2}: [description, source]

[Behavior Rules]
  Numbered rules governing the LLM's behavior
  Organized by role if multi-role

[Few-Shot Examples]
  Domain-specific examples the LLM wouldn't know otherwise
  - Example 1: [input] → [expected output]
  - Example 2: [input] → [expected output]

[Output Schema]
  Strict JSON format specification

[Constraint Rules]
  Priority ordering, length limits, mandatory fields
```

**2. Output Control Table**

| Field | Type | Constraint | Rationale |
|-------|------|-----------|-----------|
| [field.path] | [string/int/enum/array] | [max length, enum values, min count] | [Why this constraint exists] |

**3. Priority Ordering**

When the LLM has multiple dimensions to evaluate, explicitly rank them:
```
① [Highest priority dimension] — [why it matters most]
② [Second priority] — [why]
③ [Third priority] — [why]
④ [Lowest priority] — [why it matters least]
```

#### Example

For an expression analysis coach:

Output control:
| Field | Type | Constraint | Rationale |
|-------|------|-----------|-----------|
| reply.text | string | 2-4 sentences, ≤500 chars | Longer replies break conversational rhythm |
| reply.emotion | enum | friendly\|neutral\|encouraging\|challenging | Controls TTS tone and UI emoji |
| feedback.corrections | array | max 3 items | >3 corrections overwhelms the learner |
| feedback.corrections[].type | enum | 6 predefined types | Enables frontend categorization and error pattern tracking |
| feedback.highlights | array | min 1 item | Guarantees positive reinforcement every turn |
| feedback.explanation_zh | string | Must be Chinese | Target users are Chinese speakers |

Priority ordering:
```
① Naturalness — is the expression native-sounding? (product differentiator)
② Coherence — does the response flow logically?
③ Appropriateness — does it match the scene's formality?
④ Variety — are different sentence structures used?
⑤ Grammar — only flag obvious errors (not a grammar checker)
```

#### Tips

- **Few-shot examples are your secret weapon**. LLMs don't reliably detect domain-specific patterns (e.g., Chinglish, medical jargon misuse) without explicit examples in the prompt.
- **Priority ordering prevents "grammar-only" feedback**. Without explicit ranking, LLMs default to the easiest analysis (grammar) and ignore harder ones (naturalness, register).
- **Output control is not optional**. LLMs are verbose by default. Without constraints, every response will be too long, have too many items, and include unwanted fields.
- **Version your prompts**. Track prompt changes in your version control — a prompt change is a product change.

---

### Evaluation Rubric Design

**When to Use**: Your AI assigns scores, makes quality judgments, or categorizes outputs, and you need consistent, reproducible results across sessions.

#### Template

**Scoring Rubric**:

| Dimension | Weight | 1-3 (Poor) | 4-6 (Acceptable) | 7-9 (Good) | 10 (Excellent) |
|-----------|--------|------------|-------------------|------------|----------------|
| [Dim 1] | [X%] | [Observable behaviors at this level] | [Observable behaviors] | [Observable behaviors] | [Observable behaviors] |
| [Dim 2] | [X%] | [Observable behaviors at this level] | [Observable behaviors] | [Observable behaviors] | [Observable behaviors] |

**Weighted Formula**:
```
overall_score = dim1 × weight1 + dim2 × weight2 + ... (weights must sum to 100%)
```

**Consistency Requirements**:
- Same input evaluated N times → scores within ±[X] points
- Different evaluators (prompt variants) → scores within ±[Y] points

#### Example

| Dimension | Weight | 1-3 | 4-6 | 7-9 | 10 |
|-----------|--------|-----|-----|-----|----|
| Expression naturalness | 30% | Frequent direct translations, unnatural phrasing | Some natural parts, some stilted | Mostly natural, occasional awkwardness | Indistinguishable from native speaker |
| Logical coherence | 25% | Disorganized, no transitions | Basic logic but stiff connections | Clear logic, smooth transitions | Rigorous, flowing argumentation |
| Scene appropriateness | 20% | Completely wrong register | Mostly appropriate, some mismatches | Matches scene requirements | Perfect register and politeness level |
| Sentence variety | 15% | Only simple sentences | Some variation but repetitive | Diverse structures | Rich, varied, purposeful structure choices |
| Grammar accuracy | 10% | Frequent errors affecting comprehension | Errors present but understandable | Occasional minor errors | Near-perfect |

Formula: `overall = naturalness×0.3 + coherence×0.25 + appropriateness×0.2 + variety×0.15 + grammar×0.1`

#### Tips

- **Anchor descriptions must be observable**, not subjective. "Good vocabulary" is vague; "Uses 3+ context-appropriate advanced words" is measurable.
- **Weight ordering = product values**. The highest-weighted dimension is your product's core differentiator.
- **Embed the rubric in the prompt**, not just in the PRD. The LLM needs to see the scale descriptions to score consistently.
- **Test consistency by evaluating the same conversation 3 times**. If variance > 1 point, your rubric descriptions are too ambiguous.

---

## Phase 3: Risk & Cost

### AI Failure Mode Taxonomy

**When to Use**: Your product calls external AI APIs (LLM, STT, TTS, vision, etc.) and you need to plan what happens when they fail, because they will.

#### Template

**Failure Classification**:

| Category | Detection Method | Soft Recovery | Partial Degradation | Hard Failure |
|----------|-----------------|--------------|--------------------|----|
| API Timeout | Response time > [X]s | Auto-retry 1× with backoff | Show cached/partial result | "Service temporarily unavailable" + retry button |
| Parse Error | JSON.parse throws | Extract raw text, omit structured data | Show primary output only, hide secondary | Log error, return plain text response |
| Rate Limit (429) | HTTP 429 status | Read Retry-After header, queue | Show "High traffic" message with progress | "Please try again in [X] minutes" |
| Auth/Permission | HTTP 401/403 | Refresh token, retry | Prompt user to re-authenticate | Guide to permission settings |
| Data Limit | Input > [X] tokens/chars | Auto-truncate, warn user | Process partial input | "Content too large, please reduce" |
| Data Quality | Empty/garbage output | Offer manual input alternative | Show raw output + edit interface | "Could not process, please try again" |

**Silent vs. Notify Decision Framework**:

| Condition | Action | Rationale |
|----------|--------|-----------|
| Noise input (e.g., <0.5s audio) | Silent ignore | Not a real user intent |
| Auto-retry succeeds | Silent | User doesn't need to know |
| Partial data returned | Show with indicator | User should know it's incomplete |
| Feature unavailable | Notify + alternative | User needs to take action |
| Quota exhausted | Notify + stats + reset time | User needs to plan |

#### Example

STT (Speech-to-Text) failure modes:

| Category | Detection | Recovery |
|----------|-----------|---------|
| Timeout >10s | Frontend timer | Show "Recognition timed out" + [Re-record] button |
| Empty result | API returns "" | "Didn't catch that, please try again" + [Re-record] |
| Low confidence result | Confidence < threshold | Show transcription + [Edit ✏️] icon for manual correction |
| API error 429/500 | HTTP status | Auto-retry 1× → fail → "Please use text input instead" |

#### Tips

- **"User Perception" column is the most important**. Engineers think about error codes; PMs must think about what the user *sees and feels*.
- **Silent ignore is valid for noise**. Not every anomaly deserves a UI response. Sub-0.5s audio clips, empty frames, accidental taps — filter at the edge.
- **Always preserve user work**. If the network drops mid-conversation, save pending content to localStorage. Never lose user input.
- **Quota messages should include 3 things**: what limit was hit, when it resets, and a summary of what was accomplished.

---

### AI Cost Control

**When to Use**: Your product uses pay-per-call AI APIs and you need to ensure costs don't spiral, especially during development and early scaling.

#### Template

**1. Per-API Cost Table**

| API Service | Provider | Pricing Model | Est. Cost per Unit | Volume Lever |
|------------|---------|--------------|-------------------|-------------|
| [Service 1] | [Provider] | [$/min, $/1K tokens, etc.] | ~$[X] | [What you can control: duration, token count, etc.] |
| [Service 2] | [Provider] | [$/min, $/1K tokens, etc.] | ~$[X] | [What you can control] |

**2. Cost per User Action**

| User Action | API Calls | Est. Cost | Control Strategy |
|------------|----------|-----------|-----------------|
| [Action 1] | [N × Service A + M × Service B] | ~$[X] | [How to limit: truncation, caching, limits] |

**3. Daily/Monthly Budget**

| Metric | Limit | Rationale |
|--------|------|-----------|
| [Actions] per user per day | [N] | Cost ceiling: $[X]/user/day |
| [Actions] per user per day | [N] | Cost ceiling: $[X]/user/day |
| Total daily budget (all users) | $[X] | Kill switch if exceeded |

**4. Cost Reduction Strategies**

| Strategy | Saves | Trade-off |
|----------|-------|-----------|
| Context window truncation | [X]% token cost | Loses early conversation history |
| Output length limits | [X]% token cost | Shorter AI responses |
| Model downgrade for simple tasks | [X]% per call | Slightly lower quality |
| Caching repeated queries | [X]% of duplicate calls | Stale results for dynamic content |
| Batch processing (async) | Queue management | Higher latency |

#### Example

| API | Pricing | Est. Cost | Control |
|-----|---------|-----------|---------|
| STT (Whisper) | $0.006/min | ~$0.006-0.012 | Limit recording to 2 min |
| LLM (GPT-4o) | $5/1M input + $15/1M output | ~$0.01-0.03/turn | Sliding window: keep last 20 turns only |
| TTS | $15/1M chars | ~$0.015/response | Limit AI reply to 2-4 sentences, ≤500 chars |

Full conversation (12 turns): ~$0.30-0.50. Daily limit: 20 conversations = max ~$10/user/day.

#### Tips

- **Estimate costs BEFORE building**. A feature that costs $0.50/use may be fine for 10 users but devastating at 1,000.
- **Sliding window truncation is the single most effective cost control** for conversational AI. Keep recent context, drop old turns.
- **Output length constraints serve double duty**: they reduce cost AND improve user experience (shorter = more readable).
- **Set a kill switch**. Define a daily budget ceiling. If API spend exceeds it, disable non-essential AI features rather than going bankrupt.

---

## Phase 4: Quality Verification

### AI Quality Testing

**When to Use**: You need to verify that AI outputs meet product standards before launch, and continuously monitor quality in production.

#### Template

**1. Test Dimensions**

| Dimension | Test Method | Sample Size | Acceptance Criteria |
|-----------|-----------|------------|-------------------|
| Output consistency | Same input × N runs, compare outputs | N = [X] | Scores within ±[X] variance; key fields match |
| Domain accuracy | Curated test set of known inputs → expected outputs | N = [X] | >[X]% correctly identified/classified |
| Role/character stability | Extended multi-turn conversation | [X] turns | No character breaks, consistent personality |
| Scoring consistency | Same conversation evaluated N times | N = [X] | Score variance < [X] points |
| Output quality | Human review of random sample | N = [X] | >[X]% rated "useful" or "correct" by reviewer |
| Latency | Measure P50/P95 response times | [X] requests | P95 < [X]ms |
| Hallucination rate | Fact-check outputs against known sources | N = [X] | <[X]% contain fabricated information |

**2. End-to-End Test Scenarios**

| Scenario | Steps | Verification |
|---------|-------|-------------|
| [Happy path] | [Step 1] → [Step 2] → ... → [Final step] | [What to check at the end] |
| [Edge case path] | [Step 1] → [Trigger edge case] → ... | [Verify graceful handling] |
| [Degradation path] | [Step 1] → [Simulate failure] → ... | [Verify fallback behavior] |

**3. Test Case Format**

| Field | Content |
|-------|---------|
| **Test ID** | TC-[XXX] |
| **Module** | [Module] > [Sub-module] |
| **Preconditions** | [Required state before test] |
| **Input** | [Exact input to provide] |
| **Steps** | 1. [Action] 2. [Action] 3. [Check] |
| **Expected Result** | [Specific, measurable expected output] |
| **Priority** | P0 (must pass) / P1 (should pass) / P2 (nice to have) |

#### Example

Test dimensions for a language learning AI:

| Dimension | Method | Sample | Criteria |
|-----------|--------|--------|---------|
| Chinglish detection | 50 known Chinglish sentences | 50 | >80% correctly flagged with fix |
| Feedback quality | Human review of corrections | 50 | >90% rated as reasonable improvement |
| Role consistency | 20-turn conversation | 3 sessions | Zero character breaks |
| Guidance triggers | Simulate silence, short answers, off-topic | 10 each | Correct guidance behavior triggered |
| Score consistency | Same 8-turn conversation × 3 evaluations | 5 conversations | All dimensions within ±1 point |

E2E scenarios:
1. **New user full journey**: Register → Setup → Pick scene → 8 turns → View report → View notes → Save phrase → Review next day
2. **Material-driven journey**: Import YouTube → Browse extracted phrases → Enter generated scene → Practice → Notes show material-related expressions
3. **Degradation**: STT timeout → Verify text input fallback activates → Continue conversation in text mode

#### Tips

- **AI testing is probabilistic, not deterministic**. You're testing distributions, not exact outputs. Use ranges and thresholds, not exact matches.
- **Human evaluation is irreplaceable for quality**. Automated metrics (BLEU, ROUGE) correlate poorly with user-perceived quality for conversational AI.
- **Test the guidance strategies explicitly**. Simulate every user state in your guidance table and verify the AI responds correctly.
- **Regression test your prompts**. When you change a prompt, re-run your test suite. A small wording change can dramatically shift output behavior.
- **Monitor in production**. Log AI outputs, sample randomly, and review weekly. Quality drifts over time as models update.
