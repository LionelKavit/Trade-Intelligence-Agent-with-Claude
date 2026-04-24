"""Fundamental analysis - extract metrics from financial statements."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional

import yfinance as yf


@dataclass
class FinancialMetrics:
    """Core financial metrics and ratios."""
    # Valuation
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    
    # Profitability
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    roe: Optional[float] = None  # Return on Equity
    roa: Optional[float] = None  # Return on Assets
    roic: Optional[float] = None  # Return on Invested Capital
    
    # Growth
    revenue_growth: Optional[float] = None  # YoY
    earnings_growth: Optional[float] = None  # YoY
    eps_growth: Optional[float] = None  # YoY
    
    # Debt & Liquidity
    debt_to_equity: Optional[float] = None
    debt_to_assets: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    debt_to_ebitda: Optional[float] = None
    
    # Other
    book_value_per_share: Optional[float] = None
    price_to_book: Optional[float] = None
    free_cash_flow: Optional[float] = None
    fcf_to_net_income: Optional[float] = None


@dataclass
class CompanyHealth:
    """Overall company health assessment."""
    health_score: float  # 0-100
    debt_level: str  # "low", "moderate", "high"
    liquidity: str  # "strong", "adequate", "weak"
    profitability: str  # "strong", "moderate", "weak"
    growth_trend: str  # "positive", "neutral", "negative"
    valuation: str  # "undervalued", "fairly_valued", "overvalued"
    summary: str


class FundamentalAnalyzer:
    """Analyze fundamental metrics of companies."""
    
    def __init__(self):
        pass
    
    def get_financial_metrics(self, ticker: str) -> FinancialMetrics:
        """Extract financial metrics for a ticker.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            FinancialMetrics object with extracted metrics
        """
        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info or {}
            
            # Get quarterly financials for growth calculations
            quarterly = stock.quarterly_financials
            annual = stock.financials
            
            metrics = FinancialMetrics()
            
            # Valuation metrics
            metrics.pe_ratio = info.get('trailingPE')
            metrics.pb_ratio = info.get('priceToBook')
            metrics.peg_ratio = info.get('pegRatio')
            metrics.ps_ratio = info.get('priceToSalesTrailing12Months')
            
            # Profitability
            metrics.profit_margin = info.get('profitMargins')
            metrics.operating_margin = info.get('operatingMargins')
            metrics.roe = info.get('returnOnEquity')
            metrics.roa = info.get('returnOnAssets')
            metrics.roic = info.get('roic')
            
            # Debt & Liquidity
            metrics.debt_to_equity = info.get('debtToEquity')
            metrics.current_ratio = info.get('currentRatio')
            metrics.quick_ratio = info.get('quickRatio')
            
            # Per share metrics
            metrics.book_value_per_share = info.get('bookValue')
            metrics.price_to_book = info.get('priceToBook')
            
            # Cash flow
            metrics.free_cash_flow = info.get('freeCashflow')
            
            # Calculate growth rates from historical data
            if not quarterly.empty:
                try:
                    # Revenue growth
                    if 'Total Revenue' in quarterly.index:
                        latest = quarterly.loc['Total Revenue'].iloc[0] if len(quarterly.columns) > 0 else None
                        year_ago = quarterly.loc['Total Revenue'].iloc[4] if len(quarterly.columns) > 4 else None
                        if latest and year_ago and year_ago != 0:
                            metrics.revenue_growth = (latest - year_ago) / year_ago
                    
                    # Net income growth
                    if 'Net Income' in quarterly.index:
                        latest = quarterly.loc['Net Income'].iloc[0] if len(quarterly.columns) > 0 else None
                        year_ago = quarterly.loc['Net Income'].iloc[4] if len(quarterly.columns) > 4 else None
                        if latest and year_ago and year_ago != 0:
                            metrics.earnings_growth = (latest - year_ago) / year_ago
                except:
                    pass
            
            return metrics
        
        except Exception as e:
            print(f"Error fetching financial metrics for {ticker}: {e}")
            return FinancialMetrics()
    
    def assess_health(self, ticker: str, metrics: Optional[FinancialMetrics] = None) -> CompanyHealth:
        """Assess overall company health.
        
        Args:
            ticker: Stock symbol
            metrics: FinancialMetrics object (fetches if None)
            
        Returns:
            CompanyHealth assessment
        """
        if metrics is None:
            metrics = self.get_financial_metrics(ticker)
        
        scores = []
        
        # Debt assessment (lower is better)
        if metrics.debt_to_equity is not None:
            if metrics.debt_to_equity < 0.5:
                debt_level = "low"
                scores.append(25)
            elif metrics.debt_to_equity < 1.5:
                debt_level = "moderate"
                scores.append(15)
            else:
                debt_level = "high"
                scores.append(5)
        else:
            debt_level = "unknown"
        
        # Liquidity assessment (higher is better)
        if metrics.current_ratio is not None:
            if metrics.current_ratio > 1.5:
                liquidity = "strong"
                scores.append(25)
            elif metrics.current_ratio > 1.0:
                liquidity = "adequate"
                scores.append(15)
            else:
                liquidity = "weak"
                scores.append(5)
        else:
            liquidity = "unknown"
        
        # Profitability assessment
        if metrics.roe is not None:
            if metrics.roe > 0.15:
                profitability = "strong"
                scores.append(25)
            elif metrics.roe > 0.05:
                profitability = "moderate"
                scores.append(15)
            else:
                profitability = "weak"
                scores.append(5)
        elif metrics.profit_margin is not None:
            if metrics.profit_margin > 0.15:
                profitability = "strong"
                scores.append(25)
            elif metrics.profit_margin > 0.05:
                profitability = "moderate"
                scores.append(15)
            else:
                profitability = "weak"
                scores.append(5)
        else:
            profitability = "unknown"
        
        # Growth assessment
        if metrics.revenue_growth is not None or metrics.earnings_growth is not None:
            growth_rate = metrics.revenue_growth or metrics.earnings_growth or 0
            if growth_rate > 0.15:
                growth_trend = "positive"
                scores.append(15)
            elif growth_rate > -0.05:
                growth_trend = "neutral"
                scores.append(10)
            else:
                growth_trend = "negative"
                scores.append(3)
        else:
            growth_trend = "unknown"
        
        # Valuation assessment
        if metrics.pe_ratio is not None:
            if metrics.pe_ratio < 15:
                valuation = "undervalued"
                scores.append(10)
            elif metrics.pe_ratio < 25:
                valuation = "fairly_valued"
                scores.append(7)
            else:
                valuation = "overvalued"
                scores.append(3)
        else:
            valuation = "unknown"
        
        # Calculate overall health score
        health_score = sum(scores) / len(scores) if scores else 50
        
        # Generate summary
        summary = f"Company shows {profitability} profitability with {debt_level} debt levels. "
        summary += f"Liquidity is {liquidity}. Growth trend is {growth_trend}. "
        summary += f"Valuation is {valuation}."
        
        return CompanyHealth(
            health_score=health_score,
            debt_level=debt_level,
            liquidity=liquidity,
            profitability=profitability,
            growth_trend=growth_trend,
            valuation=valuation,
            summary=summary
        )
    
    def get_summary_dict(self, ticker: str) -> dict:
        """Get complete fundamental analysis as dictionary.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary with all fundamental data
        """
        metrics = self.get_financial_metrics(ticker)
        health = self.assess_health(ticker, metrics)
        
        # Filter out None values
        metrics_dict = {k: v for k, v in asdict(metrics).items() if v is not None}
        
        return {
            "ticker": ticker.upper(),
            "metrics": {k: round(v, 4) if isinstance(v, float) else v for k, v in metrics_dict.items()},
            "health": {
                "score": round(health.health_score, 1),
                "debt_level": health.debt_level,
                "liquidity": health.liquidity,
                "profitability": health.profitability,
                "growth_trend": health.growth_trend,
                "valuation": health.valuation,
                "summary": health.summary
            }
        }
