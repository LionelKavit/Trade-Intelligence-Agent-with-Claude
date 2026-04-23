"""
MCP Client wrapper for fintools-mcp integration.

Provides a client that connects to the local fintools-mcp MCP server
and exposes its tools for use by Claude.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Optional
import asyncio


class MCPClient:
    """Client for interacting with fintools-mcp server."""
    
    def __init__(self, server_script: Path):
        """Initialize the MCP client.
        
        Args:
            server_script: Path to the MCP server script (fintools_mcp/server.py)
        """
        self.server_script = server_script
        self.process: Optional[subprocess.Popen] = None
        self.tools_cache = {}
    
    def start(self):
        """Start the MCP server process."""
        if self.process is not None:
            return
        
        print(f"Starting MCP server from {self.server_script}")
        self.process = subprocess.Popen(
            [sys.executable, "-m", "fintools_mcp"],
            cwd=self.server_script.parent.parent,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
    
    def stop(self):
        """Stop the MCP server process."""
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None
    
    def get_tools(self) -> list[dict[str, Any]]:
        """Get available tools from the MCP server.
        
        Returns:
            List of tool definitions with name, description, and input schema.
        """
        if self.tools_cache:
            return self.tools_cache
        
        # For now, return hardcoded tool definitions
        # In a production system, you'd query the server dynamically
        tools = [
            {
                "name": "get_technical_indicators",
                "description": "Get technical indicators for a stock — RSI, MACD, ATR, EMAs, and Fibonacci levels.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol (e.g. AAPL, SPY, GOOGL)"
                        },
                        "period": {
                            "type": "string",
                            "enum": ["1mo", "3mo", "6mo", "1y"],
                            "description": "Data period (default 3mo)"
                        },
                        "interval": {
                            "type": "string",
                            "enum": ["1m", "5m", "15m", "1h", "1d"],
                            "description": "Bar interval (default 1d)"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_stock_quote",
                "description": "Get current stock quote with price, volume, 52-week range, and market cap.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_trend_score",
                "description": "Get trend score from -100 (strong downtrend) to +100 (strong uptrend) with component breakdown.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        },
                        "period": {
                            "type": "string",
                            "enum": ["1mo", "3mo", "6mo", "1y"],
                            "description": "Data period (default 3mo)"
                        },
                        "interval": {
                            "type": "string",
                            "enum": ["1m", "5m", "15m", "1h", "1d"],
                            "description": "Bar interval (default 1d)"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "get_support_resistance",
                "description": "Get key support/resistance levels with touch counts and strength ratings.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        },
                        "period": {
                            "type": "string",
                            "enum": ["1mo", "3mo", "6mo", "1y"],
                            "description": "Data period (default 3mo)"
                        }
                    },
                    "required": ["ticker"]
                }
            },
            {
                "name": "screen_stocks",
                "description": "Screen S&P 500 stocks by RSI, trend score, EMA position, relative volume.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "min_rsi": {
                            "type": "number",
                            "description": "Minimum RSI (0-100)"
                        },
                        "max_rsi": {
                            "type": "number",
                            "description": "Maximum RSI (0-100)"
                        },
                        "min_trend_score": {
                            "type": "number",
                            "description": "Minimum trend score (-100 to 100)"
                        },
                        "max_trend_score": {
                            "type": "number",
                            "description": "Maximum trend score (-100 to 100)"
                        },
                        "above_ema_200": {
                            "type": "boolean",
                            "description": "Filter to stocks above 200 EMA"
                        },
                        "above_ema_50": {
                            "type": "boolean",
                            "description": "Filter to stocks above 50 EMA"
                        },
                        "min_volume_ratio": {
                            "type": "number",
                            "description": "Minimum volume ratio vs 20-day average"
                        }
                    }
                }
            },
            {
                "name": "analyze_options_chain",
                "description": "Analyze options chain with IV analysis, liquidity filtering, put/call ratios.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        },
                        "expiration": {
                            "type": "string",
                            "description": "Expiration date (YYYY-MM-DD) or 'next_friday', 'next_month'"
                        },
                        "min_volume": {
                            "type": "integer",
                            "description": "Minimum option contract volume"
                        }
                    },
                    "required": ["ticker", "expiration"]
                }
            },
            {
                "name": "calculate_position_size",
                "description": "Calculate risk-based position size with stop loss and profit target.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        },
                        "entry_price": {
                            "type": "number",
                            "description": "Entry price"
                        },
                        "stop_loss": {
                            "type": "number",
                            "description": "Stop loss price"
                        },
                        "profit_target": {
                            "type": "number",
                            "description": "Profit target price"
                        },
                        "account_size": {
                            "type": "number",
                            "description": "Account size in dollars"
                        },
                        "risk_percent": {
                            "type": "number",
                            "description": "Risk percentage (e.g., 1.5 for 1.5%)"
                        }
                    },
                    "required": ["entry_price", "stop_loss", "profit_target", "account_size", "risk_percent"]
                }
            },
            {
                "name": "calculate_atr_position",
                "description": "ATR-based position sizing — auto-calculates stop and target from volatility.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Stock symbol"
                        },
                        "entry_price": {
                            "type": "number",
                            "description": "Entry price"
                        },
                        "account_size": {
                            "type": "number",
                            "description": "Account size in dollars"
                        },
                        "risk_percent": {
                            "type": "number",
                            "description": "Risk percentage (e.g., 1.5 for 1.5%)"
                        },
                        "atr_multiplier_stop": {
                            "type": "number",
                            "description": "ATR multiplier for stop (e.g., 1.5)"
                        },
                        "atr_multiplier_target": {
                            "type": "number",
                            "description": "ATR multiplier for target (e.g., 3.0)"
                        }
                    },
                    "required": ["ticker", "entry_price", "account_size", "risk_percent"]
                }
            },
            {
                "name": "analyze_trades",
                "description": "Analyze trade statistics — win rate, profit factor, Sharpe ratio, drawdown.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "pnls": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of trade P&Ls"
                        },
                        "initial_balance": {
                            "type": "number",
                            "description": "Starting account balance"
                        }
                    },
                    "required": ["pnls"]
                }
            },
            {
                "name": "compare_tickers",
                "description": "Side-by-side technical comparison across multiple symbols.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "tickers": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of stock symbols"
                        },
                        "period": {
                            "type": "string",
                            "enum": ["1mo", "3mo", "6mo", "1y"],
                            "description": "Data period (default 3mo)"
                        }
                    },
                    "required": ["tickers"]
                }
            }
        ]
        
        self.tools_cache = tools
        return tools
    
    def call_tool(self, tool_name: str, **kwargs) -> dict:
        """Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments for the tool
        
        Returns:
            Tool result as a dictionary
        """
        # Placeholder: In a real implementation, this would send a JSON-RPC
        # request to the server process and parse the response.
        # For now, we return a message indicating the tool would be called.
        
        return {
            "tool": tool_name,
            "args": kwargs,
            "status": "would_call",
            "message": f"Tool {tool_name} would be called with args: {kwargs}"
        }
