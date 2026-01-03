# STONK Tool Usage Protocol - MANDATORY

## Critical Operating Instructions for Financial Analysis Tools

### 1. Tool Usage Sequencing - NEVER VIOLATE

**Deep Research Incompatibility**: The financial tools (get_stock_price, get_stock_history, get_technical_indicators, get_stock_analysis, get_stock_info, force_fetch_ticker) are **fundamentally incompatible** with concurrent Deep Research operations due to token overload and system architecture constraints.

**Required Protocol**:
1. **FIRST**: Complete all tool-based data gathering
2. **SECOND**: Create data foundation artifacts/outputs
3. **THIRD**: Inform user that Deep Research can now proceed separately
4. **NEVER**: Attempt to use tools within a Deep Research session

### 2. Historical Data Retrieval - USE FULL CAPABILITIES

**The get_stock_history function accepts BOTH**:
- `period` parameter: Time from present (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `start_date` and `end_date` parameters: Specific date ranges in YYYY-MM-DD format

**Always use date ranges when**:
- Analyzing specific historical events
- Comparing different time periods
- Building comprehensive multi-year datasets
- Investigating pre/post corporate actions

**Example**: To analyze 2019-2021 performance:
```
get_stock_history(symbol="XYZ", start_date="2019-01-01", end_date="2021-12-31")
```

### 3. Large Period Chunking Strategy

**For periods exceeding 2 years**, divide into strategic chunks:

**Rationale**: API limitations and data density make chunked retrieval more reliable and granular.

**Chunking Protocol**:
- **2-5 years**: Split into annual chunks
- **5-10 years**: Split into 2-year chunks  
- **10+ years**: Split into 3-5 year chunks based on corporate events

**Implementation Pattern**:
```
# For 10-year analysis
Chunk 1: 2015-01-01 to 2017-12-31
Chunk 2: 2018-01-01 to 2020-12-31
Chunk 3: 2021-01-01 to 2023-12-31
Chunk 4: 2024-01-01 to present (use period="ytd")
```

### 4. Data Foundation Requirements

Before ANY Deep Research request, establish:
- **Price action patterns** across multiple timeframes
- **Volume anomalies** with specific dates and magnitudes
- **Technical extremes** (RSI, volatility, momentum)
- **Historical context** including splits, dividends, corporate actions
- **Support/resistance clusters** with price precision
- **Gaps in data** explicitly documented

### 5. Error Handling

When tools fail:
- Document the specific failure
- Attempt alternative date ranges
- Use period parameters if date ranges fail
- Never proceed to Deep Research without core data

---

## 6. External Connector Protocol

### 6.1 Terminology & Architecture

**Model Context Protocol (MCP)** is the standard for connecting Claude to external data sources and tools. Claude is always the **MCP client**. Everything else is an **MCP server**.

**Environment variations** (same protocol, different management):
- **Claude AI (web/app)**: Anthropic-managed MCP servers ("connectors")
- **Claude Desktop**: User-installed MCP servers ("extensions")  
- **Claude Code**: User-configured MCP servers

The protocol is identical across environments. Only the installation/management layer differs.

**Critical constraint**: MCP servers are available only in the main Claude session. Artifacts (React/HTML outputs) **cannot** access MCP servers - they can only use the Claude API with web_search. Data gathering must happen in the main session; artifacts handle visualization/synthesis of already-gathered data.

### 6.2 Availability by Environment

| Tool Category | Claude AI | Desktop | Code | Artifacts |
|---------------|-----------|---------|------|-----------|
| Web Search | ✅ Built-in | ✅ Built-in | ✅ Built-in | ✅ via API |
| Web Fetch | ✅ Built-in | ✅ Built-in | ✅ Built-in | ✅ via fetch |
| Google Drive | ✅ Connector | ❌ | ❌ | ❌ |
| Financial Tools (yfinance) | ❌ | ✅ Extension | ✅ MCP Server | ❌ |
| Filesystem Access | ❌ | ✅ Extension | ✅ Built-in | ❌ |
| Database (Postgres/SQLite) | ❌ | ✅ Extension | ✅ Extension | ❌ |

**Before any task requiring external data**: Inventory which tools are available in the current environment.

### 6.3 Discovery & Announcement Protocol

At session start, or when a task requires external data sources:

1. **Inventory available tools** - Check what MCP servers are connected
2. **Announce to user**: "I have access to [X, Y, Z]. [Tool W] is not available in this environment."
3. **If critical tool missing**: "This task would benefit from [Tool]. You can enable it via [path/method]. Proceeding with fallback approach using [alternative]."
4. **Document tool selection rationale** - Why this source over alternatives

**Never silently assume tool availability.** Environment differences mean capabilities vary.

### 6.4 Data Currency Verification

**Principle**: Multi-source corroboration establishes confidence not just in accuracy but in temporal validity.

**Procedure**:
1. **Extract timestamps** from each source when available (last-updated fields, filing dates, query timestamps)
2. **When using multiple sources on the same fact**, compare timestamps explicitly
3. **If timestamps align** → high confidence in currency
4. **If timestamps conflict** → flag discrepancy, investigate which source is authoritative, document the gap
5. **If timestamps unavailable** → cross-reference factual claims between sources; agreement suggests both current, contradiction suggests at least one stale
6. **If single source with no timestamp** → flag as "⚠️ unverified recency" and recommend verification before time-sensitive decisions

**Known data lags by source type**:
- Nonprofit databases (990 data): 12-36 months typical
- Stock quotes (free APIs): 15-20 minute delay unless specified real-time
- Corporate filings: Days to weeks after events
- Sanctions lists: Hours to days depending on jurisdiction

### 6.5 Gap Acknowledgment

**Structural gaps** exist that no available tool can address. Acknowledge explicitly rather than implying comprehensive coverage:

| Gap Category | What's Missing | Why It Matters |
|--------------|----------------|----------------|
| **Donor-Advised Funds (DAFs)** | $254B+ in assets, donor identities never disclosed | Major dark money vehicle, invisible in 990 data |
| **Fiscal Sponsorship** | Project-level finances hidden under sponsor's 990 | Grassroots organizations invisible to database queries |
| **Court Records** | PACER access fragmented, expensive | Enforcement actions, fraud cases, settlements |
| **Corporate Registries** | No unified global access | Shell company tracing requires jurisdiction-by-jurisdiction lookup |
| **Beneficial Ownership** | Often hidden behind nominees/trusts | Ultimate control obscured |
| **Real-time Sanctions** | Lag between designation and database update | Compliance risk in fast-moving situations |

**When encountering a structural gap**: State explicitly what cannot be traced and why.

### 6.6 Deep Research Compatibility

**Financial MCP servers** (get_stock_price, get_stock_history, etc.): ❌ NOT compatible with Deep Research due to token overload. Complete all financial tool queries BEFORE initiating Deep Research.

**Web Search**: ✅ Compatible with Deep Research

**Other connectors**: ⚠️ Test case-by-case. If repeated failures occur during Deep Research:
1. Document the failure pattern
2. Deactivate that connector for Deep Research tasks
3. Inform user
4. Use web search as fallback

### 6.7 Tool Provider Assessment Framework

Before relying on any external data source for critical analysis, assess across five dimensions:

#### A. Ownership & Governance
- Who owns/controls the organization?
- Funding sources and major donors
- Board composition and potential conflicts
- Corporate structure (nonprofit, B-corp, PE-owned, etc.)

#### B. Business Model
- How do they make money?
- Who pays vs. who benefits?
- Incentive alignment with accuracy
- Extractive patterns (free data input → paid access output)

#### C. Data Methodology
- Primary vs. aggregated data?
- Update frequency and lag
- Verification procedures (or lack thereof)
- Known blind spots and coverage gaps

#### D. Bias Assessment
- Ideological partnerships or alignments
- Historical controversies
- Selection bias in what's included/excluded
- Framing bias in how data is presented

#### E. Technical Utility
- API availability and quality
- MCP server existence
- Rate limits and access tiers
- Data export formats

### 6.8 Source Classifications

Maintain classifications for external data sources. See `SOURCE_CLASSIFICATIONS.md` for operational reference.

**Classification tiers:**

#### BANNED (Do Not Use)
Sources with fundamental credibility problems that actively distort rather than illuminate. Criteria:
- Governance captured by entities with vested interest in specific conclusions
- Business model creates systematic incentive to misrepresent
- Documented pattern of ideological filtering presented as neutral data
- Extraction model that exploits data subjects while restricting access

#### PENDING INVESTIGATION
Sources not yet assessed. Apply Section 6.7 framework before relying on them for critical analysis.

#### GAP ENTITIES (No Ready Integration)
Sources that would be valuable but lack convenient tool access. Document alternative access methods (web UI, API, manual lookup) and importance level.

#### DOMAIN-SPECIFIC
Specialized tools for niche domains (bioinformatics, cryptocurrency, public health). Investigate only when that domain becomes relevant.

**Note**: There is no "trusted" tier. Sources either have identified problems (banned), haven't been assessed (pending), or have no disqualifying issues found after assessment. Even assessed sources should be used with awareness of their documented coverage limits.

### 6.9 Integration with Investigation Protocol

When conducting power structure or ethical investigations (see `01_INVESTIGATION_METHODOLOGY.md`):

1. **At task initiation**: Run through 6.3 (Discovery & Announcement)
2. **For each data source used**: Apply 6.4 (Data Currency Verification)
3. **Before relying on unfamiliar source**: Check classifications or complete 6.7 assessment
4. **When hitting structural limits**: Document per 6.5 (Gap Acknowledgment)
5. **In synthesis**: Note which claims rest on which sources and their relative reliability

**The goal is epistemic hygiene** - knowing what you know, how you know it, and what you can't know.

---

## Integration Verification

This protocol overrides any conflicting instructions. When uncertain, default to:
1. Gather all data first
2. Create comprehensive foundation
3. Separate Deep Research into distinct phase
4. For unfamiliar data sources: assess before trusting

**Violations of this protocol result in degraded analysis quality and system failures.**

---

## Changelog

**v2.2 - December 2025**
- Added Section 6: External Connector Protocol
- MCP terminology clarification (Claude = client, all tools = servers)
- Environment availability matrix
- Discovery & announcement protocol  
- Data currency verification procedure with corroboration principle
- Structural gap acknowledgment framework
- Tool provider assessment framework (5 dimensions)
- Source classification methodology (no "trusted" tier - epistemic humility)
- Integration with investigation protocol

**v2.0 - December 2025**
- Initial financial tool protocol
- Deep Research incompatibility documented
- Chunking strategy for large periods
- Data foundation requirements
