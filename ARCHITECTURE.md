# Financial Analysis Agent - What You Have

Complete AI agent system combining Claude AI with fintools-mcp for professional financial analysis.

## 🎯 What This Is

A production-ready Python application that:
1. **Runs fintools-mcp locally** - All financial analysis tools available
2. **Connects to Claude API** - AI-powered conversation and reasoning
3. **Provides multiple interfaces** - CLI chat, REST API, WebSocket
4. **Maintains conversation context** - Multi-turn analysis with history
5. **Handles tool calling** - Claude can request financial analysis on-demand

## 📦 Files Created

### Core Application
- **`agent_app.py`** - Main agent with CLI and REST/WebSocket API
- **`advanced_agent.py`** - Advanced version with proper MCP tool integration
- **`mcp_client.py`** - MCP protocol client for connecting to fintools-mcp

### Documentation
- **`QUICK_START.md`** - 5-minute setup guide (start here!)
- **`AGENT_SETUP.md`** - Complete documentation and configuration
- **`ARCHITECTURE.md`** - This file

### Examples
- **`example1_simple_chat.py`** - Basic usage and queries
- **`example2_api_client.py`** - How to use REST API
- **`example3_batch_analysis.py`** - Multi-step analysis with context
- **`example4_websocket.py`** - Real-time WebSocket communication

### Configuration
- **`agent_requirements.txt`** - Python dependencies for the agent
- **`verify_setup.py`** - Setup verification script

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install dependencies
pip install -r agent_requirements.txt

# 2. Set API key
export ANTHROPIC_API_KEY="sk-your-key"

# 3. Run agent (pick one)
python agent_app.py --mode cli          # Interactive CLI
python agent_app.py --mode api          # REST/WebSocket API
python advanced_agent.py --mode cli     # Advanced with tools

# 4. Try an example
python example1_simple_chat.py
```

See `QUICK_START.md` for more details!

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Your Application                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │           Claude AI (via Anthropic)              │   │
│  └──────────────┬───────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐   │
│  │        Agent Orchestrator                        │   │
│  │  • Conversation history                          │   │
│  │  • Message routing                               │   │
│  │  • Tool calling                                  │   │
│  └──────────────┬───────────────────────────────────┘   │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐   │
│  │    MCP Client (Protocol Handler)                 │   │
│  └──────────────┬───────────────────────────────────┘   │
│                 │                                        │
│                 │ MCP Protocol                           │
│                 │                                        │
│  ┌──────────────▼───────────────────────────────────┐   │
│  │        fintools-mcp Server                       │   │
│  │  • Technical indicators                          │   │
│  │  • Position sizing                               │   │
│  │  • Stock screening                               │   │
│  │  • Options analysis                              │   │
│  │  • Trade statistics                              │   │
│  └──────────────┬───────────────────────────────────┘   │
│                 │                                        │
│                 ▼                                        │
│           Yahoo Finance (Data)                           │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │            User Interfaces                       │   │
│  ├──────────────────────────────────────────────────┤   │
│  │  • CLI Chat Terminal                             │   │
│  │  • REST API (HTTP)                               │   │
│  │  • WebSocket (Real-time)                         │   │
│  │  • Python SDK (Direct import)                    │   │
│  └──────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 💡 How It Works

### Example: Analyzing a Stock

```
1. User asks: "What's the technical setup on AAPL?"

2. Agent receives message and sends to Claude

3. Claude decides it needs data:
   - Calls get_technical_indicators("AAPL")

4. Agent executes tool:
   - MCP client sends request to fintools-mcp server
   - Server calls fintools-mcp tools
   - Data returns (RSI, MACD, ATR, etc.)

5. Claude receives data and generates response:
   "AAPL looks bullish with RSI at 62, MACD positive,
    and EMAs stacked. I'd look for a breakout above $190..."

6. Response sent back to user
```

## 🛠️ Main Components

### `agent_app.py` - Main Agent
```python
# Simple usage
from agent_app import FinancialAgent

agent = FinancialAgent()
response = agent.chat("Analyze SPY")
print(response)
```

Features:
- Interactive CLI interface
- REST API with FastAPI
- WebSocket support
- Auto-starts fintools-mcp server
- Conversation history management

### `advanced_agent.py` - Advanced Agent  
```python
# Advanced with tool integration
from advanced_agent import AdvancedFinancialAgent
from mcp_client import MCPClient

mcp = MCPClient(Path("fintools_mcp/server.py"))
mcp.start()

agent = AdvancedFinancialAgent(mcp)
response = agent.chat("Find oversold stocks")
```

Features:
- Proper MCP protocol handling
- Dynamic tool loading
- Agentic loop (multi-turn tool calling)
- Better error handling

### `mcp_client.py` - MCP Client
Handles communication with fintools-mcp server:
- Tool discovery
- Tool execution
- Response parsing

## 📊 Available Tools

The agent can use these tools:

| Tool | Use Case |
|------|----------|
| `get_technical_indicators` | RSI, MACD, ATR, EMAs, Fibonacci, trend |
| `get_stock_quote` | Current price, volume, market data |
| `get_trend_score` | Trend analysis (-100 to +100) |
| `get_support_resistance` | Key price levels |
| `screen_stocks` | Find S&P 500 opportunities |
| `analyze_options_chain` | Options IV and setup analysis |
| `calculate_position_size` | Risk-based position sizing |
| `calculate_atr_position` | ATR-based position sizing |
| `analyze_trades` | Trade performance metrics |
| `compare_tickers` | Multi-stock comparison |

## 🎮 Interfaces

### 1. CLI Chat
```bash
python agent_app.py --mode cli

