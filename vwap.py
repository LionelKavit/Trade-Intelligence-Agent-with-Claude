"""VWAP — Volume Weighted Average Price (intraday, resets daily)."""

from __future__ import annotations

from datetime import date, datetime


class VWAP:
    def __init__(self) -> None:
        self._cum_volume = 0.0
        self._cum_tp_volume = 0.0
        self._current_date: date | None = None
        self._value: float | None = None

    def update(self, high: float, low: float, close: float, volume: float, timestamp: datetime | None = None) -> float | None:
        if timestamp is not None:
            bar_date = timestamp.date()
            if self._current_date is not None and bar_date != self._current_date:
                self._cum_volume = 0.0
                self._cum_tp_volume = 0.0
            self._current_date = bar_date

        tp = (high + low + close) / 3.0
        self._cum_tp_volume += tp * volume
        self._cum_volume += volume

        if self._cum_volume == 0:
            return None

        self._value = self._cum_tp_volume / self._cum_volume
        return self._value
