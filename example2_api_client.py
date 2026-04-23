"""
Example 2: API Client
Example showing how to interact with the agent via REST API.
"""

import requests
import json
from typing import Optional

BASE_URL = "http://127.0.0.1:8000"


class AgentAPIClient:
    """Client for interacting with the agent API."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def chat(self, message: str) -> Optional[str]:
        """Send a message and get response."""
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json={"message": message},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def health(self) -> bool:
        """Check if API is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def reset(self) -> bool:
        """Reset conversation history."""
        try:
            response = requests.post(f"{self.base_url}/reset", timeout=5)
            return response.status_code == 200
        except:
            return False


def main():
    print("Example 2: Agent REST API Client\n")
    
    client = AgentAPIClient()
    
    # Check if API is running
    if not client.health():
        print("Error: API server not running")
        print("Start it with: python agent_app.py --mode api")
        return
    
    print("✓ Connected to API server\n")
    
    # Example 1: Get technical analysis
    print("=" * 50)
    print("Requesting technical analysis for SPY...")
    print("=" * 50)
    response = client.chat("Analyze the technical setup on SPY. Is it bullish or bearish?")
    if response:
        print(f"\nResponse:\n{response}\n")
    
    # Example 2: Screen for opportunities
    print("=" * 50)
    print("Requesting stock screening...")
    print("=" * 50)
    response = client.chat(
        "Find S&P 500 stocks with strong uptrends (trend score > 50) "
        "that are above their 200 EMA. Show the top 5."
    )
    if response:
        print(f"\nResponse:\n{response}\n")
    
    # Example 3: Position sizing calculation
    print("=" * 50)
    print("Requesting position sizing...")
    print("=" * 50)
    response = client.chat(
        "Calculate position sizing for a long trade on QQQ: "
        "entry $350, stop $340, target $365, account $100k, risk 1.5%"
    )
    if response:
        print(f"\nResponse:\n{response}\n")
    
    # Example 4: Options analysis
    print("=" * 50)
    print("Requesting options analysis...")
    print("=" * 50)
    response = client.chat(
        "Analyze the SPY options chain for this Friday. "
        "What's the IV like? Any interesting setups for iron condors?"
    )
    if response:
        print(f"\nResponse:\n{response}\n")


if __name__ == "__main__":
    main()
