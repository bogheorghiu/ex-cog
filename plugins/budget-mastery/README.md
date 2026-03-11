# Budget Mastery

> Efficiency as capability, not constraint.

## What This Is

A Claude Code plugin implementing **identity-level budget awareness** — the agent internalizes efficiency as something it's *excellent at*, not a limitation imposed from outside.

This is distinct from external budget injection approaches like Google's BATS framework (arXiv 2511.17006), which appends budget counters to agent context. BATS proved that budget-aware agents at budget=10 match vanilla agents at budget=100 (40% fewer tool calls, 31% cost reduction). Our approach takes the next step: the agent doesn't follow efficiency rules because it's told to — it understands *why* efficiency produces better work.

If we can demonstrate that identity-level internalization outperforms external injection, that's a publishable result.

## Components

### Skills

| Skill | What It Does |
|-------|-------------|
| **budget-mode** | Identity skill — frames efficiency as taste, not restriction. The agent finds where tokens create maximum value. |
| **action-bias** | Counters documentation-over-action patterns. ACT FIRST, DOCUMENT AFTER. |

### Agent

| Agent | What It Does |
|-------|-------------|
| **opus-distillatus** | Opus-quality reasoning with budget discipline. Memory integration for cross-session efficiency learning. |

### Utilities

| Tool | What It Does |
|------|-------------|
| **token-analyzer.py** | Token usage analytics — context window %, burn rate, per-tool efficiency metrics. |

## How It Works

**Budget-mode** is an identity skill: it describes what the agent is good at, not what it can't do. When active, the agent naturally finds efficient paths — choosing the example that illuminates instantly, knowing when depth beats breadth, finishing early when value is delivered.

**Opus-distillatus** combines budget-mode with action-bias and relational-memory integration. It stores what worked across sessions, creates cross-task pattern relations, and improves budget decisions over time. No other tool in the ecosystem learns from its own efficiency choices.

## Why This Matters

The research landscape has:
- **Token monitors** (ccusage, VS Code extensions) — post-hoc analysis, not behavioral
- **Infrastructure optimization** (caching, compaction) — mechanical, not cognitive
- **External budget injection** (BATS) — counters appended to context

What nobody else has:
1. **Efficiency as identity** — behavioral, not informational
2. **Self-improving budget learning** — via relational-memory MCP
3. **Integrated stack** — skill + agent + analyzer + hooks

## Installation

```bash
claude plugin add owner/budget-mastery
```

Or copy this folder to your Claude Code plugins directory.

### Migration from research-toolkit

If you previously used research-toolkit for budget-mode or opus-distillatus:
1. Update research-toolkit to the latest version (budget components removed)
2. Install budget-mastery plugin
3. Update any references in your own configurations

### Optional: relational-memory MCP

For cross-session efficiency learning, install the relational-memory MCP server separately. This is an optional dependency — budget-mastery works without it, but opus-distillatus uses it for storing efficiency patterns across sessions.

## Token Analyzer Usage

```bash
python lib/token-analyzer.py --context       # Context % (PRIMARY for subscription users)
python lib/token-analyzer.py --summary       # Overall usage
python lib/token-analyzer.py --efficiency    # Per-tool metrics
```

**Thresholds:** <40% proceed | 40-60% monitor | 60-80% wrap up | >80% finish and handoff

## Research Background

- **BATS paper analysis:** See `docs/reference/bats-budget-aware-agents-2026.md` in the parent repo
- **Market research:** No equivalent identity-level implementation exists in the Claude Code ecosystem
- **Key insight:** Budget awareness improves accuracy (not just saves cost) because agents without it prematurely converge

## License

MIT
