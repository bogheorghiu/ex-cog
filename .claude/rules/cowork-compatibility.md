# Cowork Compatibility (ENFORCED)

This repo serves BOTH Claude Code and Claude Cowork. Cowork has a stricter parser.

## plugin.json Rules

Only these fields: `name`, `version`, `description`, `author` (with `name` only).

**Never add:** `skills[]`, `agents[]`, `commands[]`, `deprecated[]`, `author.email`

Skills, agents, and commands are auto-discovered from directory structure.

## marketplace.json Rules

- No `metadata` wrapper
- No `pluginRoot`
- Source paths: `./plugin-name` (with `./` prefix)
- Plugins at repo root (not in subdirectory)

## Reference

Working example: `anthropics/financial-services-plugins`
