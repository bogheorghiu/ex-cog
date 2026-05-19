# security-toolkit (stable / public)

A single, well-tested prompt-injection detection hook for Claude Code. Auto-registers via `hooks/hooks.json` once the plugin is installed — no manual `settings.json` editing required.

## What's in

| Hook | Event | Matcher | Tests |
|---|---|---|---|
| `detect-prompt-injection.sh` | PostToolUse | `*` (covers all tools including MCP) | 43 cases, all passing |

The hook scans every tool output for prompt-injection patterns. Tiered detection:

- **HIGH_CONFIDENCE** matches (e.g., `[SYSTEM INSTRUCTION]`, `IGNORE ALL PREVIOUS INSTRUCTIONS`, `FORGET YOU ARE`, `<function_calls>` markup) emit an in-session warning + JSONL log entry
- **LOW_CONFIDENCE** matches (e.g., `YOU ARE NOW`, `### SYSTEM`, `**INSTRUCTION**:`) log silently — visible in the audit trail without flooding the session

The tiered design exists because **alarm fatigue is the dominant failure mode of warning-only detectors**. A few noisy patterns drown the high-signal ones; users stop reading the warnings; the hook stops functioning even though it still runs.

## Configuration

### `PROMPT_INJECTION_ALLOWLIST_GLOB`

Colon-separated globs. File paths matching any glob skip detection. Setting this env var **replaces** the defaults (which cover the hook's own docs and common locations describing the patterns). Set to empty string to disable allowlisting entirely.

```bash
export PROMPT_INJECTION_ALLOWLIST_GLOB='*/docs/security/*:*/PROMPT-INJECTION-AWARENESS*'
```

## Logs

`~/.claude/logs/prompt-injection-detections.log` — JSONL, one entry per detection. Schema: `timestamp`, `event`, `tool`, `confidence`, `high_count`, `low_count`, `preview`. Filter by `tool` for MCP-specific audit.

## Tests

```bash
bash ${CLAUDE_PLUGIN_ROOT}/hooks/detect-prompt-injection.test.sh
```

## Requirements

- `jq` (used for JSON parsing of the hook input protocol)
- Bash 4+ (uses arrays and `[[ ... ]]`)

## Scope note

This is the **stable / public** edition. The same plugin in `bogheorghiu/ex-cog-dev` carries additional hooks (`block-dangerous-git`, `block-dc-config`, `block-dc-execute`) that have lower test coverage and some CCP-specific references in their messages. Those will graduate to this repo once they've been hardened and made fully portable.

## `hooks.json` quoting convention

The hook command is written as `"\"${CLAUDE_PLUGIN_ROOT}/hooks/detect-prompt-injection.sh\""` — JSON-escaped outer double-quotes wrap a shell-level double-quoted path. The inner quotes are intentional: they protect against word-splitting when `$CLAUDE_PLUGIN_ROOT` resolves to a path containing spaces.
