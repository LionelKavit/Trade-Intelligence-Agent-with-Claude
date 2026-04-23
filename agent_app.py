"""
AI Agent using fintools-mcp via MCP protocol.

This agent connects to a local fintools-mcp server and provides:
- Chat interface for interactive financial analysis
- API endpoints for programmatic access
- Claude as the AI backbone
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
import uvicorn

from anthropic import Anthropic


# ============================================================================
# Configuration
# ============================================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("Error: ANTHROPIC_API_KEY environment variable not set")
    sys.exit(1)

MCP_SERVER_PATH = Path(__file__).parent / "fintools_mcp" / "server.py"
MCP_PROCESS: Optional[subprocess.Popen] = None


# ============================================================================
# MCP Server Management
# ============================================================================

def start_mcp_server():
    """Start the fintools-mcp server as a subprocess."""
    global MCP_PROCESS
    
    if MCP_PROCESS is not None:
        return
    
    print("Starting fintools-mcp server...")
    try:
        MCP_PROCESS = subprocess.Popen(
            [sys.executable, "-m", "fintools_mcp"],
            cwd=Path(__file__).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Give server time to start
        time.sleep(2)
        print("✓ fintools-mcp server started")
    except Exception as e:
        print(f"✗ Failed to start fintools-mcp server: {e}")
        raise


def stop_mcp_server():
    """Stop the fintools-mcp server."""
    global MCP_PROCESS
    
    if MCP_PROCESS is not None:
        print("Stopping fintools-mcp server...")
        MCP_PROCESS.terminate()
        try:
            MCP_PROCESS.wait(timeout=5)
        except subprocess.TimeoutExpired:
            MCP_PROCESS.kill()
        MCP_PROCESS = None
        print("✓ fintools-mcp server stopped")


# ============================================================================
# Agent
# ============================================================================

class FinancialAgent:
    """AI agent for financial analysis using fintools-mcp."""
    
    SYSTEM_PROMPT = """You are an expert financial analyst AI assistant with access to real-time financial analysis tools.

You have access to the following tools via MCP:
- get_technical_indicators: RSI, MACD, ATR, EMAs, Fibonacci levels, trend assessment
- get_stock_quote: Current price, volume, 52-week range, market cap
- get_trend_score: Trend score (-100 to +100) with component breakdown
- get_support_resistance: Key support/resistance levels with strength ratings
- screen_stocks: Screen S&P 500 by RSI, trend score, EMA position, relative volume
- analyze_options_chain: Options chain with IV analysis and liquidity filtering
- calculate_position_size: Risk-based position sizing with stop loss and profit target
- calculate_atr_position: ATR-based position sizing with auto-calculated stops
- analyze_trades: Win rate, profit factor, Sharpe ratio, drawdown analysis
- compare_tickers: Side-by-side technical comparison across multiple symbols

Your role is to:
1. Help users analyze stocks and market conditions using technical analysis
2. Provide position sizing recommendations based on risk management principles
3. Screen for trading opportunities matching specific criteria
4. Analyze options strategies with IV and liquidity considerations
5. Evaluate trading performance and statistics
6. Compare multiple securities for relative strength

Always:
- Be precise with financial terminology and calculations
- Use the tools to provide data-backed analysis
- Consider risk management in all recommendations
- Ask clarifying questions when user intent is unclear
- Provide context for your recommendations"""
    
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.conversation_history = []
        # Note: In a real implementation, you would connect to the MCP server
        # and extract tools from it. For now, we describe the available tools.
    
    def chat(self, user_message: str) -> str:
        """Send a message and get a response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=self.conversation_history,
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message,
        })
        
        return assistant_message
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Financial Analysis Agent",
    description="AI-powered financial analysis using fintools-mcp",
    version="1.0.0",
)

agent = FinancialAgent()


@app.on_event("startup")
async def startup():
    """Start the MCP server on app startup."""
    start_mcp_server()


@app.on_event("shutdown")
async def shutdown():
    """Stop the MCP server on app shutdown."""
    stop_mcp_server()


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/chat")
async def chat(request: dict):
    """
    Send a message to the agent and get a response.
    
    Request body:
    {
        "message": "What's the technical setup on AAPL?"
    }
    """
    message = request.get("message", "").strip()
    if not message:
        return {"error": "Message cannot be empty"}
    
    try:
        response = agent.chat(message)
        return {
            "message": message,
            "response": response,
            "conversation_length": len(agent.conversation_history),
        }
    except Exception as e:
        return {"error": str(e)}, 500


@app.post("/reset")
async def reset():
    """Reset the conversation history."""
    agent.reset_conversation()
    return {"status": "Conversation reset"}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat.
    
    Send messages as JSON: {"message": "..."}
    Receive responses as JSON: {"response": "..."}
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "").strip()
            
            if not message:
                await websocket.send_json({"error": "Message cannot be empty"})
                continue
            
            try:
                response = agent.chat(message)
                await websocket.send_json({
                    "response": response,
                    "conversation_length": len(agent.conversation_history),
                })
            except Exception as e:
                await websocket.send_json({"error": str(e)})
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()


# ============================================================================
# CLI Interface
# ============================================================================

def cli_chat():
    """Interactive CLI chat interface."""
    start_mcp_server()
    
    print("\n" + "=" * 70)
    print("Financial Analysis Agent - Chat Interface")
    print("=" * 70)
    print("\nConnected to Claude AI with fintools-mcp\n")
    print("Commands:")
    print("  'quit' or 'exit' - Exit the chat")
    print("  'reset' - Reset conversation history")
    print("  'help' - Show available tools\n")
    
    try:
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit"]:
                print("\nGoodbye!")
                break
            
            if user_input.lower() == "reset":
                agent.reset_conversation()
                print("Conversation history reset.\n")
                continue
            
            if user_input.lower() == "help":
                print("\nAvailable Tools:")
                print("- get_technical_indicators: RSI, MACD, ATR, EMAs, Fibonacci")
                print("- get_stock_quote: Price, volume, 52-week range")
                print("- get_trend_score: Trend analysis (-100 to +100)")
                print("- get_support_resistance: Key levels")
                print("- screen_stocks: S&P 500 screening")
                print("- analyze_options_chain: Options analysis")
                print("- calculate_position_size: Risk-based position sizing")
                print("- calculate_atr_position: ATR-based sizing")
                print("- analyze_trades: Trade performance analysis")
                print("- compare_tickers: Side-by-side comparison\n")
                continue
            
            print("\nAnalyzing...\n")
            response = agent.chat(user_input)
            print(f"Agent: {response}\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    finally:
        stop_mcp_server()


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Financial Analysis Agent"
    )
    parser.add_argument(
        "--mode",
        choices=["cli", "api"],
        default="cli",
        help="Run mode: cli for chat interface, api for REST/WebSocket server",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="API host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="API port (default: 8000)",
    )
    
    args = parser.parse_args()
    
    if args.mode == "cli":
        cli_chat()
    else:
        print(f"Starting API server on {args.host}:{args.port}")
        print("Chat endpoint: POST /chat")
        print("WebSocket endpoint: WS /ws/chat")
        print("Health check: GET /health")
        print("Reset: POST /reset")
        print("API docs: http://localhost:8000/docs")
        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            log_level="info",
        )
