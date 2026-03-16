# financial-mcp

Financial data MCP server powered by yfinance. Provides stock prices, analysis, technical indicators, and ticker validation.

## Usage

### Claude Cowork (remote install via uvx)

Add to your Cowork MCP config:

```json
{
  "financial": {
    "command": "uvx",
    "args": [
      "--from",
      "git+https://github.com/bogheorghiu/ex-cog#subdirectory=research-toolkit/mcp-servers/financial-mcp",
      "financial-mcp"
    ]
  }
}
```

### Claude Code (plugin — auto-discovered)

When installed via the ex-cog marketplace, the plugin's `.mcp.json` handles configuration automatically using `${CLAUDE_PLUGIN_ROOT}`.

### Direct (pip install)

```bash
pip install ./research-toolkit/mcp-servers/financial-mcp
financial-mcp
```

## Tools

- `get_stock_price` — current price and basic info
- `get_stock_info` — detailed company information
- `get_stock_history` — historical price data
- `get_stock_analysis` — analyst recommendations and targets
- `get_technical_indicators` — RSI, MACD, moving averages
- `fetch_ticker` — validate and fetch ticker data
- `force_fetch_ticker` — bypass cache validation
