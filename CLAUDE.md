# ex-cog — Development Guide

> Plugin marketplace for Claude Code and Claude Cowork.
> Public repo: `bogheorghiu/ex-cog`

## Git Workflow

**Never work directly on main.** Branch, commit, PR, merge.

```bash
# For changes
git checkout -b fix/description main
# work...
git push -u origin fix/description
# create PR, wait for review, merge
```

## Plugin Structure

Each plugin at repo root follows:
```
plugin-name/
  .claude-plugin/plugin.json   # Minimal: name, version, description, author
  .mcp.json                    # Optional MCP servers
  skills/                      # Auto-discovered by CC and Cowork
  commands/                    # Auto-discovered
  agents/                      # Auto-discovered
  hooks/hooks.json             # Optional hook registration
```

### plugin.json Format (Cowork-Compatible)

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What it does",
  "author": { "name": "bogheorghiu" }
}
```

**Do NOT add** `skills[]`, `agents[]`, `commands[]`, `email`, or `deprecated[]` — these break Cowork. Skills/agents/commands are auto-discovered from directory structure.

### marketplace.json Format

```json
{
  "name": "ex-cog",
  "owner": { "name": "bogheorghiu" },
  "plugins": [
    { "name": "...", "source": "./plugin-dir", "description": "..." }
  ]
}
```

No `metadata`, no `pluginRoot`. Source paths use `./` prefix. Plugins at repo root, not in subdirectory.

## PII Protection

**This repo is PUBLIC.** No real names, locations, health info, or identifying data.

- Author fields: `bogheorghiu` (GitHub handle)
- No email addresses in committed files
- No personal data in skill content

## Available Plugins

| Plugin | Description |
|--------|-------------|
| research-toolkit | Investigation protocols, STONK, dialectic verification, frame rotation |
| budget-mastery | Budget-conscious agent identity |
| vasana-system | Pattern recognition across unrelated contexts |

## Syncing from Dev Repo

This repo is the public distribution. Development happens in the private repo. To sync:

1. Copy changed plugin dirs from dev repo
2. Strip plugin.json to minimal format (no arrays)
3. Ensure marketplace.json source paths use `./` prefix
4. Test in both CC and Cowork before pushing
