#!/usr/bin/env python3
"""
Token Analyzer for Budget-Mode Integration

Analyzes ~/.claude/logs/token-usage.jsonl to provide:
1. Session cost summaries
2. Efficiency metrics (tokens per task type)
3. Action points conversion for TBS interface
4. Historical patterns for budget-conscious decisions
5. Context window % tracking (primary metric for subscription users)

Usage:
    python token-analyzer.py [--summary | --session SESSION_ID | --efficiency | --action-points | --context]
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

TOKEN_LOG_PATH = Path.home() / ".claude" / "logs" / "token-usage.jsonl"

# Action Point conversion rates (for TBS interface metaphor)
# 1 action point ≈ $0.01 USD (adjustable)
ACTION_POINT_RATE = 0.01

# Context window size (Opus 4.5, Sonnet 4.5, Haiku as of 2026-01-18)
CONTEXT_WINDOW = 200000


def parse_log_file(path: Path = TOKEN_LOG_PATH) -> list[dict]:
    """Parse pretty-printed JSON entries from token log."""
    if not path.exists():
        return []

    with open(path, 'r') as f:
        content = f.read()

    entries = []
    decoder = json.JSONDecoder()
    content = content.strip()

    while content:
        try:
            obj, end = decoder.raw_decode(content)
            entries.append(obj)
            content = content[end:].lstrip()
        except json.JSONDecodeError:
            content = content[1:]

    return entries


def normalize_cost(cost_str: str) -> float:
    """Handle cost strings like '.0970905' (missing leading zero)."""
    if not cost_str:
        return 0.0
    if isinstance(cost_str, (int, float)):
        return float(cost_str)
    if cost_str.startswith('.'):
        cost_str = '0' + cost_str
    return float(cost_str)


def get_cost_field(entry: dict) -> str:
    """Get cost from entry, handling both old and new field names."""
    # New format: deprecated_cost_usd, old format: estimated_cost_usd
    return entry.get('deprecated_cost_usd', entry.get('estimated_cost_usd', '0'))


def get_summary(entries: list[dict]) -> dict:
    """Get overall token usage summary."""
    by_tool = defaultdict(lambda: {
        'count': 0,
        'total_cost': 0.0,
        'total_input': 0,
        'total_output': 0,
        'cache_read': 0,
        'cache_creation': 0
    })

    total_cost = 0.0
    sessions = set()

    for e in entries:
        tool = e.get('tool', 'unknown')
        cost = normalize_cost(get_cost_field(e))
        tokens = e.get('tokens', {})

        by_tool[tool]['count'] += 1
        by_tool[tool]['total_cost'] += cost
        by_tool[tool]['total_input'] += tokens.get('input', 0)
        by_tool[tool]['total_output'] += tokens.get('output', 0)
        by_tool[tool]['cache_read'] += tokens.get('cache_read', 0)
        by_tool[tool]['cache_creation'] += tokens.get('cache_creation', 0)

        total_cost += cost
        sessions.add(e.get('session_id', 'unknown'))

    return {
        'total_entries': len(entries),
        'total_cost_usd': total_cost,
        'unique_sessions': len(sessions),
        'by_tool': dict(by_tool),
        'action_points_used': int(total_cost / ACTION_POINT_RATE)
    }


def get_session_stats(entries: list[dict], session_id: str) -> dict:
    """Get stats for a specific session."""
    session_entries = [e for e in entries if e.get('session_id') == session_id]
    return get_summary(session_entries)


def get_efficiency_metrics(entries: list[dict]) -> dict:
    """Calculate efficiency metrics for budget-mode decisions."""
    by_tool = defaultdict(list)

    for e in entries:
        tool = e.get('tool', 'unknown')
        tokens = e.get('tokens', {})
        cost = normalize_cost(get_cost_field(e))

        total_tokens = (tokens.get('input', 0) + tokens.get('output', 0) +
                       tokens.get('cache_read', 0) + tokens.get('cache_creation', 0))

        if total_tokens > 0:
            by_tool[tool].append({
                'tokens': total_tokens,
                'cost': cost,
                'cost_per_1k': (cost / total_tokens) * 1000 if total_tokens > 0 else 0
            })

    metrics = {}
    for tool, data in by_tool.items():
        if data:
            avg_tokens = sum(d['tokens'] for d in data) / len(data)
            avg_cost = sum(d['cost'] for d in data) / len(data)
            metrics[tool] = {
                'call_count': len(data),
                'avg_tokens_per_call': int(avg_tokens),
                'avg_cost_per_call': round(avg_cost, 4),
                'total_tokens': sum(d['tokens'] for d in data),
                'total_cost': round(sum(d['cost'] for d in data), 4)
            }

    return metrics


def get_action_points_status() -> dict:
    """Get current action points status for TBS interface."""
    entries = parse_log_file()
    summary = get_summary(entries)

    # Recent (last 24h) - filter with safe timestamp parsing
    now = datetime.now()
    recent_entries = []
    for e in entries:
        try:
            ts = e.get('timestamp', '')
            if ts:  # Skip entries with missing timestamps
                entry_time = datetime.fromisoformat(ts.replace('Z', '+00:00')).replace(tzinfo=None)
                if entry_time > now - timedelta(days=1):
                    recent_entries.append(e)
        except (ValueError, TypeError):
            # Skip entries with malformed timestamps
            pass
    recent_summary = get_summary(recent_entries)

    return {
        'total_action_points_used': summary['action_points_used'],
        'total_cost_usd': round(summary['total_cost_usd'], 4),
        'last_24h': {
            'action_points': recent_summary['action_points_used'],
            'cost_usd': round(recent_summary['total_cost_usd'], 4),
            'calls': recent_summary['total_entries']
        },
        'rate': f"1 AP = ${ACTION_POINT_RATE}"
    }


def get_context_status(session_id: str = None) -> dict:
    """Get context window usage status - PRIMARY METRIC for subscription users.

    If session_id is provided, returns status for that session.
    Otherwise, returns status for all sessions with the most recent highlighted.
    """
    entries = parse_log_file()

    if not entries:
        return {'error': 'No token usage data found'}

    # Group by session
    sessions = defaultdict(list)
    for e in entries:
        sid = e.get('session_id', 'unknown')
        sessions[sid].append(e)

    if session_id and session_id in sessions:
        # Specific session requested
        session_entries = sessions[session_id]
        latest = session_entries[-1]
        cumulative = latest.get('session_cumulative', {})
        return {
            'session_id': session_id,
            'total_tokens': cumulative.get('total_tokens', 0),
            'context_percent': cumulative.get('context_percent', 0),
            'context_window': CONTEXT_WINDOW,
            'entries': len(session_entries),
            'status': _get_context_warning(cumulative.get('context_percent', 0))
        }

    # Return all sessions with summary
    result = {
        'context_window': CONTEXT_WINDOW,
        'sessions': []
    }

    for sid, session_entries in sorted(sessions.items(), key=lambda x: x[1][-1].get('timestamp', ''), reverse=True):
        latest = session_entries[-1]
        cumulative = latest.get('session_cumulative', {})
        pct = cumulative.get('context_percent', 0)
        result['sessions'].append({
            'session_id': sid[:16] + '...' if len(sid) > 16 else sid,
            'full_id': sid,
            'context_percent': pct,
            'total_tokens': cumulative.get('total_tokens', 0),
            'entries': len(session_entries),
            'status': _get_context_warning(pct)
        })

    # Highlight most recent
    if result['sessions']:
        result['current'] = result['sessions'][0]

    return result


def _get_context_warning(percent: float) -> str:
    """Get status message based on context % used."""
    if percent >= 80:
        return "⚠️ CRITICAL - Approaching context limit!"
    elif percent >= 60:
        return "⚡ HIGH - Consider wrapping up soon"
    elif percent >= 40:
        return "📊 MODERATE - Good headroom remaining"
    else:
        return "✅ LOW - Plenty of context available"


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Token usage analyzer for budget-mode')
    parser.add_argument('--summary', action='store_true', help='Show overall summary')
    parser.add_argument('--session', type=str, help='Show stats for specific session')
    parser.add_argument('--context', action='store_true', help='Show context % status (PRIMARY for subscription users)')
    parser.add_argument('--efficiency', action='store_true', help='Show efficiency metrics')
    parser.add_argument('--action-points', action='store_true', help='Show action points status')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    entries = parse_log_file()

    if not entries:
        print("No token usage data found.")
        return

    if args.context:
        data = get_context_status(args.session)  # Can combine with --session
    elif args.session:
        data = get_session_stats(entries, args.session)
    elif args.efficiency:
        data = get_efficiency_metrics(entries)
    elif args.action_points:
        data = get_action_points_status()
    else:
        data = get_summary(entries)

    # Always output JSON (--json flag is for consistency, both formats are JSON)
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
