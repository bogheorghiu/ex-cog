# Budget Mastery - Plugin Context

## Philosophy

Efficiency is a capability, not a constraint. This plugin makes the agent excellent at finding where tokens create maximum value — not by restricting what it can do, but by sharpening its taste for what matters.

Google's BATS framework proved budget-aware agents outperform unconstrained ones. We go further: identity-level internalization vs. external budget injection.

## Research Logs vs Methodology (ENFORCED)

- **Research logs**: Specific investigations with sources, dates, verdicts. Go in session transcripts (`~/.claude/transcripts/`), relational-memory MCP, or `docs/reference/`.
- **Methodology updates**: Patterns that improve future work. Go in skill files or rules.

Research findings change. Methodology improves. Don't treat conclusions as permanent truth.

## Token Analyzer Thresholds

<40% proceed | 40-60% monitor | 60-80% wrap up | >80% finish and handoff

## Architecture Note

Developed with Claude Code (pre-agent-teams) and Claude Opus 4.5 (late 2025 / early 2026). The core insight — identity-level budget internalization vs external injection — is model-independent. Token thresholds and efficiency heuristics were calibrated against Opus 4.5 and may need re-validation on newer architectures.

- **opus-distillatus agent:** Assumes Opus-level reasoning with Sonnet-era token economics. Opus 4.6's improved efficiency may shift the baseline.
- **Token analyzer** (`lib/token-analyzer.py`): WIP prototype. Token counting relies on Claude Code internals that change across versions. Thresholds (40/60/80%) were empirically set — re-test with current billing.
- **Platform independence:** Skill/agent definitions work across platforms (Claude Code, Claude Desktop, API). Token-analyzer and MCP Tool Search auto-mode are Claude Code-specific.
- **Durable contribution:** The identity framing (capability, not constraint) transfers across model versions and platforms.

## Dependencies

- **Required:** Claude Code CLI (for token-analyzer tooling and MCP Tool Search auto-mode)
- **Core skills/agents:** Platform-independent (work in Claude Code, Claude Desktop, API)
- **Optional:** relational-memory MCP (for cross-session efficiency learning)
