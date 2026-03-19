# AI-Assisted Development: Enterprise Architecture & Mental Model

> A Chief Architect's Guide to Token-Optimized, Spec-Driven Development with Coding Agents

---

## Table of Contents
1. [The Mental Model](#the-mental-model)
2. [Architectural Layers](#architectural-layers)
3. [Token Economics](#token-economics)
4. [Spec-Driven Development Framework](#spec-driven-development-framework)
5. [Enterprise Patterns](#enterprise-patterns)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
7. [Implementation Roadmap](#implementation-roadmap)

---

## The Mental Model

### Core Principle: Context is Currency

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE TOKEN ECONOMY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   INPUTS (Cost)              PROCESSING            OUTPUTS      │
│   ─────────────              ──────────            ───────      │
│   • Specs                    • Reasoning           • Code       │
│   • Context                  • Planning            • Tests      │
│   • Codebase refs            • Generation          • Docs       │
│   • Instructions                                                │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  OPTIMIZE HERE: Minimize input while maximizing signal  │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key Insight**: Every token you send is money spent. But not all tokens are equal:
- **High-value tokens**: Precise specs, relevant code context, clear constraints
- **Low-value tokens**: Verbose docs, irrelevant code, redundant instructions

### The Three Laws of AI-Assisted Development

1. **Specificity > Volume**: A 50-line precise spec outperforms a 500-line vague document
2. **Structure > Prose**: Structured formats (schemas, templates) reduce ambiguity
3. **Relevance > Completeness**: Load only what's needed for the current task

---

## Architectural Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENTERPRISE AI STACK                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ LAYER 5: GOVERNANCE & OBSERVABILITY                         │   │
│  │ • Token usage dashboards    • Cost allocation               │   │
│  │ • Quality metrics           • Audit trails                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ LAYER 4: ORCHESTRATION                                      │   │
│  │ • Task routing              • Agent coordination            │   │
│  │ • Session management        • Fallback strategies           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ LAYER 3: CONTEXT MANAGEMENT                                 │   │
│  │ • Spec registry             • Codebase indexing (RAG)       │   │
│  │ • Semantic caching          • Context compression           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ LAYER 2: AGENT RUNTIME                                      │   │
│  │ • Claude Code / Cursor / Copilot                            │   │
│  │ • MCP integrations          • Tool permissions              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▲                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ LAYER 1: FOUNDATION                                         │   │
│  │ • LLM Provider (Anthropic/OpenAI/etc)                       │   │
│  │ • API Gateway               • Rate limiting                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Layer Details

#### Layer 1: Foundation
- **Model Selection**: Choose model tier based on task complexity
  - Simple refactoring → Haiku/GPT-4o-mini (cheap, fast)
  - Complex architecture → Opus/GPT-4 (expensive, thorough)
- **API Strategy**: Direct API vs cloud provider (Bedrock/Vertex/Foundry)

#### Layer 2: Agent Runtime
- **CLAUDE.md / AGENTS.md**: Repository-level instructions
- **MCP Integrations**: Connect to Jira, Slack, Google Drive, databases
- **Tool Permissions**: Restrict file access, command execution

#### Layer 3: Context Management (TOKEN OPTIMIZATION LIVES HERE)
- **Spec Registry**: Central store for validated specifications
- **RAG Pipeline**: Index codebase for semantic retrieval
- **Semantic Caching**: Cache responses for similar queries
- **Compression**: Summarize conversation history

#### Layer 4: Orchestration
- **Task Routing**: Route tasks to appropriate agents/models
- **Multi-Agent Coordination**: Prevent conflicting implementations
- **Session Management**: Fresh context per task

#### Layer 5: Governance
- **Token Dashboards**: Track usage by team/project/task-type
- **Quality Gates**: Automated code review before merge
- **Audit Trails**: Compliance and reproducibility

---

## Token Economics

### The Token Budget Framework

```
┌────────────────────────────────────────────────────────────────┐
│                   TOKEN BUDGET PER TASK                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  CONTEXT WINDOW (e.g., 200K tokens)                           │
│  ═══════════════════════════════════════════════════════════  │
│                                                                │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────────────┐ │
│  │   SYSTEM     │ │    SPEC      │ │   DYNAMIC CONTEXT      │ │
│  │   (~5-10%)   │ │   (~10-20%)  │ │   (~30-50%)            │ │
│  │              │ │              │ │                        │ │
│  │ • CLAUDE.md  │ │ • Task spec  │ │ • Retrieved code       │ │
│  │ • Base rules │ │ • Schema     │ │ • Conversation         │ │
│  │ • Persona    │ │ • Examples   │ │ • Tool results         │ │
│  └──────────────┘ └──────────────┘ └────────────────────────┘ │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              RESERVED FOR GENERATION (~30-40%)          │   │
│  │              (Output tokens)                            │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Cost Optimization Strategies

| Strategy | Token Reduction | Implementation Complexity |
|----------|-----------------|--------------------------|
| Modular AGENTS.md | 70% | Low |
| Semantic caching | 40-60% | Medium |
| Context compression | Up to 96% | Medium |
| Model tiering | 50-80% cost | Low |
| RAG vs full context | 60-80% | High |
| Session isolation | 30-50% | Low |

### The Compression Hierarchy

```
Level 0: Full Context (Baseline)
    │
    ▼ Compress
Level 1: Relevant Files Only (-50%)
    │
    ▼ Compress
Level 2: Relevant Functions/Classes (-70%)
    │
    ▼ Compress
Level 3: Summaries + Key Code (-85%)
    │
    ▼ Compress
Level 4: Semantic Index Lookup (-95%)
```

---

## Spec-Driven Development Framework

### When to Use Specs (Decision Tree)

```
                    ┌─────────────────────┐
                    │   New Task Arrives  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Can explain in one  │
                    │     sentence?       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │ YES            │                │ NO
              ▼                │                ▼
    ┌─────────────────┐        │      ┌─────────────────┐
    │  Skip the spec  │        │      │  2+ prompts to  │
    │  Direct prompt  │        │      │    explain?     │
    └─────────────────┘        │      └────────┬────────┘
                               │               │
                               │    ┌──────────┼──────────┐
                               │    │ YES                 │ NO
                               │    ▼                     ▼
                               │  ┌─────────────┐  ┌─────────────┐
                               │  │ WRITE SPEC  │  │ Light spec  │
                               │  │ Full SDD    │  │ or outline  │
                               │  └─────────────┘  └─────────────┘
```

### Spec Types by Task Complexity

| Task Type | Spec Level | Token Investment | Example |
|-----------|------------|------------------|---------|
| Bug fix (obvious) | None | 0 | "Fix typo in README" |
| Bug fix (complex) | Light | 200-500 | Root cause + fix approach |
| Feature (small) | Outline | 500-1000 | Inputs, outputs, constraints |
| Feature (medium) | Standard | 1000-3000 | Full SDD with schema |
| Feature (large) | Comprehensive | 3000-8000 | Multi-agent coordination |
| Architecture change | Living Doc | 5000+ | Evolving spec with phases |

### Spec Template (Token-Optimized)

```markdown
# [FEATURE_NAME]

## Goal
[1-2 sentences: What does success look like?]

## Schema
```typescript
interface Input { ... }
interface Output { ... }
```

## Constraints
- [ ] Must/Must not statements
- [ ] Performance requirements
- [ ] Security considerations

## Implementation Hints
- Key files: `src/foo.ts`, `lib/bar.ts`
- Pattern to follow: [reference existing code]
- Avoid: [anti-patterns specific to this codebase]

## Acceptance Criteria
- [ ] Testable statement 1
- [ ] Testable statement 2
```

**Why this works**: Structured format reduces ambiguity. Schema provides type safety. Hints reduce exploration tokens. Criteria enable verification.

---

## Enterprise Patterns

### Pattern 1: Hierarchical Context Loading

```
┌─────────────────────────────────────────────────────────────┐
│                 CONTEXT LOADING STRATEGY                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALWAYS LOADED (System-level)                              │
│  ├── Organization standards (500 tokens)                   │
│  ├── Security requirements (300 tokens)                    │
│  └── Code style guide (200 tokens)                         │
│                                                             │
│  LOADED PER-REPO (CLAUDE.md)                               │
│  ├── Architecture overview (500 tokens)                    │
│  ├── Key patterns (300 tokens)                             │
│  └── Testing requirements (200 tokens)                     │
│                                                             │
│  LOADED ON-DEMAND (RAG/Search)                             │
│  ├── Relevant source files                                 │
│  ├── Related tests                                         │
│  └── API documentation                                     │
│                                                             │
│  NEVER LOADED                                              │
│  ├── Unrelated modules                                     │
│  ├── Historical discussions                                │
│  └── Full dependency docs                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 2: Model Tiering

```
┌─────────────────────────────────────────────────────────────┐
│                    MODEL SELECTION MATRIX                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TASK COMPLEXITY        MODEL TIER         COST/1M TOKENS  │
│  ───────────────        ──────────         ──────────────  │
│                                                             │
│  Code generation        Haiku/Mini         $0.25-0.80      │
│  (boilerplate)                                              │
│                                                             │
│  Standard features      Sonnet/GPT-4o      $3-5            │
│  (most work)                                                │
│                                                             │
│  Architecture/          Opus/GPT-4         $15-75          │
│  Complex reasoning                                          │
│                                                             │
│  Code review/           Sonnet             $3-5            │
│  Explanation                                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 3: Session Isolation

```
BAD: Long-running session accumulating context
────────────────────────────────────────────
Session 1: [Task A context][Task B context][Task C context]...
           ─────────────────────────────────────────────────►
           Context grows, irrelevant info pollutes reasoning

GOOD: Fresh session per task
────────────────────────────────────────────
Session 1: [Task A context] → Complete → End
Session 2: [Task B context] → Complete → End
Session 3: [Task C context] → Complete → End
           Clean context, focused reasoning
```

### Pattern 4: Semantic Caching

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Query 1    │───►│  Vector Store   │◄───│   Query 2    │
│ "Add auth"   │    │                 │    │ "Implement   │
│              │    │  ┌───────────┐  │    │  login"      │
└──────────────┘    │  │ Cached    │  │    └──────────────┘
                    │  │ Response  │  │
      SIMILAR ──────┼─►│ for auth  │◄─┼────── SIMILAR
      (cosine>0.9)  │  │ features  │  │      (cosine>0.9)
                    │  └───────────┘  │
                    └─────────────────┘
                           │
                           ▼
                    Return cached response
                    (Zero new tokens!)
```

---

## Anti-Patterns to Avoid

### 1. The Monolithic AGENTS.md
```
BAD:  10,000+ line AGENTS.md loaded every request
GOOD: Modular files loaded based on task type

# Structure
.claude/
├── base.md           # Always loaded (minimal)
├── frontend.md       # Loaded for UI tasks
├── backend.md        # Loaded for API tasks
├── database.md       # Loaded for DB tasks
└── testing.md        # Loaded for test tasks
```

### 2. The "Dump Everything" Context
```
BAD:  "Here's our entire codebase documentation..."
GOOD: "Here's the specific function you'll modify: [code]"
```

### 3. The Vague Spec
```
BAD:  "Make the app faster"
GOOD: "Reduce API response time for /users endpoint from 800ms to <200ms
       by implementing Redis caching for user lookups"
```

### 4. The Endless Session
```
BAD:  One session for entire sprint
GOOD: New session per task, with focused context
```

### 5. The Kitchen Sink MCP
```
BAD:  20 MCP tools connected "just in case"
GOOD: 3-5 MCP tools relevant to current workflow
      (Tool definitions consume tokens!)
```

---

## Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- [ ] Establish CLAUDE.md standards across repositories
- [ ] Set up token usage monitoring/dashboards
- [ ] Define model tiering policy
- [ ] Create spec templates for common task types

### Phase 2: Context Optimization (Weeks 3-4)
- [ ] Implement modular agent configuration
- [ ] Set up codebase indexing (RAG pipeline)
- [ ] Configure semantic caching layer
- [ ] Establish session isolation practices

### Phase 3: Process Integration (Weeks 5-6)
- [ ] Integrate spec-driven workflow into sprint planning
- [ ] Train teams on spec writing
- [ ] Set up quality gates for AI-generated code
- [ ] Establish feedback loops for continuous improvement

### Phase 4: Scale & Govern (Weeks 7-8)
- [ ] Roll out to additional teams
- [ ] Implement cost allocation by team/project
- [ ] Set up audit trails for compliance
- [ ] Create runbooks for common scenarios

---

## Key Metrics to Track

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Tokens per task | Decreasing trend | Cost efficiency |
| First-attempt success rate | >70% | Spec quality |
| Rework rate | <20% | Spec completeness |
| Cost per feature | Baseline -30% | ROI |
| Developer satisfaction | >4/5 | Adoption |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│              TOKEN OPTIMIZATION CHEAT SHEET                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  DO:                          DON'T:                       │
│  ✓ Write precise specs        ✗ Dump entire docs          │
│  ✓ Use structured formats     ✗ Write prose requirements  │
│  ✓ Load context on-demand     ✗ Include "just in case"    │
│  ✓ Fresh session per task     ✗ Endless conversations     │
│  ✓ Tier models by complexity  ✗ Use Opus for everything   │
│  ✓ Cache similar queries      ✗ Recompute every time      │
│  ✓ Modular AGENTS.md          ✗ Monolithic instructions   │
│                                                             │
│  RULE OF THUMB:                                            │
│  "If it takes 2+ prompts to explain, write a spec"        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Sources

- [How to Write a Good Spec for AI Agents - O'Reilly](https://www.oreilly.com/radar/how-to-write-a-good-spec-for-ai-agents/)
- [AGENTS.md Token Optimization Guide 2026 - SmartScope](https://smartscope.blog/en/generative-ai/claude/agents-md-token-optimization-guide-2026/)
- [Spec-Driven Development with AI Coding Agents - Java Code Geeks](https://www.javacodegeeks.com/2026/03/spec-driven-developmentwith-ai-coding-agents-the-workflow-replacingprompt-and-pray.html)
- [Claude Code for Enterprise - Anthropic](https://claude.com/product/claude-code/enterprise)
- [Claude Code Best Practices - Anthropic Engineering](https://www.anthropic.com/engineering/claude-code-best-practices)
- [How Claude Code is Built - Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/how-claude-code-is-built)
- [LLM Context Management Guide - 16x Engineer](https://eval.16x.engineer/blog/llm-context-management-guide)
- [Context Window Management Strategies - GetMaxim](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- [Context Packing - Docker](https://www.docker.com/blog/context-packing-context-window/)
- [Spec-Driven Development - Thoughtworks](https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices)
