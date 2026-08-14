#!/usr/bin/env python3
"""
Competitive Analysis Canvas Generator

This script generates markdown templates for competitive analysis canvases.
Can be customized based on the type of analysis needed.

Usage:
    python generate_canvas.py --type [product|growth|reverse] --output <filename>

Examples:
    python generate_canvas.py --type product --output analysis_chatgpt.md
    python generate_canvas.py --type growth --output my_growth_tracker.md
    python generate_canvas.py --type reverse --output reverse_claude.md
"""

import argparse
from datetime import datetime
from pathlib import Path

PRODUCT_CANVAS_TEMPLATE = """# Competitive Product Analysis: {product_name}

**Analysis Date**: {date}
**Analyst**: {analyst}
**Analysis Purpose**: {purpose}

---

## Dimension 1: Scenario (Scene)

### Core Problem Being Solved
- [ ] Detection (识别): ___
- [ ] Prediction (预测): ___
- [ ] Generation (生成): ___
- [ ] Agent/Automation (驱动): ___

### Target Use Cases
1. ___
2. ___
3. ___

### Validation Method
- [ ] Tested core user path
- [ ] Interviewed users
- [ ] Reviewed case studies

### Findings
___

---

## Dimension 2: Model Architecture

### Underlying Model(s)
- Primary model: ___
- Model family: ___

### Model Strategy
- [ ] Single model
- [ ] Multiple specialized models
- [ ] Fine-tuned custom
- [ ] Third-party API

### Evidence
- Response latency: ___ seconds
- Quality patterns: ___

### Findings
___

---

## Dimension 3: Data Strategy

### Data Sources
- [ ] Public web data
- [ ] Licensed datasets
- [ ] User-generated content
- [ ] Proprietary data

### Data Moat
___

### Findings
___

---

## Dimension 4: UX

### Interaction Paradigm
- [ ] Linear chat
- [ ] Canvas/dual-pane
- [ ] Copilot
- [ ] Other: ___

### Latency Handling
- Response time: ___ seconds
- Streaming: [ ] Yes [ ] No

### UI Quality (1-10)
- Visual design: ___
- Information architecture: ___
- Micro-interactions: ___

### Findings
___

---

## Dimension 5: Cost Economics

### Pricing Model
- [ ] Freemium
- [ ] Subscription
- [ ] Pay-as-you-go

### Pricing Tiers
- Free: ___
- Pro: $___/month
- Team: $___/month

### Findings
___

---

## Strategic Summary

### Strengths
1. ___
2. ___
3. ___

### Weaknesses
1. ___
2. ___
3. ___

### Opportunities for Our Product
1. ___
2. ___
3. ___

### Threats/Risks
1. ___
2. ___
3. ___
"""

GROWTH_CANVAS_TEMPLATE = """# AI PM Competency Growth Canvas

**Project Name**: {project_name}
**Research Focus**: {focus}
**Time Period**: {date_start} to {date_end}

---

## Technical Literacy

### Pre-Mortem Goals
Concepts to build:
- [ ] RAG
- [ ] Agent workflows
- [ ] Fine-tuning
- [ ] Prompt engineering
- [ ] Other: ___

Questions:
1. ___
2. ___

### Actual Actions
1. ___
2. ___

Tools used: ___
Time invested: ___ hours

### Post-Mortem & Gaps
Knowledge gained: ___
Misconceptions corrected: ___
Skills needed: ___

**Rating (0-10)**: ___

---

## Product Sense

### Pre-Mortem Goals
Questions to validate:
- [ ] UX quality
- [ ] Pain point fit
- [ ] Value capture
- [ ] Other: ___

Hypotheses:
1. ___
2. ___

### Actual Actions
1. ___
2. ___

Time in product: ___ hours

### Post-Mortem & Gaps
Validated insights: ___
Surprises: ___
Intuitions to refine: ___

**Rating (0-10)**: ___

---

## Engineering Capability

### Pre-Mortem Goals
Challenges to experience:
- [ ] Read source code
- [ ] Reverse-engineer
- [ ] Build POC
- [ ] Other: ___

### Actual Actions
1. ___
2. ___

Repos examined: ___
Tools used: ___

### Post-Mortem & Gaps
Engineering insights: ___
Technical limitations: ___
Skills to learn: ___

**Rating (0-10)**: ___

---

## Business Insight

### Pre-Mortem Goals
Questions to validate:
- [ ] Unit economics
- [ ] GTM strategy
- [ ] Positioning
- [ ] Other: ___

### Actual Actions
1. ___
2. ___

Market research: ___
Pricing analysis: ___

### Post-Mortem & Gaps
Insights validated: ___
Surprises: ___
Market dynamics: ___

**Rating (0-10)**: ___

---

## Overall Reflection

**Most Valuable Learning**: ___

**Biggest Surprise**: ___

**Application to Work**: ___

**Next Focus**: ___

**Overall Rating (0-10)**: ___
"""

