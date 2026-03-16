#!/usr/bin/env python3
"""
FRED Data Fetcher - Free public data from Federal Reserve Economic Data

No API key required for basic CSV downloads.

Commonly used series:
- DGS10: 10-Year Treasury Constant Maturity Rate
- DTWEXBGS: Nominal Broad U.S. Dollar Index
- GOLDAMGBD228NLBM: Gold Fixing Price (London PM)
- T10Y2Y: 10-Year Treasury Minus 2-Year Treasury (yield curve)
"""

from __future__ import annotations
import urllib.request
import csv
from datetime import datetime, timedelta
from io import StringIO
from typing import Optional


# Common macro series for quick reference
MACRO_SERIES = {
    "DGS10": "10-Year Treasury Yield",
    "DTWEXBGS": "Broad Dollar Index",
    "GOLDAMGBD228NLBM": "Gold Price (London PM)",
    "T10Y2Y": "10Y-2Y Yield Spread",
    "VIXCLS": "VIX Volatility Index",
    "FEDFUNDS": "Federal Funds Rate",
}


def fetch_fred_series(
    series_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    last_n_days: int = 30,
) -> list[dict]:
    """
    Fetch data from FRED for a given series.

    Args:
        series_id: FRED series identifier (e.g., 'DGS10')
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        last_n_days: If no dates provided, fetch last N days (default 30)

    Returns:
        List of dicts with 'date' and 'value' keys
    """
    # Build URL
    base_url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"

    if start_date:
        base_url += f"&cosd={start_date}"
    else:
        # Default to last N days
        start = (datetime.now() - timedelta(days=last_n_days)).strftime("%Y-%m-%d")
        base_url += f"&cosd={start}"

    if end_date:
        base_url += f"&coed={end_date}"

    try:
        with urllib.request.urlopen(base_url, timeout=10) as response:
            data = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        print(f"Error fetching {series_id}: {e}")
        return []

    # Parse CSV
    results = []
    reader = csv.DictReader(StringIO(data))
    for row in reader:
        date = row.get('DATE', row.get('date', ''))
        value = row.get(series_id, row.get('value', ''))

        # Skip missing values (FRED uses '.' for missing)
        if value and value != '.':
            try:
                results.append({
                    'date': date,
                    'value': float(value)
                })
            except ValueError:
                pass

    return results


def get_latest(series_id: str) -> Optional[dict]:
    """Get the most recent value for a series."""
    data = fetch_fred_series(series_id, last_n_days=14)
    return data[-1] if data else None


def check_divergence(yields_series: str = "DGS10", dollar_series: str = "DTWEXBGS", days: int = 5) -> dict:
    """
    Check for yield-dollar divergence pattern.

    Normal: Yields up → Dollar up
    Red flag: Yields up + Dollar down (or vice versa)

    Returns dict with analysis.
    """
    yields_data = fetch_fred_series(yields_series, last_n_days=days + 5)
    dollar_data = fetch_fred_series(dollar_series, last_n_days=days + 5)

    if len(yields_data) < 2 or len(dollar_data) < 2:
        return {"error": "Insufficient data"}

    # Calculate changes
    yield_change = yields_data[-1]['value'] - yields_data[-days]['value'] if len(yields_data) > days else 0
    dollar_change = dollar_data[-1]['value'] - dollar_data[-days]['value'] if len(dollar_data) > days else 0

    # Determine pattern
    yield_direction = "up" if yield_change > 0.05 else ("down" if yield_change < -0.05 else "flat")
    dollar_direction = "up" if dollar_change > 0.5 else ("down" if dollar_change < -0.5 else "flat")

    # Check for divergence
    divergence = False
    if yield_direction == "up" and dollar_direction == "down":
        divergence = True
        interpretation = "RED FLAG: Yields rising but dollar falling - potential foreign selling / confidence crisis"
    elif yield_direction == "down" and dollar_direction == "down":
        divergence = True
        interpretation = "WARNING: Both falling - flight from US assets"
    elif yield_direction == "up" and dollar_direction == "up":
        interpretation = "Normal: Higher rates attracting capital"
    else:
        interpretation = "Stable or mixed signals"

    return {
        "period_days": days,
        "yield_latest": yields_data[-1]['value'],
        "yield_change": round(yield_change, 3),
        "yield_direction": yield_direction,
        "dollar_latest": dollar_data[-1]['value'],
        "dollar_change": round(dollar_change, 2),
        "dollar_direction": dollar_direction,
        "divergence_detected": divergence,
        "interpretation": interpretation,
        "as_of": yields_data[-1]['date']
    }


def macro_snapshot() -> dict:
    """Get a quick snapshot of key macro indicators."""
    snapshot = {}

    for series_id, name in MACRO_SERIES.items():
        latest = get_latest(series_id)
        if latest:
            snapshot[series_id] = {
                "name": name,
                "value": latest['value'],
                "date": latest['date']
            }
        else:
            snapshot[series_id] = {"name": name, "error": "Failed to fetch"}

    # Add divergence check
    snapshot["divergence_analysis"] = check_divergence()

    return snapshot


def main():
    """CLI interface for quick checks."""
    import sys
    import json

    if len(sys.argv) < 2:
        print("FRED Data Fetcher - Free macro data")
        print("\nUsage:")
        print("  python fred_fetcher.py <series_id>     # Get latest value")
        print("  python fred_fetcher.py snapshot        # Quick macro snapshot")
        print("  python fred_fetcher.py divergence      # Check yield-dollar divergence")
        print("\nCommon series:")
        for sid, name in MACRO_SERIES.items():
            print(f"  {sid}: {name}")
        return

    cmd = sys.argv[1].upper()

    if cmd == "SNAPSHOT":
        result = macro_snapshot()
        print(json.dumps(result, indent=2))
    elif cmd == "DIVERGENCE":
        result = check_divergence()
        print(json.dumps(result, indent=2))
    else:
        # Treat as series ID
        latest = get_latest(cmd)
        if latest:
            name = MACRO_SERIES.get(cmd, cmd)
            print(f"{name}")
            print(f"  Value: {latest['value']}")
            print(f"  Date:  {latest['date']}")
        else:
            print(f"No data found for series: {cmd}")


if __name__ == "__main__":
    main()
