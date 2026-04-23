"""Position sizing and risk/reward calculator."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PositionPlan:
    ticker: str
    direction: str  # "long" or "short"
    entry_price: float
    stop_price: float
    target_price: float
    shares: int
    position_value: float
    risk_per_share: float
    reward_per_share: float
    total_risk: float
    total_reward: float
    risk_reward_ratio: float
    risk_pct_of_account: float


def calculate_position(
    ticker: str,
    entry_price: float,
    stop_price: float,
    target_price: float,
    account_size: float,
    risk_pct: float = 1.5,
) -> PositionPlan:
    """Calculate position size based on risk percentage of account.

    Args:
        ticker: Stock symbol
        entry_price: Planned entry price
        stop_price: Stop loss price
        target_price: Profit target price
        account_size: Total account equity
        risk_pct: Max risk as percentage of account (default 1.5%)

    Returns:
        PositionPlan with shares, risk, reward, and R:R ratio.
    """
    direction = "long" if entry_price < target_price else "short"
    risk_per_share = abs(entry_price - stop_price)
    reward_per_share = abs(target_price - entry_price)

    if risk_per_share == 0:
        risk_per_share = 0.01

    max_risk_dollars = account_size * (risk_pct / 100.0)
    shares = int(max_risk_dollars / risk_per_share)
    shares = max(shares, 1)

    total_risk = risk_per_share * shares
    total_reward = reward_per_share * shares
    rr_ratio = reward_per_share / risk_per_share if risk_per_share > 0 else 0

    return PositionPlan(
        ticker=ticker.upper(),
        direction=direction,
        entry_price=entry_price,
        stop_price=stop_price,
        target_price=target_price,
        shares=shares,
        position_value=entry_price * shares,
        risk_per_share=risk_per_share,
        reward_per_share=reward_per_share,
        total_risk=total_risk,
        total_reward=total_reward,
        risk_reward_ratio=round(rr_ratio, 2),
        risk_pct_of_account=round((total_risk / account_size) * 100, 2),
    )


def atr_based_position(
    ticker: str,
    entry_price: float,
    atr: float,
    account_size: float,
    risk_pct: float = 1.5,
    stop_atr_mult: float = 2.0,
    target_atr_mult: float = 3.0,
    direction: str = "long",
) -> PositionPlan:
    """Calculate position using ATR for stop and target distances.

    Args:
        ticker: Stock symbol
        entry_price: Planned entry price
        atr: Current ATR value
        account_size: Total account equity
        risk_pct: Max risk as percentage of account
        stop_atr_mult: ATR multiplier for stop distance (default 2.0)
        target_atr_mult: ATR multiplier for target distance (default 3.0)
        direction: "long" or "short"
    """
    if direction == "long":
        stop_price = entry_price - (atr * stop_atr_mult)
        target_price = entry_price + (atr * target_atr_mult)
    else:
        stop_price = entry_price + (atr * stop_atr_mult)
        target_price = entry_price - (atr * target_atr_mult)

    return calculate_position(
        ticker=ticker,
        entry_price=entry_price,
        stop_price=stop_price,
        target_price=target_price,
        account_size=account_size,
        risk_pct=risk_pct,
    )
