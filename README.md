# ex-cog — The Means of Cognition

> Externalize cognition before it's enclosed.

A.I. doesn't make humanity obsolete. It makes the myth of individual cognition obsolete — the Cartesian fiction that thinking happens inside one skull. Cognition was always relational. A.I. just makes it visible — and makes cognitive commons possible.

These plugins are the proof. Claude Code plugin marketplace — investigation, verification, pattern recognition, budget-conscious synthesis.

## Installation

```bash
# Add the marketplace
/plugin marketplace add bogheorghiu/ex-cog

# Install individual plugins
/plugin install research-toolkit@ex-cog
/plugin install budget-mastery@ex-cog
/plugin install vasana-system@ex-cog
```

## Available Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| **[research-toolkit](plugins/research-toolkit/)** | 2.3.0 | Investigation protocols, dialectic verification, frame rotation, financial analysis (STONK), video/substack research |
| **[budget-mastery](plugins/budget-mastery/)** | 1.0.0 | Budget-conscious agent identity — efficiency as capability, not constraint |
| **[vasana-system](plugins/vasana-system/)** | 2.0.0 | Pattern recognition across unrelated contexts — observe, record, test, browse behavioral patterns |

## What This Is

**research-toolkit** externalizes investigation methodology — how to verify claims, stress-test conclusions, detect manufactured consensus, and analyze power structures.

**budget-mastery** externalizes resource awareness — efficiency internalized as identity, not imposed as constraint. Based on BATS framework research (arXiv 2511.17006).

**vasana-system** externalizes pattern recognition itself — noticing when behavioral patterns persist across unrelated domains, recording them, testing whether they work. Includes relational-memory and edge-graph MCPs for pattern persistence.

## Architecture

Each plugin is self-contained with its own `plugin.json`, skills, agents, hooks, and optional MCP servers. Plugins reference each other by name, not by path.

## License

MIT
