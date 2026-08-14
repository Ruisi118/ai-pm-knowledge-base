# Product Requirements Document (PRD) Templates

## Standard PRD Template

### 1. Executive Summary
**Purpose**: One-page overview for executives and stakeholders

#### Components:
- **Problem Statement** (2-3 sentences)
- **Proposed Solution** (2-3 sentences)
- **Business Impact** (3 bullet points)
- **Timeline** (High-level milestones)
- **Resources Required** (Team size and budget)
- **Success Metrics** (3-5 KPIs)

### 2. Problem Definition

#### 2.1 Customer Problem
- **Who**: Target user persona(s)
- **What**: Specific problem or need
- **When**: Context and frequency
- **Where**: Environment and touchpoints
- **Why**: Root cause analysis
- **Impact**: Cost of not solving

#### 2.2 Market Opportunity
- **Market Size**: TAM, SAM, SOM
- **Growth Rate**: Annual growth percentage
- **Competition**: Current solutions and gaps
- **Timing**: Why now?

#### 2.3 Business Case
- **Revenue Potential**: Projected impact
- **Cost Savings**: Efficiency gains
- **Strategic Value**: Alignment with company goals
- **Risk Assessment**: What if we don't do this?

### 3. Solution Overview

#### 3.1 Proposed Solution
- **High-Level Description**: What we're building
- **Key Capabilities**: Core functionality
- **User Journey**: End-to-end flow
- **Differentiation**: Unique value proposition

#### 3.2 In Scope
- Feature 1: Description and priority
- Feature 2: Description and priority
- Feature 3: Description and priority

#### 3.3 Out of Scope
- Explicitly what we're NOT doing
- Future considerations
- Dependencies on other teams

#### 3.4 MVP Definition
- **Core Features**: Minimum viable feature set
- **Success Criteria**: Definition of "working"
- **Timeline**: MVP delivery date
- **Learning Goals**: What we want to validate

### 4. User Stories & Requirements

