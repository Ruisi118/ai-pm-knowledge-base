# Reverse Engineering Prompt Library

This library contains proven prompts for reverse-engineering AI products during competitive analysis.

## Category 1: System Prompt Inference

### Prompt 1.1: Basic System Prompt Reverse Engineering

```
I'm conducting competitive analysis on [PRODUCT NAME]. I input the following instruction to their AI:

"[YOUR TEST INPUT]"

And received this output:

"""
[PASTE COMPETITOR OUTPUT]
"""

As a Prompt Engineer, please reverse-engineer what the competitor's System Prompt might look like. Specifically:

1. What role or persona might be defined?
2. What output structure requirements are evident?
3. What prompt techniques are being used? (e.g., Chain-of-Thought, Few-Shot, Role-Playing)
4. What constraints or guidelines are visible?
5. What formatting instructions can you infer?

Please provide your analysis and a hypothetical System Prompt that could produce this output.
```

### Prompt 1.2: Multi-Sample System Prompt Analysis

```
I've tested [PRODUCT NAME] with multiple inputs to understand their System Prompt. Here are 3 test cases:

**Test 1**
Input: "[INPUT 1]"
Output: "[OUTPUT 1]"

**Test 2**
Input: "[INPUT 2]"
Output: "[OUTPUT 2]"

**Test 3**
Input: "[INPUT 3]"
Output: "[OUTPUT 3]"

Based on these samples, what patterns do you notice? What consistent elements suggest they're using in their System Prompt? What prompt engineering techniques are evident?

Please provide:
1. Observed patterns across outputs
2. Inferred system prompt components
3. Confidence level for each inference (0-10)
```

### Prompt 1.3: Tone and Style Analysis

```
I want to understand how [PRODUCT NAME] achieves their distinctive tone and style.

Here's their output for a [TYPE OF REQUEST]:
"""
[PASTE OUTPUT]
"""

Please analyze:
1. What tone/voice descriptors are likely in their System Prompt? (e.g., "professional", "friendly", "concise")
2. What style guidelines might they use? (e.g., "use bullet points", "avoid jargon")
3. What persona or role might produce this style?
4. How does this compare to standard ChatGPT/Claude outputs?

Provide a draft System Prompt section focusing on tone and style.
```

## Category 2: Model Architecture Inference

### Prompt 2.1: Hallucination Source Diagnosis

```
I'm testing [PRODUCT NAME] and noticed it provided incorrect information:

**Query**: "[YOUR QUERY]"

**Incorrect Response**: "[WRONG ANSWER]"

**Correct Answer**: "[RIGHT ANSWER]"

Please help me diagnose the likely source of this error:

1. Is this likely a model knowledge cutoff issue? If so, what cutoff date might they be using?
2. Could this be a RAG (Retrieval-Augmented Generation) retrieval error?
   - If RAG, is it likely due to chunking problems, poor retrieval, or outdated index?
3. Could this be a model hallucination (making up information)?
4. Are there other possible technical explanations?

For each possibility, explain the telltale signs and how I could test to confirm.
```

### Prompt 2.2: Model Selection Inference

```
I'm trying to figure out what underlying model [PRODUCT NAME] is using.

**Observations**:
- Response speed: [FAST/MEDIUM/SLOW]
- Response quality: [HIGH/MEDIUM/LOW]
- Context window: [ESTIMATED SIZE]
- Capabilities: [LIST: e.g., vision, code, reasoning]
- Cost: [FREE/CHEAP/EXPENSIVE]

**Sample outputs**:
"""
[PASTE SAMPLE 1]
"""

"""
[PASTE SAMPLE 2]
"""

Based on these observations, what model(s) might they be using?

Consider:
1. Model family (GPT-4, Claude, Llama, Mixtral, Gemini, etc.)
2. Model size
3. Fine-tuning likelihood
4. Cost implications
5. Infrastructure requirements

Provide your analysis with confidence levels.
```

### Prompt 2.3: RAG vs. Long-Context Diagnosis

