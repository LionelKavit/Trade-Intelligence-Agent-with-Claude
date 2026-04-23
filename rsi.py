"""RSI — Relative Strength Index using Wilder's smoothing."""

from __future__ import annotations


class RSI:
    def __init__(self, period: int = 14) -> None:
        self.period = period
        self._gains: list[float] = []
        self._losses: list[float] = []
        self._avg_gain: float | None = None
        self._avg_loss: float | None = None
        self._prev_close: float | None = None
        self._count = 0

    def update(self, close: float) -> float | None:
        if self._prev_close is None:
            self._prev_close = close
            return None

        change = close - self._prev_close
        self._prev_close = close
        gain = max(change, 0.0)
        loss = abs(min(change, 0.0))
        self._count += 1

        if self._count < self.period:
            self._gains.append(gain)
            self._losses.append(loss)
            return None

        if self._count == self.period:
            self._gains.append(gain)
            self._losses.append(loss)
            self._avg_gain = sum(self._gains) / self.period
            self._avg_loss = sum(self._losses) / self.period
        else:
            self._avg_gain = (self._avg_gain * (self.period - 1) + gain) / self.period
            self._avg_loss = (self._avg_loss * (self.period - 1) + loss) / self.period

        if self._avg_loss == 0:
            return 100.0
        rs = self._avg_gain / self._avg_loss
        return 100.0 - (100.0 / (1.0 + rs))


def compute_rsi(closes: list[float], period: int = 14) -> float | None:
    """Compute RSI from a list of closing prices. Returns the latest value."""
    rsi = RSI(period)
    result = None
    for close in closes:
        result = rsi.update(close)
    return result
