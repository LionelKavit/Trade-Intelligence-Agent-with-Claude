"""EMA — Exponential Moving Average."""

from __future__ import annotations


class EMA:
    def __init__(self, period: int) -> None:
        self.period = period
        self._multiplier = 2.0 / (period + 1)
        self._value: float | None = None
        self._count = 0
        self._sum = 0.0

    def update(self, close: float) -> float | None:
        self._count += 1

        if self._count < self.period:
            self._sum += close
            return None

        if self._count == self.period:
            self._sum += close
            self._value = self._sum / self.period
            return self._value

        self._value = close * self._multiplier + self._value * (1 - self._multiplier)
        return self._value


def compute_ema(closes: list[float], period: int = 20) -> float | None:
    """Compute EMA from a list of closing prices. Returns the latest value."""
    ema = EMA(period)
    result = None
    for close in closes:
        result = ema.update(close)
    return result