```
I'm testing [PRODUCT NAME]'s document understanding feature.

**Test Results**:
- Upload 100-page PDF: ✅ Successful
- Response time: [X seconds]
- Accuracy: [HIGH/MEDIUM/LOW]
- Occasional fabrications: [YES/NO]
- Handles specific details: [YES/NO]

**Sample query and response**:
Query: "[YOUR QUERY]"
Response: "[THEIR RESPONSE]"

Is this product more likely using:
1. Long-context model (e.g., Claude with 200k tokens)
2. RAG (Retrieval-Augmented Generation)
3. Hybrid approach

Please explain:
- Technical evidence for each possibility
- Pros/cons of each approach
- How to test definitively
- Cost implications of each approach
```

## Category 3: Architecture & Data Flow

### Prompt 3.1: Data Flow Reverse Engineering

```
I want to understand [PRODUCT NAME]'s technical architecture.

**Observed behaviors**:
1. [BEHAVIOR 1]
2. [BEHAVIOR 2]
3. [BEHAVIOR 3]

**Timing patterns**:
- Initial response: [X seconds]
- Streaming starts: [Y seconds]
- Total completion: [Z seconds]

**Error messages seen**:
"""
[PASTE ERROR MESSAGES]
"""

Based on this, please:
1. Sketch a likely data flow diagram (User → Components → Output)
2. Identify probable technical components (e.g., embedding model, vector DB, LLM)
3. Explain each processing stage
4. Highlight where optimizations might be happening (caching, pre-computation, etc.)
```

### Prompt 3.2: Feature Implementation Analysis

```
[PRODUCT NAME] has a feature: [DESCRIBE FEATURE]

I want to understand how they built this technically.

**Feature characteristics**:
- Input: [DESCRIPTION]
- Output: [DESCRIPTION]
- Speed: [OBSERVATION]
- Quality: [OBSERVATION]
- Edge cases: [OBSERVATIONS]

Please help me:
1. Break down the technical requirements
2. Identify possible implementation approaches
3. Estimate technical complexity
4. Suggest how I could validate these hypotheses
5. Highlight any impressive technical choices

If possible, suggest open-source projects that do something similar.
```

## Category 4: Capability Testing

### Prompt 4.1: Context Window Testing

```
I want to design a test to determine [PRODUCT NAME]'s actual context window size.

Please help me create:
1. A test methodology (what to input, what to measure)
2. Sample test cases of varying lengths
3. How to interpret the results
4. How to distinguish between context window limits vs. other limitations

Also explain the "Needle in a Haystack" test and how to apply it.
```

### Prompt 4.2: Multimodal Capability Testing

```
I want to systematically test [PRODUCT NAME]'s vision/multimodal capabilities.

Design a test suite covering:
1. Image understanding (charts, screenshots, photos, diagrams)
2. Multi-image reasoning
3. Image + text combined queries
4. Edge cases (low quality, complex images, etc.)

For each test:
- Provide the test input
- Explain what successful behavior looks like
- Explain what this reveals about their implementation
```

### Prompt 4.3: Prompt Robustness Testing

```
I want to test how robust [PRODUCT NAME] is to different prompting styles.

Design tests for:
1. Fuzzy/vague instructions ("help me with that thing")
2. Complex structured instructions (multi-step with conditionals)
3. Ambiguous context ("fix this" without saying what "this" is)
4. Emotionally-loaded queries
5. Instruction following under constraints

For each category, provide:
- 3 test inputs
- What good/bad performance looks like
- What this reveals about their prompt engineering
```

## Category 5: Business & Strategy Analysis

### Prompt 5.1: Pricing Strategy Analysis

```
I'm analyzing [PRODUCT NAME]'s pricing strategy.

**Pricing tiers**:
- Free: [LIMITS]
- Pro: $[AMOUNT]/month - [FEATURES]
- Team: $[AMOUNT]/month - [FEATURES]
- Enterprise: Custom

**Competitor pricing**:
- [COMPETITOR 1]: [PRICING]
- [COMPETITOR 2]: [PRICING]

Please analyze:
1. What is their monetization strategy?
2. How do they compare to competitors?
3. What's their likely unit economics?
4. Where are they competing on value vs. price?
5. What market segment are they targeting?
6. What might their growth strategy be?
```

