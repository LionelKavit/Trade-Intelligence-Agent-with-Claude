# Financial Analysis Agent - Setup & Usage Guide

A complete Python agent system that combines Claude AI with fintools-mcp for professional financial analysis.

## Features

- **Interactive Chat Interface**: CLI-based conversation with Claude
- **REST API**: HTTP endpoints for programmatic access
- **WebSocket Support**: Real-time bidirectional communication
- **Tool Integration**: Access all fintools-mcp tools directly
- **Conversation History**: Maintains context across messages
- **Risk Management**: Position sizing and trade analysis tools

## Quick Start

### 1. Install Dependencies

```bash
# Install fintools-mcp (if not already installed)
pip install fintools-mcp

# Install agent dependencies
pip install -r agent_requirements.txt
```

Or with `uv`:
```bash
uv pip install fintools-mcp
uv pip install -r agent_requirements.txt
```

### 2. Set Up API Key

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Run the Agent

#### CLI Chat Mode (Recommended for Testing)
```bash
python agent_app.py --mode cli
```

#### API Server Mode
```bash
python agent_app.py --mode api --host 127.0.0.1 --port 8000
```

#### Advanced Agent with Tool Integration
```bash
python advanced_agent.py --mode cli
```

## Usage Examples

### CLI Chat Interface

```bash
$ python agent_app.py --mode cli

==================== Financial Analysis Agent - Chat Interface ====================

Connected to Claude AI with fintools-mcp

Commands:
  'quit' or 'exit' - Exit the chat
  'reset' - Reset conversation history
  'help' - Show available tools

You: What's the technical setup on AAPL?

Analyzing...

Agent: I'll analyze Apple's technical setup for you...

[Detailed technical analysis with indicators, trend assessment, etc.]

You: Size a position if I want to go long at $150 with a $100k account?

Agent: Based on your entry and account size, here's the position sizing...

You: quit

Goodbye!
```

### API Mode

#### Start the Server
```bash
python agent_app.py --mode api
```

Server starts at `http://127.0.0.1:8000`

#### Send a Chat Message (REST)
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the trend for SPY?"}'
```

Response:
```json
{
  "message": "What is the trend for SPY?",
  "response": "Based on current technical analysis...",
  "conversation_length": 2
}
```

#### WebSocket Chat (Real-time)
```python
import asyncio
import websockets
import json

async def chat():
    uri = "ws://127.0.0.1:8000/ws/chat"
    async with websockets.connect(uri) as ws:
        # Send message
        await ws.send(json.dumps({"message": "Analyze MSFT"}))
        
        # Receive response
        response = await ws.recv()
        print(json.loads(response))

asyncio.run(chat())
```

#### Reset Conversation
```bash
curl -X POST "http://127.0.0.1:8000/reset"
```

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```

#### API Documentation
Open browser to: `http://127.0.0.1:8000/docs`

## Available Tools

The agent has access to these fintools-mcp tools:

| Tool | Purpose |
|------|---------|
| `get_technical_indicators` | RSI, MACD, ATR, EMAs, Fibonacci, trend |
| `get_stock_quote` | Price, volume, 52-week range, market cap |
| `get_trend_score` | Trend score (-100 to +100) analysis |
| `get_support_resistance` | Key price levels and strength |
| `screen_stocks` | S&P 500 screening by criteria |
| `analyze_options_chain` | Options analysis with IV metrics |
| `calculate_position_size` | Risk-based position sizing |
| `calculate_atr_position` | ATR-based position sizing |
| `analyze_trades` | Trade statistics and performance |
| `compare_tickers` | Multi-symbol comparison |

## Example Queries

Ask the agent things like:

- "What's the technical setup on NVDA?"
- "Find oversold S&P 500 stocks still above their 200 EMA"
- "Show me support and resistance levels for QQQ"
- "Size a long position on AAPL at $150 with a $100k account risking 1.5%"
- "Compare AAPL, GOOGL, MSFT on technical strength"
- "Analyze this options chain for SPY next Friday"
- "Here are my last 20 trades: [150, -80, 200, ...] — what's my win rate?"

## Architecture

```
fintools-mcp-agent/
├── agent_app.py              # Main agent with CLI & REST/WebSocket API
├── advanced_agent.py         # Advanced agent with MCP tool integration
├── mcp_client.py             # MCP client wrapper
├── agent_requirements.txt    # Agent dependencies
└── AGENT_SETUP.md            # This file
```

### How It Works

1. **MCP Server**: fintools-mcp runs as a subprocess
2. **Agent**: Runs Claude via Anthropic API
3. **Tool Calling**: Claude requests tool calls, agent executes them
4. **Conversation**: Maintains history for context
5. **Interface**: CLI or API endpoints for user interaction

## Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY       # Required: Your Claude API key
CLAUDE_MODEL           # Optional: Model to use (default: claude-3-5-sonnet-20241022)
```

### API Configuration

```python
# In agent_app.py, modify these to customize:
- MCP_SERVER_PATH      # Path to fintools_mcp server
- SYSTEM_PROMPT        # Agent's system instructions
- Model name           # Claude model version
```

## Development

### Running Tests

```bash
# Test the agent locally
python -c "from agent_app import FinancialAgent; a = FinancialAgent(); print(a.chat('Hi'))"
```

### Adding Custom Tools

To add more tools or customize behavior:

1. Edit `SYSTEM_PROMPT` in `agent_app.py`
2. Add tool definitions in `mcp_client.py`
3. Implement tool handlers as needed

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Troubleshooting

### MCP Server Won't Start
```bash
# Check if fintools-mcp is installed
python -m fintools_mcp

# Try manual installation
pip install --upgrade fintools-mcp
```

### API Key Error
```bash
# Verify API key
echo $ANTHROPIC_API_KEY

# Set if missing
export ANTHROPIC_API_KEY="sk-..."
```

### Connection Refused
- Ensure port 8000 is available
- Use `--port` flag to specify different port
- Check firewall settings

### Tool Calls Not Working
- Verify MCP server started successfully
- Check logs for errors
- Ensure all fintools-mcp dependencies installed

## Production Deployment

### Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r agent_requirements.txt
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
EXPOSE 8000
CMD ["python", "agent_app.py", "--mode", "api", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t fintools-agent .
docker run -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY -p 8000:8000 fintools-agent
```

### Systemd Service

Create `/etc/systemd/system/fintools-agent.service`:
```ini
[Unit]
Description=Financial Analysis Agent
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/fintools-mcp
Environment="ANTHROPIC_API_KEY=..."
ExecStart=/usr/bin/python3 agent_app.py --mode api --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable fintools-agent
sudo systemctl start fintools-agent
```

## Performance Tips

- **Conversation Limit**: Reset conversation history periodically for better performance
- **Batch Requests**: Use API for batch processing of multiple tickers
- **Caching**: Implement Redis caching for frequently requested stocks
- **Async**: Use WebSocket for multiple concurrent users

## License

Same as fintools-mcp (MIT)

## Support

For issues with fintools-mcp, see: https://github.com/slimbiggins007/fintools-mcp

For agent-specific issues, check:
1. MCP server logs
2. API response codes
3. ANTHROPIC_API_KEY validity
4. Network connectivity
