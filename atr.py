"""ATR — Average True Range using Wilder's smoothing."""

from __future__ import annotations


class ATR:
    def __init__(self, period: int = 14) -> None:
        self.period = period
        self._prev_close: float | None = None
        self._tr_values: list[float] = []
        self._atr: float | None = None
        self._count = 0

    def update(self, high: float, low: float, close: float) -> float | None:
        if self._prev_close is None:
            self._prev_close = close
            return None

        tr = max(
            high - low,
            abs(high - self._prev_close),
            abs(low - self._prev_close),
        )
        self._prev_close = close
        self._count += 1

        if self._count < self.period:
            self._tr_values.append(tr)
            return None

        if self._count == self.period:
            self._tr_values.append(tr)
            self._atr = sum(self._tr_values) / self.period
        else:
            self._atr = (self._atr * (self.period - 1) + tr) / self.period

        return self._atr


def compute_atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> float | None:
    """Compute ATR from lists of high, low, close prices. Returns the latest value."""
    atr = ATR(period)
    result = None
    for h, l, c in zip(highs, lows, closes):
        result = atr.update(h, l, c)
    return result
