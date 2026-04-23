"""MACD — Moving Average Convergence Divergence."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MACDResult:
    macd_line: float
    signal_line: float
    histogram: float


class MACD:
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9) -> None:
        self.fast = fast
        self.slow = slow
        self.signal_period = signal
        self._ema_fast: float | None = None
        self._ema_slow: float | None = None
        self._ema_signal: float | None = None
        self._count = 0
        self._fast_mult = 2.0 / (fast + 1)
        self._slow_mult = 2.0 / (slow + 1)
        self._signal_mult = 2.0 / (signal + 1)

    def update(self, close: float) -> MACDResult | None:
        self._count += 1

        if self._ema_fast is None:
            self._ema_fast = close
            self._ema_slow = close
            return None

        self._ema_fast = close * self._fast_mult + self._ema_fast * (1 - self._fast_mult)
        self._ema_slow = close * self._slow_mult + self._ema_slow * (1 - self._slow_mult)

        if self._count < self.slow:
            return None

        macd_line = self._ema_fast - self._ema_slow

        if self._ema_signal is None:
            self._ema_signal = macd_line
        else:
            self._ema_signal = macd_line * self._signal_mult + self._ema_signal * (1 - self._signal_mult)

        histogram = macd_line - self._ema_signal
        return MACDResult(macd_line=macd_line, signal_line=self._ema_signal, histogram=histogram)


def compute_macd(closes: list[float], fast: int = 12, slow: int = 26, signal: int = 9) -> MACDResult | None:
    """Compute MACD from a list of closing prices. Returns the latest value."""
    macd = MACD(fast, slow, signal)
    result = None
    for close in closes:
        result = macd.update(close)
    return result