#### 4.1 User Stories
```
As a [persona]
I want to [action]
So that [outcome/benefit]

Acceptance Criteria:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

#### 4.2 Functional Requirements
| ID | Requirement | Priority | Notes |
|----|------------|----------|-------|
| FR1 | User can... | P0 | Critical for MVP |
| FR2 | System should... | P1 | Important |
| FR3 | Feature must... | P2 | Nice to have |

#### 4.3 Non-Functional Requirements
- **Performance**: Response times, throughput
- **Scalability**: User/data growth targets
- **Security**: Authentication, authorization, data protection
- **Reliability**: Uptime targets, error rates
- **Usability**: Accessibility standards, device support
- **Compliance**: Regulatory requirements

### 5. Design & User Experience

#### 5.1 Design Principles
- Principle 1: Description
- Principle 2: Description
- Principle 3: Description

#### 5.2 Wireframes/Mockups
- Link to Figma/Sketch files
- Key screens and flows
- Interaction patterns

#### 5.3 Information Architecture
- Navigation structure
- Data organization
- Content hierarchy

### 6. Technical Specifications

#### 6.1 Architecture Overview
- System architecture diagram
- Technology stack
- Integration points
- Data flow

#### 6.2 API Design
- Endpoints and methods
- Request/response formats
- Authentication approach
- Rate limiting

#### 6.3 Database Design
- Data model
- Key entities and relationships
- Migration strategy

#### 6.4 Security Considerations
- Authentication method
- Authorization model
- Data encryption
- PII handling

### 7. Go-to-Market Strategy

#### 7.1 Launch Plan
- **Soft Launch**: Beta users, timeline
- **Full Launch**: All users, timeline
- **Marketing**: Campaigns and channels
- **Support**: Documentation and training

#### 7.2 Pricing Strategy
- Pricing model
- Competitive analysis
- Value proposition

#### 7.3 Success Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Adoption Rate | X% | Daily Active Users |
| User Satisfaction | X/10 | NPS Score |
| Revenue Impact | $X | Monthly Recurring Revenue |
| Performance | <Xms | P95 Response Time |

### 8. Risks & Mitigations

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|-------------------|
| Technical debt | Medium | High | Allocate 20% for refactoring |
| User adoption | Low | High | Beta program with feedback loops |
| Scope creep | High | Medium | Weekly stakeholder reviews |

### 9. Timeline & Milestones

| Milestone | Date | Deliverables | Success Criteria |
|-----------|------|--------------|-----------------|
| Design Complete | Week 2 | Mockups, IA | Stakeholder approval |
| MVP Development | Week 6 | Core features | All P0s complete |
| Beta Launch | Week 8 | Limited release | 100 beta users |
| Full Launch | Week 12 | General availability | <1% error rate |

### 10. Team & Resources

#### 10.1 Team Structure
- **Product Manager**: [Name]
- **Engineering Lead**: [Name]
- **Design Lead**: [Name]
- **Engineers**: X FTEs
- **QA**: X FTEs

#### 10.2 Budget
- Development: $X
- Infrastructure: $X
- Marketing: $X
- Total: $X

### 11. Appendix
- User Research Data
- Competitive Analysis
- Technical Diagrams
- Legal/Compliance Docs

---

## Agile Epic Template

### Epic: [Epic Name]

#### Overview
**Epic ID**: EPIC-XXX
**Theme**: [Product Theme]
**Quarter**: QX 20XX
**Status**: Discovery | In Progress | Complete

#### Problem Statement
[2-3 sentences describing the problem]

#### Goals & Objectives
1. Objective 1
2. Objective 2
3. Objective 3

#### Success Metrics
- Metric 1: Target
- Metric 2: Target
- Metric 3: Target

#### User Stories
| Story ID | Title | Priority | Points | Status |
|----------|-------|----------|--------|--------|
| US-001 | As a... | P0 | 5 | To Do |
| US-002 | As a... | P1 | 3 | To Do |

#### Dependencies
- Dependency 1: Team/System
- Dependency 2: Team/System

#### Acceptance Criteria
- [ ] All P0 stories complete
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Documentation updated

---

## One-Page PRD Template

### [Feature Name] - One-Page PRD

**Date**: [Date]
**Author**: [PM Name]
**Status**: Draft | In Review | Approved

#### Problem
*What problem are we solving? For whom?*
[2-3 sentences]

#### Solution
*What are we building?*
[2-3 sentences]

#### Why Now?
*What's driving urgency?*
- Reason 1
- Reason 2
- Reason 3

#### Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| KPI 1 | X | Y |
| KPI 2 | X | Y |

#### Scope
**In**: Feature 1, Feature 2, Feature 3
**Out**: Feature A, Feature B

#### User Flow
```
Step 1 → Step 2 → Step 3 → Success!
```

#### Risks
1. Risk 1 → Mitigation
2. Risk 2 → Mitigation

#### Timeline
- Design: Week 1-2
- Development: Week 3-6
- Testing: Week 7
- Launch: Week 8

#### Resources
- Engineering: X developers
- Design: X designer
- QA: X tester

#### Open Questions
1. Question 1?
2. Question 2?

---

## Feature Brief Template (Lightweight)

### Feature: [Name]

#### Context
*Why are we considering this?*

#### Hypothesis
*We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We'll know we're right when [we see this metric]*

#### Proposed Solution
*High-level approach*

#### Effort Estimate
- **Size**: XS | S | M | L | XL
- **Confidence**: High | Medium | Low

#### Next Steps
1. [ ] User research
2. [ ] Design exploration
3. [ ] Technical spike
4. [ ] Stakeholder review

---

## AI Product PRD Template

For LLM/Agent-driven products. Extends the standard PRD with agent architecture, prompt specifications, failure mode planning, and AI quality standards.

### [Product Name] — AI Product PRD

**Date**: [Date]
**Author**: [PM Name]
**Status**: Draft | In Review | Approved
**Version**: [X.Y]

#### 1. Problem & Solution

##### 1.1 Problem Statement
*What problem are we solving? For whom? Why now?*
[2-3 paragraphs]

##### 1.2 Proposed Solution
*What are we building? How does AI enable the solution?*
[2-3 paragraphs]

##### 1.3 Target Users
*User personas with AI-relevant context (e.g., tech literacy, tolerance for AI errors)*

| Persona | Background | Core Pain Point | AI Expectation |
|---------|-----------|----------------|----------------|
| [Name] | [Background] | [Pain] | [What they expect from AI] |

##### 1.4 Success Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| [KPI 1] | [Target] | [How to measure] |

##### 1.5 Scope
**In**: [Features included]
**Out**: [Features explicitly excluded]

#### 2. User Personas & Journeys

##### 2.1 User Stories
```
As a [persona]
I want to [action involving AI]
So that [outcome/benefit]
```

##### 2.2 Key User Journeys
*Map the end-to-end flow including AI interactions*
```
[Step 1] → [Step 2] → [AI Processing] → [Step 3] → [Result]
```

##### 2.3 Moments that Matter
| Moment | User Feeling Goal | Design Implication |
|--------|------------------|-------------------|
| [Key moment] | [Target emotion] | [What to design for] |

#### 3. Agent Architecture

##### 3.1 Agent Role Definitions
```
[Product] Agent System
├── [Role 1 Name] ([emoji])
│   └── [One-line responsibility]
├── [Role 2 Name] ([emoji])
│   └── [One-line responsibility]
└── [Role N Name] ([emoji])
    └── [One-line responsibility]
```

##### 3.2 Agent Behavior Flow
```
User Input
    │
    ▼
