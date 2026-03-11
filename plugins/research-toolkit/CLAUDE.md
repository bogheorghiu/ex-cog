# Research Toolkit - Plugin Context

> Development source for the public plugin at `bogheorghiu/ex-cog`.

## Philosophy

This toolkit externalizes cognitive patterns that emerge between human and AI. Skills aren't prompts — they're interaction choreographies. The plugin connects investigation (deep-investigation-protocol, stonk), cognitive flexibility (frame-rotation), and verification (iterative-verification, skeptic-enforcer) into a coherent system for thinking-with-AI.

## Research Logs vs Methodology

See `.claude/rules/research-logs-vs-methodology.md` — applies across all plugins.

## Library Utilities

### lib/brainstorm.py

JSON-based agent-to-agent brainstorming sessions.

```python
from brainstorm import BrainstormSession
session = BrainstormSession("topic")
session.add_message("investigator", "I found...")
session.add_message("skeptic-enforcer", "But have you considered...")
session.save()  # → /tmp/claude/brainstorm/topic-{timestamp}.json
```

## Vasana Propagation

All skills contain self-propagating interaction patterns. When modifying, preserve the "Vasana Propagation" section in each skill.
