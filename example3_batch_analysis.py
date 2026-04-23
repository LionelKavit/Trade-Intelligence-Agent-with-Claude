"""
Example 3: Batch Analysis & Conversation Flow
Shows how to analyze multiple stocks with context-aware conversation.
"""

from agent_app import FinancialAgent


def analyze_portfolio(agent: FinancialAgent, tickers: list[str]):
    """Analyze a portfolio of stocks with context."""
    
    print(f"Analyzing portfolio: {', '.join(tickers)}\n")
    
    # 1. Compare all stocks
    print("=" * 60)
    print(f"Step 1: Comparing {len(tickers)} stocks")
    print("=" * 60)
    
    comparison_query = (
        f"Compare the technical setups for {', '.join(tickers)}. "
        "Which has the strongest uptrend? Which is most oversold?"
    )
    response = agent.chat(comparison_query)
    print(f"Analysis:\n{response}\n")
    
    # 2. Deep dive into strongest
    print("=" * 60)
    print("Step 2: Deep dive into strongest performer")
    print("=" * 60)
    
    followup_query = f"Based on your analysis, which one should I focus on? Tell me the entry setup."
    response = agent.chat(followup_query)
    print(f"Focus Stock:\n{response}\n")
    
    # 3. Position sizing for recommended trade
    print("=" * 60)
    print("Step 3: Position sizing for recommended stock")
    print("=" * 60)
    
    sizing_query = (
        "Size a position for me if I want to go long at the mentioned entry point "
        "with a $100,000 account, risking 2%, with a 3:1 reward:risk ratio"
    )
    response = agent.chat(sizing_query)
    print(f"Position Sizing:\n{response}\n")
    
    # 4. Risk management
    print("=" * 60)
    print("Step 4: Risk management & stops")
    print("=" * 60)
    
    risk_query = "Where should I place my stops and targets based on technical levels?"
    response = agent.chat(risk_query)
    print(f"Risk Management:\n{response}\n")


def analyze_trade_performance(agent: FinancialAgent):
    """Analyze past trading performance."""
    
    print("\nAnalyzing Trade Performance\n")
    print("=" * 60)
    
    # Sample trades
    trades = [150, -75, 200, -50, 300, 100, -100, 250, -200, 400]
    
    query = (
        f"Analyze my trading performance. Here are my last 10 trades (P&L): {trades}. "
        "Calculate my win rate, average winner/loser, profit factor, and Sharpe ratio. "
        "Starting balance was $50,000."
    )
    
    response = agent.chat(query)
    print(f"Performance Analysis:\n{response}\n")
    
    # Follow up question
    print("=" * 60)
    print("Asking for improvement recommendations")
    print("=" * 60)
    
    followup = (
        "Based on this analysis, what should I improve in my trading strategy?"
    )
    
    response = agent.chat(followup)
    print(f"Recommendations:\n{response}\n")


def analyze_sector_rotation(agent: FinancialAgent):
    """Analyze sector rotation strategy."""
    
    print("\nAnalyzing Sector Rotation\n")
    print("=" * 60)
    
    # Sector ETFs
    sector_etfs = {
        "XLK": "Technology",
        "XLV": "Healthcare",
        "XLF": "Financials",
        "XLI": "Industrials",
        "XLE": "Energy",
        "XLU": "Utilities",
        "XLRE": "Real Estate",
        "XLY": "Consumer Discretionary",
        "XLP": "Consumer Staples",
        "XLB": "Materials"
    }
    
    tickers = list(sector_etfs.keys())
    
    query = (
        f"Compare these sector ETFs for strength: {', '.join(tickers)}. "
        "Which sectors are in uptrends? Which are showing weakness? "
        "Where is the best sector rotation opportunity right now?"
    )
    
    response = agent.chat(query)
    print(f"Sector Analysis:\n{response}\n")
    
    # Follow up for specific entry
    print("=" * 60)
    print("Getting specific entry recommendation")
    print("=" * 60)
    
    followup = (
        "Which of the strong sectors offers the best entry point right now? "
        "What's the technical setup look like?"
    )
    
    response = agent.chat(followup)
    print(f"Best Entry:\n{response}\n")


def main():
    """Run all example analyses."""
    agent = FinancialAgent()
    
    print("\n" + "=" * 70)
    print("Example 3: Batch Analysis & Conversation Flow")
    print("=" * 70 + "\n")
    
    # Example 1: Portfolio analysis
    print("\n### EXAMPLE 1: Portfolio Analysis ###\n")
    tech_stocks = ["AAPL", "MSFT", "GOOGL", "NVDA", "META"]
    analyze_portfolio(agent, tech_stocks)
    
    # Reset for next analysis
    agent.reset_conversation()
    print("\n[Conversation reset]\n")
    
    # Example 2: Trade performance
    print("\n### EXAMPLE 2: Trade Performance Analysis ###")
    analyze_trade_performance(agent)
    
    # Reset for next analysis
    agent.reset_conversation()
    print("\n[Conversation reset]\n")
    
    # Example 3: Sector rotation
    print("\n### EXAMPLE 3: Sector Rotation Strategy ###")
    analyze_sector_rotation(agent)
    
    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
