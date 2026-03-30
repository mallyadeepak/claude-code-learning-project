# Multi-Agent Design Runbook

> A practical guide to orchestrating multiple Claude agents for maximum engineering productivity — covering patterns, best practices, and real-world examples.

---

## Table of Contents

1. [Why Multi-Agent?](#1-why-multi-agent)
2. [Mental Model](#2-mental-model)
3. [Core Patterns](#3-core-patterns)
4. [Claude Code: Agent Tool](#4-claude-code-agent-tool)
5. [Claude API: Programmatic Orchestration](#5-claude-api-programmatic-orchestration)
6. [Best Practices](#6-best-practices)
7. [Anti-Patterns](#7-anti-patterns)
8. [Organization Playbook](#8-organization-playbook)

---

## 1. Why Multi-Agent?

A single Claude agent is powerful. Multiple agents working in concert are transformative. The gains come from four sources:

| Gain | Why It Matters |
|------|---------------|
| **Parallelism** | Independent tasks run simultaneously instead of sequentially — 3 agents working in parallel can cut wall-clock time by ~3× |
| **Specialization** | Each agent gets a focused prompt optimized for its task — a security reviewer thinks differently than a code generator |
| **Context isolation** | Each agent has its own context window — complex tasks no longer hit token limits |
| **Independent verification** | One agent writes, another reviews — catches errors the first agent would never catch about its own output |

### When to go multi-agent

- The task can be naturally decomposed into independent subtasks
- You need more than one "perspective" (generator + reviewer)
- A single task would consume most of the context window
- You want to run work on multiple files/services/repos in parallel
- You need a human-in-the-loop checkpoint between phases

---

## 2. Mental Model

Think of agents like engineers on a team:

```
┌─────────────────────────────────────────────────────────┐
│                     Orchestrator                        │
│         (decomposes work, delegates, integrates)        │
└──────────────┬──────────────┬──────────────┬────────────┘
               │              │              │
        ┌──────▼───┐   ┌──────▼───┐   ┌─────▼────┐
        │ Agent A  │   │ Agent B  │   │ Agent C  │
        │ (Explore)│   │  (Plan)  │   │ (Write)  │
        └──────────┘   └──────────┘   └──────────┘
```

The orchestrator is the tech lead: it knows the goal, breaks it into parts, hands work off, and combines the results. Worker agents are specialists: they do one thing well and report back.

**Key rule:** agents should be as independent as possible. If Agent B needs Agent A's output to start, run them sequentially. If they don't, run them in parallel.

---

## 3. Core Patterns

### Pattern 1: Fan-Out / Fan-In (Parallel Research)

Use when you need to gather information from multiple independent sources simultaneously.

```
         Orchestrator
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
Agent A    Agent B    Agent C      ← run in parallel
(search    (read      (read
 docs)     file 1)   file 2)
    │         │         │
    └─────────┼─────────┘
              ▼
        Orchestrator
        (synthesizes results)
```

**Example use cases:**
- Researching three different APIs simultaneously
- Running linting, tests, and security scans in parallel
- Analyzing multiple microservices for a cross-cutting change

---

### Pattern 2: Pipeline (Sequential Specialization)

Use when each stage depends on the previous stage's output.

```
Explore Agent → Plan Agent → Implementation Agent → Review Agent
   (research)    (design)       (write code)         (verify)
```

Each agent receives the previous agent's output as context, adding value at each stage. The handoff is structured — the orchestrator passes only the relevant summary forward, not the full context chain.

**Example use cases:**
- Research → design → implement → test → document
- Scan codebase → identify issues → fix issues → verify fixes

---

### Pattern 3: Generator + Critic

Use when quality matters more than speed. One agent produces output, another agent reviews it independently.

```
Generator Agent ──────► output ──────► Critic Agent
      ▲                                     │
      │                                     │
      └──── revised output ◄── feedback ────┘
                (if needed)
```

The critic should be given a different prompt and persona than the generator. "You are a senior security engineer reviewing this code for vulnerabilities" produces better critique than "review what you just wrote."

**Example use cases:**
- Write code → security review
- Draft PR description → check for accuracy
- Generate tests → verify tests actually cover edge cases

---

### Pattern 4: Map-Reduce over Files

Use when you need to process many files and aggregate results.

```
         Orchestrator
              │
    ┌────┬───┴───┬────┐
    ▼    ▼       ▼    ▼
  f1   f2  ...  fN-1  fN    ← one agent per file (or batch)
    │    │       │    │
    └────┴───┬───┴────┘
             ▼
       Orchestrator
       (aggregates, deduplicates, summarizes)
```

**Example use cases:**
- Add docstrings to every file in a module
- Run a security audit across all services
- Extract API surface from a large codebase

---

### Pattern 5: Supervisor with Retry

Use when a task might fail or produce low-quality output. A supervisor agent checks the result and re-dispatches if needed.

```
Orchestrator
     │
     ▼
Worker Agent ──► output ──► Supervisor Agent
                                   │
                          ┌────────┴────────┐
                          ▼                 ▼
                       PASS              FAIL
                          │                 │
                          ▼                 ▼
                    return result    retry with feedback
```

**Example use cases:**
- Code generation that must pass tests before being accepted
- Output that must meet a schema/format requirement
- Agent that calls an unreliable external API

---

## 4. Claude Code: Agent Tool

### Launching agents

```python
# Foreground — you need the result before proceeding
Agent(
    subagent_type="Explore",
    description="Find all API endpoints",
    prompt="Search the codebase for all HTTP route definitions..."
)

# Background — fire and forget, continue other work
Agent(
    subagent_type="general-purpose",
    description="Run test suite",
    prompt="Run pytest and return the full output...",
    run_in_background=True
)
```

### Parallel agents (single message, multiple tool calls)

The most important performance optimization: send **multiple Agent tool calls in one message** when the tasks are independent.

```
Message with two Agent calls:
├── Agent(Explore, "Find all database models")     ← starts simultaneously
└── Agent(Explore, "Find all API endpoints")       ← starts simultaneously
```

Do NOT do this:
```
Message 1: Agent(Explore, "Find all database models")
Wait for result...
Message 2: Agent(Explore, "Find all API endpoints")   ← sequential, slower
```

### Worktree isolation

For agents that write code, use `isolation: "worktree"` to give each agent its own git branch. Prevents agents from interfering with each other's file edits.

```python
Agent(
    subagent_type="general-purpose",
    description="Refactor auth module",
    prompt="Refactor src/auth.py to use the new token format...",
    isolation="worktree"   # agent works on a copy of the repo
)
```

### Continuing an agent

Agents can be resumed with `SendMessage` using the agent ID returned in the result. Useful for multi-turn workflows:

```
Agent launched → returns agentId: "abc123"
                      │
                      ▼
SendMessage(to: "abc123", "Now run the tests against what you just wrote")
```

### Choosing the right subagent type

| Task | Best subagent type |
|------|--------------------|
| Find files, search code, answer "where is X" | `Explore` |
| Design an implementation plan before writing | `Plan` |
| Explain how a codebase works | `codebase-explainer` |
| Write/edit code, run commands, multi-step tasks | `general-purpose` |
| Answer questions about Claude Code / API | `claude-code-guide` |

---

## 5. Claude API: Programmatic Orchestration

For building autonomous pipelines outside Claude Code, use the Anthropic SDK directly.

### Basic orchestrator pattern

```python
import anthropic

client = anthropic.Anthropic()

def run_agent(system_prompt: str, user_message: str, tools: list = None) -> str:
    """Run a single agent turn and return the text response."""
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
        tools=tools or [],
    )
    return response.content[0].text


def orchestrate_code_review(pr_diff: str) -> dict:
    """
    Three-agent pipeline: summarize → security review → style review.
    Security and style run in parallel after the summary.
    """
    # Stage 1: summarize the diff
    summary = run_agent(
        system_prompt="You are a senior engineer. Summarize this PR diff concisely.",
        user_message=pr_diff,
    )

    # Stage 2a + 2b: run in parallel using threads
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor() as executor:
        security_future = executor.submit(
            run_agent,
            system_prompt="You are a security engineer. Review this code for vulnerabilities. Be specific.",
            user_message=f"Summary:\n{summary}\n\nFull diff:\n{pr_diff}",
        )
        style_future = executor.submit(
            run_agent,
            system_prompt="You are a senior Python engineer. Review this code for style and maintainability.",
            user_message=f"Summary:\n{summary}\n\nFull diff:\n{pr_diff}",
        )

        security_review = security_future.result()
        style_review = style_future.result()

    # Stage 3: synthesize into final verdict
    verdict = run_agent(
        system_prompt="You are a tech lead. Given security and style feedback, give a final go/no-go recommendation.",
        user_message=f"Security review:\n{security_review}\n\nStyle review:\n{style_review}",
    )

    return {
        "summary": summary,
        "security": security_review,
        "style": style_review,
        "verdict": verdict,
    }
```

### Tool use for agent-to-agent communication

Agents can call other agents as tools. This is the most composable pattern:

```python
import anthropic
import json

client = anthropic.Anthropic()

# Define sub-agents as tools the orchestrator can call
TOOLS = [
    {
        "name": "run_security_scan",
        "description": "Runs a security review on a code snippet. Returns findings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The code to review"},
                "language": {"type": "string", "description": "Programming language"},
            },
            "required": ["code", "language"],
        },
    },
    {
        "name": "run_test_generator",
        "description": "Generates pytest tests for a given function.",
        "input_schema": {
            "type": "object",
            "properties": {
                "function_code": {"type": "string"},
                "function_name": {"type": "string"},
            },
            "required": ["function_code", "function_name"],
        },
    },
]


def handle_tool_call(tool_name: str, tool_input: dict) -> str:
    """Route tool calls to the appropriate sub-agent."""
    if tool_name == "run_security_scan":
        return run_agent(
            system_prompt="You are a security engineer. List vulnerabilities in JSON format: [{issue, severity, line}]",
            user_message=f"Language: {tool_input['language']}\n\n{tool_input['code']}",
        )
    elif tool_name == "run_test_generator":
        return run_agent(
            system_prompt="You are a Python test engineer. Write pytest tests. Return only the test code.",
            user_message=f"Function:\n{tool_input['function_code']}",
        )
    return "Unknown tool"


def run_orchestrator(task: str) -> str:
    """
    Agentic loop: orchestrator decides which tools (sub-agents) to call,
    processes results, and continues until it has a final answer.
    """
    messages = [{"role": "user", "content": task}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            system="You are an engineering orchestrator. Use your tools to complete tasks thoroughly.",
            messages=messages,
            tools=TOOLS,
        )

        # If no tool calls, we have a final answer
        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Process all tool calls in this turn
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = handle_tool_call(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Feed results back and continue the loop
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

### Async orchestration for high throughput

```python
import asyncio
import anthropic

client = anthropic.AsyncAnthropic()

async def run_agent_async(system_prompt: str, user_message: str) -> str:
    response = await client.messages.create(
        model="claude-sonnet-4-6",   # use Sonnet for worker agents, Opus for orchestrator
        max_tokens=2048,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


async def process_files_in_parallel(files: list[tuple[str, str]]) -> list[dict]:
    """
    Map-reduce: run one agent per file in parallel, then aggregate.
    files: list of (filename, content) tuples
    """
    tasks = [
        run_agent_async(
            system_prompt="Extract all function signatures as JSON: [{name, params, return_type}]",
            user_message=f"File: {fname}\n\n{content}",
        )
        for fname, content in files
    ]

    results = await asyncio.gather(*tasks)

    # Reduce: aggregate all function signatures
    all_signatures = []
    for fname, result in zip([f[0] for f in files], results):
        import json
        try:
            sigs = json.loads(result)
            for sig in sigs:
                sig["file"] = fname
            all_signatures.extend(sigs)
        except json.JSONDecodeError:
            pass

    return all_signatures
```

---

## 6. Best Practices

### Design the handoff contract first

Before writing any agent, define what each agent receives and what it returns. Treat it like an API contract.

```
Agent: SecurityScanner
  Input:  { code: str, language: str }
  Output: { vulnerabilities: [{issue, severity, line}], risk_level: "low|medium|high" }
```

Structured output (JSON) is more reliable than free-form text for agent-to-agent communication.

### Use the right model for each role

Don't use Opus for everything — it's expensive and often unnecessary for worker agents.

| Role | Recommended model | Why |
|------|-------------------|-----|
| Orchestrator | `claude-opus-4-6` | Needs best reasoning for decomposition |
| Research/Explore | `claude-sonnet-4-6` | Good balance of speed and quality |
| Simple extraction | `claude-haiku-4-5` | Fast, cheap for structured tasks |
| Code generation | `claude-sonnet-4-6` | Strong at code, faster than Opus |
| Security/critical review | `claude-opus-4-6` | High-stakes, needs best judgment |

### Keep prompts focused and stateless

Each agent should be self-contained. Avoid passing the full conversation history to every agent — extract only what's relevant.

```python
# Bad: passes everything
agent_prompt = full_conversation_history

# Good: passes only what this agent needs
agent_prompt = f"""
Review this function for SQL injection vulnerabilities:

{function_code}

Return findings as JSON.
"""
```

### Limit context to what matters

Before passing data to an agent, summarize or filter it. A 10,000-line file passed to every agent wastes tokens and degrades output quality.

```python
# Instead of passing the full file:
relevant_section = extract_relevant_lines(file_content, start=120, end=180)
```

### Build in verification gates

For critical pipelines, add a verification step before accepting output.

```python
def verified_code_generation(spec: str) -> str:
    for attempt in range(3):
        code = generate_code_agent(spec)
        test_result = run_tests_agent(code)
        if test_result["passed"]:
            return code
        spec += f"\n\nPrevious attempt failed with: {test_result['error']}"
    raise RuntimeError("Could not generate passing code after 3 attempts")
```

### Handle failures gracefully

Agents fail. Network errors, bad output, timeouts. Always wrap agent calls with error handling and fallbacks.

```python
try:
    result = run_agent(system_prompt, user_message)
    parsed = json.loads(result)
except json.JSONDecodeError:
    # Retry with explicit format instruction
    result = run_agent(system_prompt + "\nIMPORTANT: Return ONLY valid JSON.", user_message)
    parsed = json.loads(result)
except Exception as e:
    log_error(e)
    parsed = {"error": str(e), "fallback": True}
```

### Observe and log

Log every agent invocation with inputs, outputs, latency, and token usage. You cannot debug or optimize what you cannot observe.

```python
import time

def instrumented_agent(name: str, system_prompt: str, user_message: str) -> str:
    start = time.time()
    response = client.messages.create(...)
    duration = time.time() - start

    log.info({
        "agent": name,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "duration_ms": int(duration * 1000),
        "model": response.model,
    })

    return response.content[0].text
```

---

## 7. Anti-Patterns

### ❌ Chaining agents when one would do

If a task fits comfortably in a single context window and doesn't benefit from specialization, use one agent. Multi-agent adds latency, cost, and complexity.

### ❌ Passing the full context at every hop

Passing 50k tokens of history to every agent in a pipeline inflates cost and dilutes focus. Summarize at each handoff.

### ❌ No structure in agent output

Free-form text output between agents is brittle. If Agent A returns "the code looks good, maybe fix line 42", Agent B cannot reliably parse that. Use JSON.

### ❌ Infinite retry loops without backoff

```python
# Bad
while not result_is_valid(result):
    result = run_agent(...)   # will loop forever on a bad prompt

# Good
for attempt in range(MAX_RETRIES):
    result = run_agent(...)
    if result_is_valid(result):
        break
    time.sleep(2 ** attempt)   # exponential backoff
```

### ❌ Using the most expensive model for everything

Opus at every step in a 10-agent pipeline costs ~10× more than Sonnet. Reserve Opus for orchestration and high-stakes decisions.

### ❌ Running dependent tasks in parallel

If Agent B needs Agent A's output, they must run sequentially. Running them in parallel means Agent B starts with incomplete information.

---

## 8. Organization Playbook

### Starter kit: three pipelines to implement first

These three pipelines deliver the most value with the least complexity:

#### Pipeline 1: PR Review Bot

```
On pull_request event
       │
       ▼
Summarizer Agent    ← understands what changed and why
       │
   ┌───┴───┐
   ▼       ▼
Security  Style     ← run in parallel
Review    Review
   │       │
   └───┬───┘
       ▼
  Verdict Agent     ← go / no-go / needs changes
       │
       ▼
Post comment to PR
```

**Value:** Every PR gets a consistent, thorough review in under 60 seconds. Junior engineers get senior-level feedback. Reviewers focus on business logic, not style.

---

#### Pipeline 2: Test Generation

```
New function committed
       │
       ▼
Explore Agent       ← reads function + related code for context
       │
       ▼
Test Generator      ← writes pytest tests
       │
       ▼
Test Runner         ← executes tests, checks pass/fail
       │
       ▼
(if fail) Fixer Agent → loops back to Test Generator
       │
       ▼
Commit passing tests
```

**Value:** Eliminates "I'll write tests later." Every function ships with tests automatically.

---

#### Pipeline 3: Incident Triage

```
Alert fires
       │
   ┌───┴───┐
   ▼       ▼
Log        Metrics   ← fetch in parallel
Analyzer   Analyzer
   │       │
   └───┬───┘
       ▼
Root Cause Agent    ← synthesizes findings
       │
       ▼
Remediation Agent   ← suggests fix or runbook step
       │
       ▼
Post to Slack + create incident ticket
```

**Value:** First response in seconds, not minutes. On-call engineers get context before they even open their laptops.

---

### Team adoption checklist

- [ ] Define a standard `run_agent()` wrapper with logging, retries, and cost tracking
- [ ] Establish model selection guidelines (Opus/Sonnet/Haiku per role)
- [ ] Store all system prompts in version control — treat them like code
- [ ] Add token usage to your observability dashboard
- [ ] Start with one pipeline, measure the impact, then expand
- [ ] Set per-pipeline cost budgets and alert if exceeded
- [ ] Document each agent's contract (inputs, outputs, failure modes) in a shared wiki

### Cost estimation formula

```
Cost per pipeline run =
  Σ (input_tokens × input_price + output_tokens × output_price)
  for each agent in the pipeline

Example (PR review pipeline, ~3 agents):
  Summarizer:  3k input + 500 output  @ Sonnet rates
  Security:    4k input + 800 output  @ Opus rates
  Style:       4k input + 600 output  @ Sonnet rates
  Verdict:     2k input + 300 output  @ Opus rates

  ≈ $0.05–0.15 per PR review
```

Run 100 PRs/month = ~$5–15/month. Cheaper than one hour of an engineer's time.

---

## Quick Reference

```
Need to...                          Use...
──────────────────────────────────────────────────────────────
Run tasks simultaneously            Parallel Agent tool calls (single message)
Isolate file edits per agent        isolation: "worktree"
Continue a running agent            SendMessage(to: agentId)
Process many files efficiently      Map-reduce with async agents
Verify output quality               Generator + Critic pattern
Gate on human approval              Supervisor with review step (or GH environment)
Build a reusable pipeline           Tool-use agentic loop with handle_tool_call()
Minimize cost on simple tasks       claude-haiku-4-5 for worker agents
```

---

*Reference: [Anthropic Multi-Agent Documentation](https://docs.anthropic.com/en/docs/build-with-claude/agents)*
