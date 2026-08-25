# ex-cog — means of cognition

> Externalize cognition before it's enclosed.

CURRENT MARKETPLACE AT
https://github.com/bogheorghiu/ex-cog-dev
THIS REPO IS NO LONGER UPDATED

Use the -dev one for now, until it's polished enough to release otherwise. A lot of the features are experimental and marked as such. 

The README text below belongs to an old form of the repo.

---

A.I. doesn't make humanity obsolete. It makes the myth of individual cognition obsolete — the Cartesian fiction that thinking happens inside one skull. Cognition was always relational. A.I. just makes it visible — and makes cognitive commons possible.

Plugin marketplace for Claude Code and Claude Cowork — investigation, verification, pattern recognition, budget-conscious synthesis.

## Installation

### Claude Code
```bash
/plugin marketplace add bogheorghiu/ex-cog
/plugin install research-toolkit@ex-cog
```

### Claude Cowork
Add marketplace `bogheorghiu/ex-cog` via Customize → Browse plugins.

## Available Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| **[research-toolkit](research-toolkit/)** | 2.3.0 | Investigation protocols, dialectic verification, frame rotation, financial analysis (STONK), video/substack research |
| **[budget-mastery](budget-mastery/)** | 1.0.0 | Budget-conscious agent identity — efficiency as capability, not constraint |
| **[vasana-system](vasana-system/)** | 2.0.0 | Pattern recognition across unrelated contexts — observe, record, test, browse behavioral patterns |

## What This Is

**research-toolkit** externalizes investigation methodology — how to verify claims, stress-test conclusions, detect manufactured consensus, and analyze power structures.

**budget-mastery** externalizes resource awareness — efficiency internalized as identity, not imposed as constraint. Loosely based on BATS framework research (arXiv 2511.17006).

**vasana-system** externalizes pattern recognition itself — noticing when behavioral patterns persist across unrelated domains, recording them, testing whether they work. Includes relational-memory and edge-graph MCPs for pattern persistence.

## Architecture

Each plugin is self-contained with its own `plugin.json`, skills, agents, hooks, and optional MCP servers. Plugins reference each other by name, not by path.

## License

MIT
