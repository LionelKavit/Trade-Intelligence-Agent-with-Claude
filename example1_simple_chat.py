"""
Example 1: Simple Chat Interface
Simple example showing how to use the agent in CLI mode.
"""

from agent_app import FinancialAgent

def main():
    # Initialize agent
    agent = FinancialAgent()
    
    print("Example 1: Financial Analysis Agent\n")
    
    # Example 1: Technical Analysis
    print("=" * 50)
    print("Query: What's the technical setup on AAPL?")
    print("=" * 50)
    response = agent.chat("What's the technical setup on AAPL?")
    print(f"\nAgent: {response}\n")
    
    # Example 2: Trend Analysis
    print("=" * 50)
    print("Query: Compare AAPL, GOOGL, and MSFT trends")
    print("=" * 50)
    response = agent.chat("Compare AAPL, GOOGL, and MSFT trends. Which is strongest?")
    print(f"\nAgent: {response}\n")
    
    # Example 3: Position Sizing
    print("=" * 50)
    print("Query: Position sizing recommendation")
    print("=" * 50)
    response = agent.chat(
        "I want to go long NVDA at $100 with a $50k account, "
        "stop at $95, target at $110. How many shares should I buy?"
    )
    print(f"\nAgent: {response}\n")
    
    # Example 4: Screening
    print("=" * 50)
    print("Query: Stock screening")
    print("=" * 50)
    response = agent.chat(
        "Find me oversold stocks (RSI < 30) from the S&P 500 "
        "that are still above their 200-day EMA"
    )
    print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
