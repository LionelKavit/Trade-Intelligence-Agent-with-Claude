"""Trade statistics calculator — KPIs from a list of trade results."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class TradeStatsResult:
    total_trades: int = 0
    wins: int = 0
    losses: int = 0
    win_rate: float = 0.0
    gross_pnl: float = 0.0
    avg_win: float = 0.0
    avg_loss: float = 0.0
    best_trade: float = 0.0
    worst_trade: float = 0.0
    profit_factor: float = 0.0
    expectancy: float = 0.0
    max_drawdown: float = 0.0
    max_drawdown_pct: float = 0.0
    sharpe_ratio: float = 0.0
    max_consecutive_wins: int = 0
    max_consecutive_losses: int = 0
    risk_reward_avg: float = 0.0


def compute_trade_stats(
    pnls: list[float],
    starting_equity: float = 100_000.0,
) -> TradeStatsResult:
    """Compute performance statistics from a list of trade P&Ls.

    Args:
        pnls: List of P&L values per trade (positive = win, negative = loss).
        starting_equity: Starting account equity for drawdown calculation.

    Returns:
        TradeStatsResult with all computed metrics.
    """
    if not pnls:
        return TradeStatsResult()

    wins_list = [p for p in pnls if p > 0]
    losses_list = [p for p in pnls if p <= 0]

    total = len(pnls)
    wins = len(wins_list)
    losses = len(losses_list)
    gross_pnl = sum(pnls)

    avg_win = sum(wins_list) / wins if wins else 0.0
    avg_loss = sum(losses_list) / losses if losses else 0.0

    total_wins = sum(wins_list)
    total_losses = abs(sum(losses_list))
    profit_factor = total_wins / total_losses if total_losses > 0 else float("inf")

    expectancy = gross_pnl / total

    # Max drawdown
    equity = starting_equity
    peak = equity
    max_dd = 0.0
    max_dd_pct = 0.0
    for pnl in pnls:
        equity += pnl
        if equity > peak:
            peak = equity
        dd = peak - equity
        dd_pct = (dd / peak) * 100 if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = dd_pct

    # Sharpe (annualized, assuming daily trades)
    if len(pnls) > 1:
        mean_return = sum(pnls) / len(pnls)
        variance = sum((p - mean_return) ** 2 for p in pnls) / (len(pnls) - 1)
        std_dev = math.sqrt(variance)
        sharpe = (mean_return / std_dev) * math.sqrt(252) if std_dev > 0 else 0.0
    else:
        sharpe = 0.0

    # Consecutive streaks
    max_con_wins = 0
    max_con_losses = 0
    cur_wins = 0
    cur_losses = 0
    for p in pnls:
        if p > 0:
            cur_wins += 1
            cur_losses = 0
            max_con_wins = max(max_con_wins, cur_wins)
        else:
            cur_losses += 1
            cur_wins = 0
            max_con_losses = max(max_con_losses, cur_losses)

    # Average R:R (avg win / abs(avg loss))
    rr_avg = abs(avg_win / avg_loss) if avg_loss != 0 else 0.0

    return TradeStatsResult(
        total_trades=total,
        wins=wins,
        losses=losses,
        win_rate=round((wins / total) * 100, 1),
        gross_pnl=round(gross_pnl, 2),
        avg_win=round(avg_win, 2),
        avg_loss=round(avg_loss, 2),
        best_trade=round(max(pnls), 2),
        worst_trade=round(min(pnls), 2),
        profit_factor=round(profit_factor, 2),
        expectancy=round(expectancy, 2),
        max_drawdown=round(max_dd, 2),
        max_drawdown_pct=round(max_dd_pct, 2),
        sharpe_ratio=round(sharpe, 2),
        max_consecutive_wins=max_con_wins,
        max_consecutive_losses=max_con_losses,
        risk_reward_avg=round(rr_avg, 2),
    )
