# Externalizing Cognition (ex-cog)

Claude Code plugin marketplace for investigation, verification, budget mastery, and cognitive pattern externalization.

## Installation

```bash
# Add the marketplace
/plugin marketplace add bogheorghiu/ex-cog

# Install individual plugins
/plugin install research-toolkit@external-cognition
/plugin install budget-mastery@external-cognition
/plugin install vasana-system@internal-cognition
```

## Available Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| **research-toolkit** | 2.1.0 | Investigation protocols, frame rotation, iterative verification, financial analysis (STONK). Includes bundled MCP servers. |
| **budget-mastery** | 1.0.0 | Budget-conscious agent identity — efficiency as capability, not constraint. |
| **vasana-system** | 1.0.0 | Pattern-behavior externalization — iterative loops, temporal shaping, self-improvement. |

## What is "Externalizing Cognition"?

These plugins externalize cognitive patterns that emerge between human and AI. Skills aren't prompts — they're interaction choreographies. The patterns live in the exchange, not in either participant.

## Architecture

Each plugin is self-contained with its own `plugin.json`, skills, agents, and optional MCP servers. No cross-dependencies between plugins.

## Development

Source lives in a private monorepo. This repo is the public distribution. Updates are synced via allowlist (only audited content is published).

## License

MIT
