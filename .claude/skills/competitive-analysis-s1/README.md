# Competitive Analysis S1 - Quick Start

This skill provides a comprehensive framework for conducting deep competitive analysis of AI products.

## What's Included

- **SKILL.md**: Complete methodology guide (315 lines)
- **references/**: Detailed templates and resource directories (888 lines)
- **assets/**: Prompt library for reverse engineering (422 lines)
- **scripts/**: Canvas generation tool (485 lines)

**Total**: 2,110 lines of battle-tested competitive analysis knowledge

## Quick Start

### 1. Invoke the Skill

When working with Claude Code, simply mention competitive analysis tasks:

```
"Help me analyze ChatGPT's new Canvas feature"
"I want to reverse-engineer how Claude structures its responses"
"Guide me through competitive research on Perplexity"
```

Claude will automatically use this skill to guide you through the 知行合一 framework.

### 2. Generate a Canvas Template

Use the included Python script to create structured analysis documents:

```bash
# Generate a product analysis canvas
python .claude/skills/competitive-analysis-s1/scripts/generate_canvas.py \
  --type product \
  --output analysis_chatgpt.md \
  --product-name "ChatGPT Canvas" \
  --analyst "Your Name"

# Generate a growth tracking canvas
python .claude/skills/competitive-analysis-s1/scripts/generate_canvas.py \
  --type growth \
  --output my_learning_tracker.md

# Generate a reverse engineering worksheet
python .claude/skills/competitive-analysis-s1/scripts/generate_canvas.py \
  --type reverse \
  --output reverse_perplexity.md
```

### 3. Use the Prompt Library

Access ready-to-use prompts for reverse engineering:

- See `assets/prompt-library.md` for 20+ proven prompts
- Categories: System Prompt Inference, Model Analysis, Architecture, Testing, Business Strategy

### 4. Follow the Framework

The skill guides you through three phases:

**Phase 1: Input (Building Knowledge)**
- Business & Strategy Layer (VCs, founders, enterprises)
- Technology & Frontier Layer (papers, products, tech blogs)
- Open Source & Engineering Layer (GitHub, frameworks)

**Phase 2: Process (Hands-On Investigation)**
- Multi-dimensional competitive analysis
- AI-assisted reverse engineering
- DIY low-code validation

**Phase 3: Output (Structured Insights)**
- Competitive product research canvas
- PM competency growth canvas
- Knowledge artifact accumulation

## Core Methodology

```
Input (输入) → Process (内化) → Output (输出)
    ↑                                    ↓
    └────────── Continuous Learning ──────┘
```

This is the "知行合一" (Knowledge-Action Unity) approach:
- **Input**: Build high-dimensional knowledge base
- **Process**: Learn by doing, not just reading
- **Output**: Create structured, reusable insights

## Key Differentiators

### What Makes This Framework Special

1. **AI PM Focused**: Designed specifically for product managers working on AI products
2. **Hands-On**: Emphasizes testing and experimentation, not just desk research
3. **Systematic**: Provides templates, scripts, and structured workflows
4. **Deep**: Goes beyond feature comparisons to understand technical decisions
5. **Growth-Oriented**: Tracks your learning and skill development

### When to Use This Skill

✅ **Use for**:
- Deep competitive analysis of AI products
- Reverse-engineering competitor capabilities
- Building product intelligence databases
- Learning about AI product design patterns
- Strategic product planning

❌ **Don't use for**:
- Quick feature checklists (this is for DEEP analysis)
- Non-AI product research
- Financial/legal analysis

## Example Usage

### Example 1: Quick Analysis

**You**: "I need to analyze Notion AI's writing assistant feature"

**Claude** (using this skill):
1. Guides you through information gathering (Phase 1)
2. Helps you test the product systematically (Phase 2)
3. Creates structured analysis canvas (Phase 3)
4. Provides reverse-engineering prompts
5. Tracks your learning via growth canvas

### Example 2: Reverse Engineering

**You**: "How can I figure out what system prompt Perplexity uses?"

**Claude** (using this skill):
1. Provides specific reverse-engineering prompts from the library
2. Guides you through test case design
3. Helps you analyze output patterns
4. Suggests validation experiments
5. Documents findings in structured format

### Example 3: Market Intelligence

**You**: "I want to build intelligence on the AI code assistant market"

**Claude** (using this skill):
1. Directs you to information sources (VCs, GitHub, etc.)
2. Helps you analyze multiple products (Copilot, Cursor, etc.)
3. Creates comparative analysis
4. Identifies market gaps and opportunities
5. Builds reusable knowledge base

## File Structure

```
competitive-analysis-s1/
├── SKILL.md                          # Main skill guide (read this first!)
├── README.md                         # This file
├── scripts/
│   └── generate_canvas.py           # Canvas generator tool
├── references/
│   ├── analysis-templates.md        # Detailed templates for all canvases
│   └── information-sources.md       # Curated list of info sources
└── assets/
    └── prompt-library.md            # 20+ reverse engineering prompts
```

## Learning Path

### Beginner (First Time Using)
1. Read SKILL.md Overview and Phase 1
2. Review information-sources.md
3. Generate your first canvas using the script
4. Try 1-2 prompts from prompt-library.md

### Intermediate (Regular Use)
1. Complete Phase 2 hands-on testing
2. Use all three canvas types
3. Build your personal prompt variations
4. Start accumulating knowledge artifacts

### Advanced (Expert Level)
1. Customize the framework for your domain
2. Build automation around canvas generation
3. Create organization-wide intelligence database
4. Train team members using this framework

## Tips for Success

### Do's ✅
- Provide concrete examples when asking for analysis
- Use the templates - they encode best practices
- Test products hands-on, don't just read docs
- Track your learning using the growth canvas
- Build knowledge artifacts over time

### Don'ts ❌
- Don't skip the hands-on testing (Phase 2)
- Don't accept AI analysis without validation
- Don't rush - deep analysis takes time
- Don't analyze in isolation - share with team
- Don't forget to document your confidence levels

## Contributing

This skill was created from real PM experience and mentor guidance. To improve it:

1. Use it for actual competitive analysis
2. Document what worked and what didn't
3. Add new prompts to the library
4. Share successful analysis examples
5. Contribute template improvements

## Version History

- **v1.0** (2026-01-24): Initial creation based on 知行合一 framework
  - Complete three-phase methodology
  - 20+ reverse engineering prompts
  - Canvas generation tool
  - Comprehensive templates and resources

## Credits

Based on the AI PM深度调研指南 (AI PM Deep Research Guide) methodology, incorporating:
- VC/founder/enterprise perspectives
- Technical frontier tracking
- Open-source engineering practices
- Systematic competitive analysis
- AI-assisted reverse engineering
- Continuous learning and growth

---

**Ready to start?**

Just ask Claude: "Help me analyze [PRODUCT NAME]" and let the skill guide you through systematic competitive analysis!
