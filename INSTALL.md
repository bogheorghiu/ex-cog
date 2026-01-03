# Installation Guide

## Quick Start

```bash
# Clone or download this repository
git clone https://github.com/[owner]/research-toolkit-claude.git
cd research-toolkit-claude

# Option 1: Build from source (if you have the full project)
./build-release.sh

# Option 2: Use pre-built releases (when available)
# Just use the research-toolkit/ and financial-data-mcp/ folders directly
```

## Installing research-toolkit Plugin

Copy the `research-toolkit/` folder to your Claude Code plugins directory:

```bash
cp -r research-toolkit ~/.claude/plugins/
```

Restart Claude Code to activate.

## Installing financial-data-mcp

1. Install Python dependencies:
   ```bash
   cd financial-data-mcp
   pip install -r requirements.txt
   ```

2. Configure in your project's `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "financial-server": {
         "type": "stdio",
         "command": "/path/to/financial-data-mcp/server.py",
         "args": [],
         "env": {}
       }
     }
   }
   ```

3. Test the server:
   ```bash
   python3 server.py
   ```

## Optional: claude-memory MCP

For full opus-distillatus functionality, install the memory server:

```bash
cd research-toolkit/optional/claude-memory-mcp
pip install -e .
```

See `research-toolkit/optional/claude-memory-mcp/README.md` for configuration.

## Verification

After installation, in Claude Code:

1. Skills should appear in `/skills` or skill list
2. Agent should be available via Task tool
3. Financial tools should be visible in `/tools` (if MCP configured)