┌─────────────────────────┐
│ Step 1: [Process Name]  │
│ • [What happens]        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Step 2: [Process Name]  │
│ • [What happens]        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Step N: Output Assembly  │
│ • [Final output format] │
└─────────────────────────┘
```

##### 3.3 Agent Guidance Strategies
| User State | Agent Behavior | Example |
|-----------|---------------|---------|
| [State 1: e.g., Silent >10s] | [Action] | [Example response] |
| [State 2: e.g., Off-topic] | [Action] | [Example response] |
| [State 3: e.g., Performing well] | [Action] | [Example response] |

##### 3.4 Agent Output Schema
```json
{
  "primary_output": {
    "field_1": "description",
    "field_2": "description"
  },
  "secondary_output": {
    "field_1": "description"
  }
}
```

##### 3.5 Conversation State Machine
```
States: [state_1] → [state_2] → [state_3] → ... → [state_1]
Special: any → [paused], any → [ended]
```

#### 4. AI Feature Specifications

| Feature | Agent Role | LLM Task | Input Constraints | Output Constraints | Technical Notes |
|---------|-----------|----------|-------------------|-------------------|----------------|
| [Feature 1] | [Role] | [Task description] | [Format, size limits] | [Schema, field constraints] | [Model, API, latency target] |
| [Feature 2] | [Role] | [Task description] | [Format, size limits] | [Schema, field constraints] | [Model, API, latency target] |

#### 5. Prompt Design

##### 5.1 Per-Agent Prompt Design

For each agent, document:

**[Agent Name] Prompt**

*Role*: [What role does this agent play?]

*Core Challenges*:
| Challenge | Description |
|----------|-------------|
| [Challenge 1] | [Why it's hard] |

*Design Strategies*:
- [Strategy 1]: [How it addresses the challenge]
- [Strategy 2]: [How it addresses the challenge]

*Prompt Template*:
```
[Full prompt text with {variable} placeholders]
```

##### 5.2 Output Control Table

| Field | Constraint | Rationale |
|-------|-----------|-----------|
| [field.name] | [type, length, enum values] | [Why this constraint] |

##### 5.3 Evaluation Rubric

| Dimension | Weight | 1-3 (Poor) | 4-6 (Acceptable) | 7-9 (Good) | 10 (Excellent) |
|-----------|--------|------------|-------------------|------------|----------------|
| [Dimension 1] | [X%] | [Description] | [Description] | [Description] | [Description] |

**Weighted Formula**: `overall = dim1 × w1 + dim2 × w2 + ...`

#### 6. Edge Cases & Degradation

Organize by product module. For each module:

##### 6.X [Module Name]

| Trigger Condition | User Perception | Handling Strategy |
|------------------|----------------|-------------------|
| [What goes wrong] | [What user sees/feels] | [Detection → Action → Fallback] |

**Degradation Layers**:
1. **Soft failure**: System auto-recovers (retry, fallback mode)
2. **Partial failure**: Reduced functionality (omit optional fields, text-only mode)
3. **Hard failure**: User-facing error with clear next steps

#### 7. Cost Model

##### 7.1 Per-API Cost Estimation

| API Service | Est. Cost per Call | Volume Control Strategy |
|------------|-------------------|------------------------|
| [STT Service] | ~$[X]/[unit] | [e.g., limit recording to 2min] |
| [LLM Service] | ~$[X]/call | [e.g., sliding window truncation] |
| [TTS Service] | ~$[X]/1K chars | [e.g., limit response to 2-4 sentences] |

##### 7.2 Per-User-Action Cost

| User Action | API Calls Involved | Est. Total Cost |
|------------|-------------------|----------------|
| [Action 1: e.g., Full conversation] | [STT×N + LLM×N + TTS×N] | ~$[X] |
| [Action 2: e.g., Material import] | [LLM×1] | ~$[X] |

##### 7.3 Daily Limits

| Resource | Daily Limit | Rationale |
|----------|------------|-----------|
| [Action 1] | [N] times/day | [Cost ceiling: $X/user/day] |

#### 8. AI Quality Standards

##### 8.1 AI-Specific Test Dimensions

| Test Dimension | Method | Acceptance Criteria |
|---------------|--------|-------------------|
| Output consistency | Same input × 3 runs | Scores within ±[X] variance |
| Domain accuracy | [N] test cases | >[X]% correctly identified |
| Role stability | [N]-turn conversation | No character breaks |
| Scoring consistency | Same conversation × 3 evaluations | < [X] point variance |
| Suggestion quality | Human review of [N] outputs | >[X]% rated as useful |

##### 8.2 End-to-End Test Scenarios

1. **[Scenario Name]**: [Step 1] → [Step 2] → ... → [Verify]
2. **[Scenario Name]**: [Step 1] → [Step 2] → ... → [Verify]

##### 8.3 Test Case Format

| Field | Content |
|-------|---------|
| **Test ID** | TC-XXX |
| **Module** | [Module > Sub-module] |
| **Preconditions** | [Setup required] |
| **Steps** | 1. [Action] 2. [Action] 3. [Verify] |
| **Expected Result** | [Detailed expected output] |
| **Priority** | P0 / P1 / P2 |

#### 9. Technical Implementation
*(Standard PRD sections: Tech Stack, API Routes, Data Model)*

#### 10. Timeline & Milestones

| Milestone | Date | Deliverables | Success Criteria |
|-----------|------|-------------|-----------------|
| [Phase 1] | [Date] | [What's delivered] | [How to verify] |
