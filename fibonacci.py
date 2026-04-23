"""Fibonacci retracement — swing detection + fib levels + golden pocket."""

from __future__ import annotations

from dataclasses import dataclass

FIB_RATIOS = [0.236, 0.382, 0.5, 0.618, 0.65, 0.786, 1.0]


@dataclass
class FibResult:
    swing_high: float
    swing_low: float
    levels: dict[float, float]
    in_golden_pocket: bool
    direction: str  # "up" or "down"


class Fibonacci:
    def __init__(
        self,
        swing_lookback: int = 50,
        golden_pocket_low: float = 0.618,
        golden_pocket_high: float = 0.65,
    ) -> None:
        self.swing_lookback = swing_lookback
        self.golden_pocket_low = golden_pocket_low
        self.golden_pocket_high = golden_pocket_high

    def compute(self, highs: list[float], lows: list[float], closes: list[float]) -> FibResult | None:
        if len(highs) < self.swing_lookback:
            return None

        window_h = highs[-self.swing_lookback:]
        window_l = lows[-self.swing_lookback:]

        swing_high = max(window_h)
        swing_low = min(window_l)
        high_idx = window_h.index(swing_high)
        low_idx = window_l.index(swing_low)

        if swing_high == swing_low:
            return None

        diff = swing_high - swing_low

        if high_idx > low_idx:
            direction = "up"
            levels = {r: swing_high - r * diff for r in FIB_RATIOS}
        else:
            direction = "down"
            levels = {r: swing_low + r * diff for r in FIB_RATIOS}

        current_price = closes[-1]
        gp_low_price = levels.get(self.golden_pocket_low, 0)
        gp_high_price = levels.get(self.golden_pocket_high, 0)
        in_golden_pocket = min(gp_low_price, gp_high_price) <= current_price <= max(gp_low_price, gp_high_price)

        return FibResult(
            swing_high=swing_high,
            swing_low=swing_low,
            levels=levels,
            in_golden_pocket=in_golden_pocket,
            direction=direction,
        )
