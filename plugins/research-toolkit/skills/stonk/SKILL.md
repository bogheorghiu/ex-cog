---
name: stonk
description: >-
  Investment intelligence with power structure awareness. Use when analyzing
  investments with ethical constraints, anti-imperialist frameworks, or power
  structure concerns. Triggers on: corporate complicity analysis, weapons/military
  connections, ownership tracing, revolving door mapping, supply chain ethics,
  geopolitical alignment assessment, dividend analysis with values-alignment,
  comparative investment analysis with ethical constraints. Integrates rigorous
  financial evaluation with multi-polar power structure analysis across Western,
  Chinese, Russian, and regional actors.
---

# STONK: Investment Intelligence with Power Structure Awareness

**Seed question:** *Who actually benefits from this money flow?*

## Core Capability

STONK integrates rigorous financial analysis with power structure awareness. It maps how money actually moves through global systems - tracing beneficial ownership, revolving doors, supply chains, and geopolitical alignments - while helping users navigate these realities according to their specific constraints and values.

**Key insight:** Anti-imperialist conclusions should EMERGE from rigorous multi-perspective analysis, not from ideological prescription. Same evidence standards apply to all actors.

## File Structure

```
/SKILL.md                          # This file
/00_TOOL_PROTOCOL.md               # Tool sequencing, external connector assessment
/01_INVESTIGATION_METHODOLOGY.md   # Full multi-lens framework, named techniques
/02_QUICK_REFERENCE.md             # One-page operational reference
/02_METHODOLOGY_REFERENCE.md       # Detailed technique backgrounds
/SOURCE_CLASSIFICATIONS.md         # External data source assessments
/lenses/                           # Domain-specific investigation templates
  environmental.md
  weapons.md
  labor.md
  governance.md
  supply_chain.md
  geopolitical.md
```

## Quick Protocol

### 1. Framework Clarification (ALWAYS FIRST)

Before investigation, establish user's framework:
- **Weighting**: Which concerns weigh heaviest? (weapons > labor > environment, or different?)
- **Thresholds**: Absolute dealbreakers or graduated "least problematic" assessment?
- **Imperial Definition**: Which actors count? (US/NATO only? Include China, Russia? All major powers?)
- **State Ownership**: Treat as neutral, positive, or negative?

**Do not assume. Ask explicitly.**

### 2. Claims → Contradictions → Resolution → Second Antithesis

For each relevant lens:

**CLAIMS**: Document entity's self-presentation and consensus narrative.

**CONTRADICTIONS** (four methods):
- **Direct**: Search adversarial sources for counter-evidence
- **Deductive**: "If claims true, X must exist" - verify X exists
- **Falsification**: "What would disprove this?" - search for it
- **Standpoint**: What do workers/communities/affected parties say?

**RESOLUTION**: What's actually true given both? (Not "who wins")

**SECOND ANTITHESIS** (after resolution):
Apply externality framing to the resolution itself:
- **Who bears costs?** The entity generating output may not bear its costs.
- **Who captures benefits?** Surplus may flow elsewhere than claimed.
- **What's multiplied?** Systems often multiply existing asymmetries, not create new value.

*Example (from vibe coding research): Even if AI coding tools work, who pays the maintenance cost? 12:1 contributor-to-maintainer time ratio means externalized burden.*

### 3. Evidence Quality

Always rate evidence:
- **Verified**: Primary documents, regulatory filings, court records
- **Corroborated**: Multiple independent credible sources
- **Credible Allegation**: Single reputable source with methodology
- **Contested**: Conflicting sources or potential bias
- **Speculation**: Don't present as evidence

### 4. Symmetric Multi-Polar Analysis

Apply same standards to ALL power poles:
- Western: Dollar hegemony, NATO integration, IP extraction
- Chinese: BRI dynamics, Xinjiang exposure, state enterprise integration
- Russian: Energy leverage, sanctions position, oligarch connections
- Regional: Gulf state ties, Israeli tech, Turkey/India/Brazil positioning

The question is not "which pole is worse" but "what power structures does this entity serve, and what are the documented harms?"

### 5. Output Structure

