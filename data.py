"""Market data fetching via yfinance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import yfinance as yf


@dataclass
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


def fetch_bars(ticker: str, period: str = "1mo", interval: str = "1d") -> list[Bar]:
    """Fetch historical bars from Yahoo Finance.

    Args:
        ticker: Stock symbol (e.g. "AAPL")
        period: Data period — 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max
        interval: Bar interval — 1m, 5m, 15m, 1h, 1d, 1wk, 1mo

    Returns:
        List of Bar objects, oldest first.
    """
    tk = yf.Ticker(ticker)
    df = tk.history(period=period, interval=interval)

    if df.empty:
        return []

    bars = []
    for ts, row in df.iterrows():
        bars.append(Bar(
            timestamp=ts.to_pydatetime(),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=float(row["Volume"]),
        ))
    return bars


def fetch_options_chain(ticker: str, expiration: str | None = None) -> dict:
    """Fetch options chain from Yahoo Finance.

    Args:
        ticker: Stock symbol
        expiration: Expiration date (YYYY-MM-DD). If None, uses nearest expiration.

    Returns:
        Dict with 'calls', 'puts' (list of dicts), 'expirations' (list of date strings),
        and 'underlying_price'.
    """
    tk = yf.Ticker(ticker)
    expirations = tk.options  # tuple of date strings

    if not expirations:
        return {"calls": [], "puts": [], "expirations": [], "underlying_price": 0}

    exp = expiration if expiration and expiration in expirations else expirations[0]
    chain = tk.option_chain(exp)

    underlying_price = tk.fast_info.get("lastPrice", 0) or 0

    def _safe_int(val, default=0):
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return int(val)

    def _safe_float(val, default=0.0):
        import math
        if val is None or (isinstance(val, float) and math.isnan(val)):
            return default
        return float(val)

    def chain_to_dicts(df) -> list[dict]:
        records = []
        for _, row in df.iterrows():
            records.append({
                "contract": row.get("contractSymbol", ""),
                "strike": _safe_float(row.get("strike", 0)),
                "last": _safe_float(row.get("lastPrice", 0)),
                "bid": _safe_float(row.get("bid", 0)),
                "ask": _safe_float(row.get("ask", 0)),
                "volume": _safe_int(row.get("volume", 0)),
                "open_interest": _safe_int(row.get("openInterest", 0)),
                "iv": _safe_float(row.get("impliedVolatility", 0)),
                "in_the_money": bool(row.get("inTheMoney", False)),
            })
        return records

    return {
        "expiration": exp,
        "expirations": list(expirations),
        "underlying_price": underlying_price,
        "calls": chain_to_dicts(chain.calls),
        "puts": chain_to_dicts(chain.puts),
    }


def fetch_quote(ticker: str) -> dict:
    """Fetch current quote summary for a ticker."""
    tk = yf.Ticker(ticker)
    info = tk.fast_info

    return {
        "ticker": ticker.upper(),
        "price": info.get("lastPrice", 0),
        "open": info.get("open", 0),
        "high": info.get("dayHigh", 0),
        "low": info.get("dayLow", 0),
        "previous_close": info.get("previousClose", 0),
        "volume": info.get("lastVolume", 0),
        "market_cap": info.get("marketCap", 0),
        "fifty_two_week_high": info.get("yearHigh", 0),
        "fifty_two_week_low": info.get("yearLow", 0),
    }
