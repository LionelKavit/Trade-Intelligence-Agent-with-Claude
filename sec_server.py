"""SEC EDGAR MCP Server - Standalone MCP server for SEC filings and fundamental analysis."""

from __future__ import annotations

import json
import sys

from mcp.server.fastmcp import FastMCP

from fintools_mcp.sec_filings import SECFilingsFetcher
from fintools_mcp.sec_fundamental import FundamentalAnalyzer
from fintools_mcp.combined_analyzer import CombinedAnalyzer


# Initialize MCP server
mcp = FastMCP(
    "sec-filings",
    instructions="SEC EDGAR filings and fundamental analysis tools — technical + fundamental combined analysis",
)

# Initialize analyzers
sec_fetcher = SECFilingsFetcher()
fundamental_analyzer = FundamentalAnalyzer()
combined_analyzer = CombinedAnalyzer()


# ============================================================================
# Tool 1: Get Recent SEC Filings
# ============================================================================

@mcp.tool()
def get_recent_filings(
    ticker: str,
    filing_types: str = "10-K,10-Q,8-K",
) -> str:
    """Get recent SEC EDGAR filings for a company.

    Args:
        ticker: Stock symbol (e.g., AAPL, MSFT)
        filing_types: Comma-separated list of form types (e.g., 10-K,10-Q,8-K)

    Returns:
        JSON string with filing summary
    """
    types = [t.strip() for t in filing_types.split(",")]
    
    filings_summary = sec_fetcher.get_filings_summary(ticker)
    
    return json.dumps(filings_summary, indent=2)


# ============================================================================
# Tool 2: Get Fundamental Metrics
# ============================================================================

@mcp.tool()
def get_fundamental_metrics(ticker: str) -> str:
    """Get fundamental financial metrics and company health assessment.

    Args:
        ticker: Stock symbol (e.g., AAPL, MSFT)

    Returns:
        JSON string with financial ratios and health score
    """
    metrics = fundamental_analyzer.get_summary_dict(ticker)
    
    return json.dumps(metrics, indent=2)


# ============================================================================
# Tool 3: Combined Analysis (Technical + Fundamental)
# ============================================================================

@mcp.tool()
def get_combined_analysis(
    ticker: str,
    period: str = "3mo",
) -> str:
    """Get combined technical and fundamental analysis with buy/hold/sell recommendation.

    Args:
        ticker: Stock symbol (e.g., AAPL, MSFT)
        period: Data period for technical indicators (1mo, 3mo, 6mo, 1y)

    Returns:
        JSON string with combined analysis and recommendation
    """
    analysis = combined_analyzer.analyze(ticker, period=period)
    
    return json.dumps(analysis, indent=2)


# ============================================================================
# Tool 4: Compare Fundamentals
# ============================================================================

@mcp.tool()
def compare_fundamentals(tickers: str) -> str:
    """Compare fundamental metrics across multiple stocks.

    Args:
        tickers: Comma-separated stock symbols (e.g., AAPL,MSFT,GOOGL)

    Returns:
        JSON string with side-by-side fundamental comparison
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",")]
    
    comparison = {
        "tickers": ticker_list,
        "analysis": {}
    }
    
    for ticker in ticker_list:
        try:
            analysis = combined_analyzer.analyze(ticker)
            
            # Extract key metrics
            fundamental = analysis.get("fundamental", {})
            technical = analysis.get("technical", {})
            signal = analysis.get("combined_signal", {})
            
            comparison["analysis"][ticker] = {
                "price": technical.get("price"),
                "technical_trend": technical.get("trend"),
                "health_score": fundamental.get("health", {}).get("score"),
                "valuation": fundamental.get("health", {}).get("valuation"),
                "debt_level": fundamental.get("health", {}).get("debt_level"),
                "recommendation": signal.get("recommendation"),
                "confidence": signal.get("confidence")
            }
        except Exception as e:
            comparison["analysis"][ticker] = {"error": str(e)}
    
    return json.dumps(comparison, indent=2)


# ============================================================================
# Tool 5: Get Filing Details
# ============================================================================

@mcp.tool()
def get_filing_details(ticker: str, max_results: int = 5) -> str:
    """Get detailed SEC filing information.

    Args:
        ticker: Stock symbol
        max_results: Maximum number of recent filings to retrieve

    Returns:
        JSON string with filing details and URLs
    """
    filings = sec_fetcher.get_recent_filings(ticker, max_results=max_results)
    
    result = {
        "ticker": ticker.upper(),
        "total_filings": len(filings),
        "filings": [
            {
                "form_type": f.form_type,
                "filed_date": f.filed_date,
                "fiscal_period_end": f.fiscal_period_end,
                "company_name": f.company_name,
                "url": f.filing_url,
                "accession_number": f.accession_number
            }
            for f in filings
        ]
    }
    
    return json.dumps(result, indent=2)


# ============================================================================
# Tool 6: Quick Analysis Summary
# ============================================================================

@mcp.tool()
def quick_analysis_summary(ticker: str) -> str:
    """Get a quick one-line summary of a stock's fundamental health.

    Args:
        ticker: Stock symbol

    Returns:
        JSON string with quick summary
    """
    try:
        fundamental = fundamental_analyzer.get_summary_dict(ticker)
        health = fundamental.get("health", {})
        
        summary = {
            "ticker": ticker.upper(),
            "status": "success",
            "health_score": health.get("score"),
            "overall_health": "Strong" if health.get("score", 0) > 70 else "Moderate" if health.get("score", 0) > 40 else "Weak",
            "summary": health.get("summary"),
            "valuation": health.get("valuation"),
            "growth_trend": health.get("growth_trend")
        }
        
        return json.dumps(summary, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)


# ============================================================================
# Main
# ============================================================================

def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