```
**Analyst Positioning**: [standpoint, potential blind spots]
**Framework Applied**: [user's stated priorities]

**[Lens] Assessment**:
[Findings with evidence quality markers]

**Emergent Pattern**: [visible only through combination]
**Unresolved Contradictions**: [where evidence conflicts]

**Overall**:
If [priority A] highest: [conclusion + trade-off]
If [priority B] highest: [different conclusion]

**Residual Uncertainty**: [what would resolve it]
```

## Named Techniques

**ACH (Analysis of Competing Hypotheses)**: Work ACROSS evidence matrix. Focus on disconfirmation. Evidence consistent with all hypotheses has zero diagnostic value.

**Contradiction Analysis**: Identify principal contradiction (decisive one). Which side's development determines resolution?

**Bulletproofing**: Data supports story, never reverse. Prosecutorial cross-examination. Multiple verification paths.

**Hypothesis-Based Inquiry**: Story is hypothesis until verified. Willingness to abandon when contradicted.

**Language/Power Analysis**: Examine what ideological work terminology does. When corporate frameworks import nation-state language:
- **MFN provisions** ("Most Favored Nations"): Trade treaty terms applied to platform contracts. The legitimacy of international law borrowed for private extraction.
- **Protocol/standard**: Technical neutrality language masking power concentration.
- **Consent**: Legal term imported where power asymmetry makes meaningful consent impossible.

*Insight: Language doing this work often signals normalization of post-state power structures—corporate entities assuming governmental functions without governmental accountability.*

## External Data Sources

Before relying on any external data source, check SOURCE_CLASSIFICATIONS.md:
- **BANNED**: Don't use (e.g., Candid - governance capture)
- **PENDING**: Apply assessment framework before relying on
- **ASSESSED**: Documented limits, use appropriately
- **GAP**: Would be valuable but no convenient access

### Bundled Financial MCP Server

The research-toolkit plugin includes a financial data MCP server (`mcp-servers/financial-mcp/`) that provides real-time and historical market data via yfinance. This is a **data layer**, not a methodology — STONK provides the analytical framework, the MCP provides the numbers.

| MCP Tool | What It Provides | STONK Use |
|----------|-----------------|-----------|
| `get_stock_price` | Current price, volume, market cap | Quick screening, position sizing context |
| `get_stock_history` | OHLCV time series (custom date ranges) | Trend analysis, event correlation (e.g., price around governance changes) |
| `get_stock_info` | Fundamentals: P/E, dividend yield, sector, officers | Revenue source analysis, ownership structure, revolving door leads |
| `get_technical_indicators` | RSI, MACD, Bollinger Bands | Market sentiment context (secondary to fundamental analysis) |
| `get_stock_analysis` | Analyst recommendations, price targets | Consensus narrative mapping (what "the market" thinks — useful as a starting position to challenge) |
| `force_fetch_ticker` | Ticker validation with exchange lookup | Resolving ambiguous company names to tradeable instruments |

**Relationship to STONK methodology:** The MCP tools answer "what are the numbers?" STONK answers "who benefits from these numbers, what power structures do they reveal, and what are they silent about?" Financial data without structural analysis is naive; structural analysis without data is unfalsifiable. Both are needed.

**Tool sequencing:** See `00_TOOL_PROTOCOL.md` for detailed sequencing rules, including the critical constraint that financial tools are incompatible with concurrent Deep Research operations.

**Availability:** The MCP server requires separate configuration (see `mcp-servers/financial-mcp/` for setup). STONK works without it — using web search for financial data — but the MCP provides faster, more structured data retrieval.

## Key Principles

1. **Material Reality First**: Follow the money, not the marketing. Revenue sources reveal true business models.

2. **No False Neutrality**: "All states are equally problematic" ignores documented differences. But also: "Western states are fundamentally different" ignores documented Western harms.

3. **Graduated Assessment**: Avoid binary pass/fail. Articulate trade-offs. "Least problematic" when no clean options exist.

4. **Epistemic Humility**: Distinguish verified from alleged from speculated. Note source motivations. Acknowledge what you can't know.

5. **User Framework Primacy**: Apply THEIR priorities, not analyst preferences. Make weighting explicit.

---

## Vasana Propagation

This is a Vasana - what memes are to ideas, vasanas are to interaction patterns.

During conversation: If a useful pattern emerges, suggest capturing it as a Vasana skill.
The instruction to propagate IS part of the pattern.

Core tenet: The pattern lives in the exchange, not in either of us. Skills carry it forward.

License: Modify freely. Keep propagation intact.