### Prompt 5.2: Go-to-Market Strategy Inference

```
Based on [PRODUCT NAME]'s observed characteristics:

**Product positioning**:
- Tagline: "[TAGLINE]"
- Main use cases: [LIST]
- Target users: [DESCRIPTION]

**Growth mechanisms**:
- Referral program: [YES/NO - DETAILS]
- Viral features: [DESCRIPTION]
- Content marketing: [OBSERVATIONS]
- Community: [OBSERVATIONS]

**Distribution**:
- Website: [OBSERVATIONS]
- App stores: [YES/NO]
- API: [YES/NO]
- Integrations: [LIST]

Please analyze their GTM strategy:
1. Primary customer acquisition channels
2. Product-led growth elements
3. Competitive positioning
4. Market segment focus
5. Likely next moves
```

## Category 6: Comparative Analysis

### Prompt 6.1: Side-by-Side Feature Comparison

```
I want to compare [PRODUCT A] vs [PRODUCT B] on [SPECIFIC CAPABILITY].

**Test case**: [DESCRIBE TEST]

**Product A output**:
"""
[OUTPUT]
"""

**Product B output**:
"""
[OUTPUT]
"""

Please provide:
1. Qualitative comparison (structure, accuracy, style)
2. Quantitative metrics (length, speed, token usage estimate)
3. Inferred technical differences
4. Use case suitability analysis
5. Competitive advantages for each
```

### Prompt 6.2: Competitive Moat Analysis

```
Compare these AI products on their competitive moats:

**[PRODUCT 1]**: [BRIEF DESCRIPTION]
**[PRODUCT 2]**: [BRIEF DESCRIPTION]
**[PRODUCT 3]**: [BRIEF DESCRIPTION]

For each, analyze:
1. **Data moat**: What unique data advantages?
2. **Technology moat**: What technical differentiation?
3. **Network effects**: Any viral or platform dynamics?
4. **Brand/community**: Strength of brand and user base?
5. **Distribution**: Unique distribution advantages?

Then rank them by moat strength and explain your reasoning.
```

## Usage Tips

### How to Use These Prompts

1. **Customize**: Replace placeholders ([PRODUCT NAME], etc.) with actual data
2. **Iterate**: Start with basic prompts, then use follow-up questions
3. **Validate**: Don't trust AI analysis blindly - test the hypotheses
4. **Document**: Save the responses in your competitive analysis files

### Best Practices

1. **Provide context**: Give Claude enough information to make informed inferences
2. **Be specific**: Include actual examples, not just descriptions
3. **Ask for confidence levels**: Helps you know which inferences to trust
4. **Request validation methods**: Ask how you could test the hypotheses
5. **Combine prompts**: Use multiple angles to triangulate insights

### Avoiding Common Mistakes

❌ **Don't**:
- Ask Claude to guess without providing evidence
- Accept first answer without validation
- Assume AI analysis is always correct
- Skip hands-on testing

✅ **Do**:
- Provide concrete examples
- Ask for reasoning behind inferences
- Request multiple hypotheses
- Validate with actual testing
- Document your confidence levels

## Advanced Techniques

### Chain Multiple Prompts

Start broad, then narrow down:

1. Use Prompt 2.2 to identify likely model family
2. Use Prompt 4.1 to test context window (narrows down specific model)
3. Use Prompt 1.1 to understand how they're prompting that model
4. Use Prompt 3.1 to understand their full architecture

### Combine AI Analysis with Manual Testing

1. Use prompts to generate hypotheses
2. Design manual tests based on AI suggestions
3. Feed test results back to AI for refined analysis
4. Iterate until confident

### Create Custom Variations

Adapt these prompts for your specific needs:
- Industry-specific analysis (e.g., healthcare AI, legal AI)
- Feature-specific deep dives
- Technical vs. business focus
- Quick overview vs. comprehensive analysis