REVERSE_ENGINEERING_TEMPLATE = """# Reverse Engineering Analysis: {product_name}

**Analysis Date**: {date}
**Analysis Goal**: {goal}

---

## Part 1: System Prompt Inference

### Test Input
```
{test_input}
```

### Observed Output
```
{observed_output}
```

### Output Characteristics
- Structure: ___
- Tone: ___
- Format: ___

### Inferred System Prompt Elements

**Role definition**:
```
[Your hypothesis]
```

**Output requirements**:
```
[Your hypothesis]
```

**Constraints**:
```
[Your hypothesis]
```

### Validation Tests
- [ ] Test 1: ___
- [ ] Test 2: ___
- [ ] Test 3: ___

**Confidence Level**: ___ / 10

---

## Part 2: Model Capability Analysis

| Test Category | Input | Expected | Actual | Inference |
|---------------|-------|----------|--------|-----------|
| Context window | ___ | ___ | ___ | ___ |
| Multimodal | ___ | ___ | ___ | ___ |
| Reasoning | ___ | ___ | ___ | ___ |
| Speed | ___ | ___ | ___ | ___ |

### Model Hypothesis
- Base model: ___
- Size: ___
- Fine-tuning: ___
- Special capabilities: ___

---

## Part 3: Architecture Inference

### Data Flow
```
User Input → [?] → [?] → [?] → Output
```

### Component Hypotheses
1. Input processing: ___
2. Retrieval/RAG: ___
3. Model inference: ___
4. Output formatting: ___

### Evidence
- Timing patterns: ___
- Error messages: ___
- Network analysis: ___

---

## Part 4: Validation Experiments

### Experiment 1
- Hypothesis: ___
- Method: ___
- Result: ___
- Conclusion: ___

### Experiment 2
- Hypothesis: ___
- Method: ___
- Result: ___
- Conclusion: ___

---

## Summary

**Confidence (0-10)**: ___

**Key Discoveries**:
1. ___
2. ___

**Remaining Uncertainties**:
1. ___
2. ___

**Next Steps**:
1. ___
2. ___
"""


def generate_canvas(canvas_type, output_file, **kwargs):
    """Generate a canvas template file."""

    # Set defaults
    defaults = {
        'product_name': '[Product Name]',
        'analyst': '[Your Name]',
        'purpose': '[Analysis Purpose]',
        'project_name': '[Project Name]',
        'focus': '[Research Focus]',
        'goal': '[Analysis Goal]',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'date_start': datetime.now().strftime('%Y-%m-%d'),
        'date_end': '[End Date]',
        'test_input': '[Your test input]',
        'observed_output': '[Observed output]',
    }

    # Merge with provided kwargs
    template_vars = {**defaults, **kwargs}

    # Select template
    if canvas_type == 'product':
        template = PRODUCT_CANVAS_TEMPLATE
    elif canvas_type == 'growth':
        template = GROWTH_CANVAS_TEMPLATE
    elif canvas_type == 'reverse':
        template = REVERSE_ENGINEERING_TEMPLATE
    else:
        raise ValueError(f"Unknown canvas type: {canvas_type}")

    # Format template
    content = template.format(**template_vars)

    # Write to file
    output_path = Path(output_file)
    output_path.write_text(content)

    print(f"✅ Generated {canvas_type} canvas: {output_path}")
    print(f"   File size: {len(content)} bytes")
    print(f"\nNext steps:")
    print(f"   1. Open the file: {output_path}")
    print(f"   2. Fill in the analysis details")
    print(f"   3. Save and use for your competitive research")


def main():
    parser = argparse.ArgumentParser(
        description='Generate competitive analysis canvas templates'
    )
    parser.add_argument(
        '--type',
        required=True,
        choices=['product', 'growth', 'reverse'],
        help='Type of canvas to generate'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output filename (e.g., analysis_chatgpt.md)'
    )
    parser.add_argument(
        '--product-name',
        help='Product name for the analysis'
    )
    parser.add_argument(
        '--analyst',
        help='Your name'
    )

    args = parser.parse_args()

    # Build kwargs
    kwargs = {}
    if args.product_name:
        kwargs['product_name'] = args.product_name
    if args.analyst:
        kwargs['analyst'] = args.analyst

    # Generate canvas
    generate_canvas(args.type, args.output, **kwargs)


if __name__ == "__main__":
    main()
