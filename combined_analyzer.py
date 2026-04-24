"""Combined technical and fundamental analysis."""

from __future__ import annotations

import json
from typing import Optional

from fintools_mcp.data import fetch_bars
from fintools_mcp.indicators.rsi import compute_rsi
from fintools_mcp.indicators.macd import compute_macd
from fintools_mcp.indicators.ema import compute_ema
from fintools_mcp.indicators.atr import compute_atr
from fintools_mcp.sec_filings import SECFilingsFetcher
from fintools_mcp.sec_fundamental import FundamentalAnalyzer


class CombinedAnalyzer:
    """Combined technical and fundamental analysis."""
    
    def __init__(self):
        self.sec_fetcher = SECFilingsFetcher()
        self.fundamental_analyzer = FundamentalAnalyzer()
    
    def analyze(self, ticker: str, period: str = "3mo") -> dict:
        """Perform combined technical + fundamental analysis.
        
        Args:
            ticker: Stock symbol
            period: Data period for technical indicators
            
        Returns:
            Dictionary with combined analysis
        """
        ticker = ticker.upper()
        
        # Get technical analysis
        technical = self._get_technical(ticker, period)
        
        # Get fundamental analysis
        fundamental = self._get_fundamental(ticker)
        
        # Get filings summary
        filings = self._get_filings(ticker)
        
        # Generate combined signal
        signal = self._generate_signal(technical, fundamental)
        
        return {
            "ticker": ticker,
            "analysis_date": self._get_date(),
            "technical": technical,
            "fundamental": fundamental,
            "filings": filings,
            "combined_signal": signal,
            "recommendation": signal["recommendation"]
        }
    
    def _get_technical(self, ticker: str, period: str) -> dict:
        """Get technical analysis data."""
        try:
            bars = fetch_bars(ticker, period=period, interval="1d")
            if not bars:
                return {"status": "no_data"}
            
            closes = [b.close for b in bars]
            highs = [b.high for b in bars]
            lows = [b.low for b in bars]
            
            rsi = compute_rsi(closes)
            macd = compute_macd(closes)
            atr = compute_atr(highs, lows, closes)
            ema_9 = compute_ema(closes, 9)
            ema_21 = compute_ema(closes, 21)
            ema_50 = compute_ema(closes, 50)
            ema_200 = compute_ema(closes, 200)
            
            current = bars[-1]
            
            # Assess trend
            trend = "neutral"
            if ema_9 and ema_21 and ema_50 and ema_200:
                if ema_9 > ema_21 > ema_50 > ema_200:
                    trend = "strong_bullish"
                elif ema_9 > ema_21 > ema_50:
                    trend = "bullish"
                elif ema_9 < ema_21 < ema_50 < ema_200:
                    trend = "strong_bearish"
                elif ema_9 < ema_21 < ema_50:
                    trend = "bearish"
            
            return {
                "status": "success",
                "price": round(current.close, 2),
                "rsi": round(rsi, 2) if rsi else None,
                "macd": {
                    "value": round(macd.macd_line, 4) if macd else None,
                    "signal": round(macd.signal_line, 4) if macd else None,
                    "histogram": round(macd.histogram, 4) if macd else None,
                },
                "atr": round(atr, 2) if atr else None,
                "ema": {
                    "ema_9": round(ema_9, 2) if ema_9 else None,
                    "ema_21": round(ema_21, 2) if ema_21 else None,
                    "ema_50": round(ema_50, 2) if ema_50 else None,
                    "ema_200": round(ema_200, 2) if ema_200 else None,
                },
                "trend": trend,
                "bars_analyzed": len(bars)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _get_fundamental(self, ticker: str) -> dict:
        """Get fundamental analysis data."""
        try:
            return self.fundamental_analyzer.get_summary_dict(ticker)
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _get_filings(self, ticker: str) -> dict:
        """Get recent SEC filings."""
        try:
            return self.sec_fetcher.get_filings_summary(ticker)
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _generate_signal(self, technical: dict, fundamental: dict) -> dict:
        """Generate combined buy/hold/sell signal.
        
        Args:
            technical: Technical analysis data
            fundamental: Fundamental analysis data
            
        Returns:
            Signal with recommendation and reasoning
        """
        signals = []
        confidence = 0
        
        # Technical signals
        if technical.get("status") == "success":
            trend = technical.get("trend", "neutral")
            rsi = technical.get("rsi")
            
            if trend == "strong_bullish":
                signals.append("strong_technical_uptrend")
                confidence += 30
            elif trend == "bullish":
                signals.append("technical_uptrend")
                confidence += 20
            elif trend == "strong_bearish":
                signals.append("strong_technical_downtrend")
                confidence -= 30
            elif trend == "bearish":
                signals.append("technical_downtrend")
                confidence -= 20
            
            if rsi and rsi < 30:
                signals.append("technically_oversold")
                confidence += 10
            elif rsi and rsi > 70:
                signals.append("technically_overbought")
                confidence -= 10
        
        # Fundamental signals
        if fundamental.get("status") == "success":
            health = fundamental.get("health", {})
            health_score = health.get("score", 50)
            valuation = health.get("valuation", "unknown")
            debt_level = health.get("debt_level", "unknown")
            
            if health_score > 70:
                signals.append("fundamentally_strong")
                confidence += 25
            elif health_score < 40:
                signals.append("fundamentally_weak")
                confidence -= 25
            
            if valuation == "undervalued":
                signals.append("undervalued")
                confidence += 15
            elif valuation == "overvalued":
                signals.append("overvalued")
                confidence -= 15
            
            if debt_level == "high":
                confidence -= 10
            elif debt_level == "low":
                confidence += 5
        
        # Generate recommendation
        if confidence >= 40:
            recommendation = "BUY"
            reasoning = "Strong positive signals from both technical and fundamental analysis"
        elif confidence >= 15:
            recommendation = "BUY"
            reasoning = "Positive signals outweigh concerns"
        elif confidence >= -15:
            recommendation = "HOLD"
            reasoning = "Mixed signals - wait for clearer direction"
        elif confidence >= -40:
            recommendation = "SELL"
            reasoning = "Negative signals outweigh positive factors"
        else:
            recommendation = "SELL"
            reasoning = "Strong negative signals from both analyses"
        
        return {
            "recommendation": recommendation,
            "confidence": max(-100, min(100, confidence)),
            "signals": signals,
            "reasoning": reasoning
        }
    
    def _get_date(self) -> str:
        """Get current date in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