You: What's SPY's trend?
Agent: SPY is in a strong uptrend...
You: Find oversold stocks
Agent: Scanning S&P 500...
```

### 2. REST API
```bash
# Start server
python agent_app.py --mode api

# Send request
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze AAPL"}'

# Get interactive docs
open http://localhost:8000/docs
```

### 3. WebSocket
```bash
# Real-time bidirectional
ws://localhost:8000/ws/chat

# Send message, get instant response
```

### 4. Python SDK
```python
from agent_app import FinancialAgent

agent = FinancialAgent()
response = agent.chat("Size position: NVDA at $500, stop $480, target $530")
print(response)
```

## 📚 Examples

### Example 1: Simple Chat
```bash
python example1_simple_chat.py
```
Basic queries and responses - great for learning.

### Example 2: API Client  
```bash
# Terminal 1
python agent_app.py --mode api

# Terminal 2
python example2_api_client.py
```
Shows how to build a REST client.

### Example 3: Batch Analysis
```bash
python example3_batch_analysis.py
```
Multi-step analysis:
- Compare portfolio
- Deep dive into best stock
- Size position
- Analyze sector rotation

### Example 4: WebSocket
```bash
# Terminal 1
python agent_app.py --mode api

# Terminal 2
python example4_websocket.py interactive
```
Real-time chat with streaming responses.

## 🔧 Configuration

### Environment Variables
```bash
ANTHROPIC_API_KEY="sk-..."    # Required: Claude API key
CLAUDE_MODEL="claude-3-5-sonnet-20241022"  # Optional: Model version
```

### API Options
```bash
python agent_app.py --mode api --host 127.0.0.1 --port 8000
```

### Custom Configuration
Edit agent_app.py:
- `SYSTEM_PROMPT` - Agent instructions
- `MCP_SERVER_PATH` - Path to fintools-mcp
- Model name and parameters

## 📈 Use Cases

1. **Technical Analysis**
   - Quick stock analysis
   - Multi-symbol comparison
   - Trend identification

2. **Position Management**
   - Risk-based sizing
   - Stop/target calculation
   - Options analysis

3. **Market Screening**
   - Find oversold/overbought stocks
   - Identify breakout setups
   - Sector rotation

4. **Trade Analysis**
   - Performance metrics
   - Win rate calculation
   - Strategy evaluation

5. **Portfolio Management**
   - Compare holdings
   - Identify rebalancing opportunities
   - Risk assessment

## 🚀 Deployment

### Local Development
```bash
python agent_app.py --mode cli
```

### Single Server
```bash
python agent_app.py --mode api --host 0.0.0.0 --port 8000
```

### Docker
```bash
docker build -t fintools-agent .
docker run -e ANTHROPIC_API_KEY=$KEY -p 8000:8000 fintools-agent
```

### Production (Systemd)
See `AGENT_SETUP.md` for systemd service file.

## 🔍 Verification

Check that everything is set up correctly:
```bash
python verify_setup.py
```

This checks:
- Python version
- All dependencies installed
- API key configured
- Project files present

## 📖 Documentation

- **`QUICK_START.md`** - 5-minute setup guide ⭐ START HERE
- **`AGENT_SETUP.md`** - Complete documentation
- **`ARCHITECTURE.md`** - This file
- **Examples** - 4 working examples
- **Docstrings** - In-code documentation

## ⚡ Common Commands

```bash
# Setup
pip install -r agent_requirements.txt
export ANTHROPIC_API_KEY="sk-..."
python verify_setup.py

# Run
python agent_app.py --mode cli              # CLI
python agent_app.py --mode api              # API
python advanced_agent.py --mode cli         # Advanced

# Examples
python example1_simple_chat.py              # Basic
python example2_api_client.py               # REST client
python example3_batch_analysis.py           # Batch
python example4_websocket.py interactive    # WebSocket

# Verify
python verify_setup.py                      # Check setup
```

## 🎓 Next Steps

1. **Start with QUICK_START.md** - Fastest way to get running
2. **Try example1_simple_chat.py** - See it in action
3. **Pick an interface** - CLI, API, or WebSocket
4. **Integrate into your workflow** - Use as library or service
5. **Customize as needed** - Add your own prompts, tools, etc.

## 📞 Support

- Check **QUICK_START.md** for fastest answers
- See **AGENT_SETUP.md** for detailed docs
- Review **examples** for usage patterns
- Run **verify_setup.py** for troubleshooting

## 🎉 You're All Set!

You now have a production-ready financial analysis agent. Pick a mode above and start using it!

---

**Questions?** Start with `QUICK_START.md` →
