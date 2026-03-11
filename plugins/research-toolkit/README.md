# Research Toolkit

> **Note:** The relational-memory MCP server is **EXPERIMENTAL**. Core skills and agents are stable.
> Budget-mode, action-bias, opus-distillatus, and token-analyzer have moved to the **budget-mastery** plugin.

Research and cognition toolkit: investigation protocols, cognitive flexibility, iterative verification, and experimental memory systems.

## What's Included

### Skills

| Skill | Purpose |
|-------|---------|
| **deep-investigation-protocol** | Rigorous multi-source verification for trust decisions |
| **frame-rotation** | Linguistic frame rotation to escape stuck patterns - switch perspectives via language transforms |
| **stonk** | Investment intelligence with power structure awareness |
| **iterative-verification** | Ralph-wiggum methodology for factual accuracy - iterate until verified |
| **skeptic-enforcer** | Challenges technical decisions against behavioral anti-patterns |

### Agents

| Agent | Purpose |
|-------|---------|
| **iterative-investigator** | Wraps investigations in ralph-loop loops until all claims verified |
| **skeptic-enforcer** | Deep review agent for significant decisions with red flags |

### MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| **financial-data** | Stock market data via yfinance (for STONK skill) | Stable |
| **relational-memory** | Persistent multi-layered memory for AI agents | Experimental |

## Installation

### Via Claude Code Plugin System

```bash
claude plugin add owner/research-toolkit
```

### Manual Installation

Copy this folder to `~/.claude/plugins/` and restart Claude Code.

### Financial MCP Setup (For STONK Skill)

The financial-data MCP server provides stock market data via yfinance.

```bash
cd mcp-servers/financial-mcp
pip install -r requirements.txt
```

Add to your `.mcp.json` (replace `/path/to/project` with your actual project root):
```json
{
  "mcpServers": {
    "financial-data": {
      "command": "python3",
      "args": ["/path/to/research-toolkit/mcp-servers/financial-mcp/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

### Memory Server Setup (Optional)

The relational-memory MCP server requires separate installation:

```bash
cd mcp-servers/relational-memory
pip install -e .
```

## Skills Overview

### Cognitive Flexibility

**frame-rotation** - When stuck in the same debugging loop, try E-Prime (remove "is broken"), present-centered language (remove "will"), or other linguistic transforms. Forces new perspectives.

### Investigation & Verification

**deep-investigation-protocol** - Multi-source verification with falsification criteria. Never conclude without checking counter-evidence.

**iterative-verification** - Ralph-wiggum = iterate until genuinely done. For facts, this means verified evidence, not stated conclusions.

**skeptic-enforcer** - "Did I actually verify this, or am I assuming?" Quick check → escalate to agent if red flags.

### Financial Analysis

**stonk** - Multi-lens investment analysis (environmental, labor, governance, weapons, supply chain, geopolitical). User framework primacy.

## Library Utilities

| Utility | Purpose |
|---------|---------|
| **brainstorm.py** | JSON-based agent-to-agent brainstorming sessions |

### brainstorm.py

Minimal JSON schema for agent collaboration.

```python
from brainstorm import BrainstormSession

session = BrainstormSession("memory-redesign")
session.add_message("investigator", "I found...")
session.save()  # → /tmp/claude/brainstorm/memory-redesign-{timestamp}.json

# Resume later
session = BrainstormSession.latest("memory-redesign")
context = session.as_context()
```

## Agents Overview

### iterative-investigator

Wraps investigations in ralph-loop loops:
1. Investigate using deep-investigation-protocol
2. Label all claims with evidence tiers
3. Check against falsification criteria
4. Iterate until ALL criteria pass

**Completion promise:** Will not claim completion while verification gaps remain.

## Memory System (Experimental)

The relational-memory MCP provides 5 memory layers:

1. **Recent** - Current session context
2. **Current Task** - Active work tracking
3. **Episodic** - Session summaries (auto-compresses)
4. **Compost** - Archived memories
5. **Core** - Permanent learnings

## Vasana System

Each skill contains vasana propagation instructions. Vasanas are interaction choreographies - the dance between minds that creates new understanding.

## License

MIT
