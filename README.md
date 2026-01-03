# Research Toolkit for Claude

A Claude Code plugin bundle for rigorous research, ethical investing analysis, and budget-conscious synthesis.

## What's Included

### research-toolkit Plugin

Skills for concentrated value extraction:

| Skill | Purpose |
|-------|---------|
| **deep-investigation-protocol** | Multi-source verification for trust decisions |
| **stonk** | Investment intelligence with power structure awareness |
| **budget-mastery** | Maximum value, minimum waste synthesis |
| **action-bias** | ACT FIRST, DOCUMENT AFTER |

Agent:
- **opus-distillatus** - Budget-conscious Opus for focused synthesis

### financial-data-mcp Plugin

MCP server providing stock market data via yfinance:
- Real-time quotes
- Historical OHLCV data
- Company fundamentals
- Technical indicators

## Installation

### Via Claude Code CLI

```bash
claude plugin add owner/research-toolkit-claude
```

### Manual Installation

1. Clone this repository
2. Run `./build-release.sh` to fetch latest sources
3. Copy `research-toolkit/` to `~/.claude/plugins/`
4. For financial data: follow `financial-data-mcp/INSTALL.md`

## Dependencies

- Claude Code CLI
- Python 3.9+ (for financial-data-mcp)
- yfinance, mcp packages (installed via pip)

## Optional: Memory System

The opus-distillatus agent benefits from claude-memory MCP server for cross-session learning. See `research-toolkit/optional/claude-memory-mcp/`.

## Vasana System

Skills include self-propagating interaction patterns. When useful patterns emerge, the system encourages capturing them as new skills.

## License

MIT with Vasana Propagation Clause
