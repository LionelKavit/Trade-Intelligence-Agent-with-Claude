# Trade-Intelligence-Agent-with-Claude
A reliable quant research tool that uses real market data to test and monitor strategies, backing it with fundamental research and market news – all in one. This financial analysis platform gives Claude (and other AI assistants) access to professional-grade trading tools. Think of it as:
1. Trader's Toolkit (technical indicators, position sizing, options analysis)
2. Powered by AI (Claude reasons about the data and answers your questions)
3. In Natural Language (you just ask questions in English)

WHAT VALUE DOES IT PROVIDE:

A) Without this system:
- You manually check each indicator
- You manually calculate position sizes
- You miss context by looking at one metric at a time
- Analysis takes hours

B) With this system:
- Claude orchestrates the analysis
- It calls relevant tools automatically
- It combines insights across tools
- It explains everything in plain English
- Analysis takes seconds

SYSTEM ARCHITECTURE (WITH EXAMPLE) BELOW:

LAYER 1: USER INTERFACE

User asks: "If I go long AAPL at $150 with a $100k account risking 1.5%, what's my position size?"
via - Claude Chat / CLI Chat / REST API

LAYER 2: AI REASONING

Claude (Gen AI)
• Recognizes: "This needs position_size calculation"
• Decides what tools to use
• Calls tool via MCP
• Reasons about the tool results
• Writes a clear answer

LAYER 3: TOOL CALLING

MCP (Model Context Protocol)
• Safe tool interface
• Claude calls specific tools
• Tools return structured data

LAYER 4: FINANCIAL TOOLS

fintools-mcp (Technical Analysis)
• RSI, MACD, ATR, EMAs (indicators)
• Support/Resistance (price levels)
• Position Sizing (risk management)
• Stock Screening (find opportunities)
• Options Analysis (derivatives)
• Trade Statistics (performance)

LAYER 5: DATA SOURCE

Yahoo Finance (Market Data)
• Historical prices
• Options chains
• Volume, volatility, etc.

# fintools-mcp: Enterprise Financial Analysis for Claude Desktop

---

## Project Overview

`fintools-mcp` transforms Claude into a professional-grade **trade intelligence agent** with **19 AI-powered financial analysis tools** that work seamlessly in Claude Desktop.

### The Problem It Solves

Traditional stock analysis requires:
- 5+ separate tools/subscriptions ($100-300/month)
- Manual data integration (error-prone, slow)
- 20-30 minutes per stock analysis
- Constant context switching between apps

### The Solution

One question to Claude:
```
"Analyze Apple completely"
```

Returns in 10 seconds:
- Technical chart analysis (RSI, MACD, ATR, trend)
- Fundamental metrics (P/E, debt, health score, valuations)
- Latest news with sentiment analysis
- Confidence-weighted buy/hold/sell recommendation

**150x faster. Free. Integrated.**

---

## Value Proposition

| Metric | Before | After |
|--------|--------|-------|
| **Time per analysis** | 25 minutes | 10 seconds |
| **Cost** | $100-300/month | $0 |
| **News sources** | 5 (manual) | 40,000+ (automatic) |
| **Tools to learn** | 5+ UIs | 1 (Claude) |
| **Consistency** | Manual (errors) | Systematic (reliable) |
| **Scale** | 4 stocks/hour | 100+ stocks/hour |

---

## The 19 Tools

### Technical Analysis (11 tools)
- RSI, MACD, ATR, EMAs (9/21/50/200)
- Support & resistance levels
- Fibonacci levels & trend scoring
- Options chain analysis
- Position sizing (2 methods)
- Trade performance analysis
- Multi-stock comparison
- News & sentiment
- Stock screening (S&P 500)
- Market quotes

### Fundamental Analysis (6 tools)
- SEC filings (10-K, 10-Q, 8-K)
- Financial metrics (P/E, ROE, margins)
- Health scoring (0-100)
- Debt analysis
- Company comparison
- Quick analysis summary

### Integration (2 tools + config)
- News fetcher (40,000 sources)
- Combined analysis (technical + fundamental + news)
- Sentiment-adjusted recommendations

---

## How It Works

### Architecture
```
Claude Desktop
    ↓
[fintools server] + [sec-filings server]
    ↓
[Technical Analysis] + [Fundamental Analysis] + [News/Sentiment]
    ↓
Real-time recommendations with reasoning
```

### Data Sources (All FREE)
- **Market data**: Yahoo Finance (real-time)
- **SEC filings**: SEC EDGAR API (official)
- **News**: Yahoo Finance + NewsAPI (optional, 100 req/day free)
- **Fundamentals**: Yahoo Finance calculations

### Example Flow
```
User: "Analyze Tesla"
↓
Claude calls all tools in parallel:
  ✓ get_technical_indicators() → RSI 45, MACD negative
  ✓ get_fundamental_metrics() → P/E 28, Health 62
  ✓ get_stock_news() → 3 positive, 2 negative articles
↓
Claude integrates:
  Technical: Neutral (bearish MACD, neutral RSI)
  Fundamental: Below average health
  News: Slightly negative
↓
Recommendation: "HOLD - Mixed signals" (confidence: 55%)
```

---

## Installation

### 1. Install Package
```bash
pip install -e .
```

### 2. Configure Claude Desktop
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fintools": {
      "command": "/opt/anaconda3/bin/python",
      "args": ["-m", "fintools_mcp"]
    },
    "sec-filings": {
      "command": "/opt/anaconda3/bin/python",
      "args": ["-m", "fintools_mcp.sec_server"]
    }
  }
}
```

### 3. (Optional) Add NewsAPI Key
```bash
# Easy option: set environment variable
export NEWSAPI_KEY="your_free_api_key"

# Or save to config file
nano ~/.fintools_config.json
# Add: "newsapi_key": "your_key"
```

### 4. Restart Claude Desktop
Close Claude → Wait 5 sec → Reopen Claude

---

## Usage Examples

### Example 1: Quick Analysis
```
Claude: "Analyze AAPL"

Returns:
- Price: $189.94
- Technical: Bullish (RSI 65, MACD positive)
- Fundamental: Strong (P/E 28, Health 78)
- News: Positive (4/5 articles)
- Recommendation: BUY (confidence: 72%)
```

### Example 2: Screening
```
Claude: "Find oversold stocks with strong fundamentals"

Returns:
- Screens S&P 500 for RSI < 30
- Filters for Health > 70
- Checks news sentiment
- Returns top 5 with entry/exit prices
```

### Example 3: Deep Dive
```
Claude: "Deep analysis on Microsoft"

Returns:
- Latest 10-K filing summary
- Financial metrics vs industry
- Chart patterns
- News sentiment
- Comparison with AAPL & GOOGL
```

### Example 4: Position Sizing
```
Claude: "Size a position for NVDA with 2% risk, entry at 120"

Returns:
- Position size (calculate shares)
- Stop loss price
- Profit target
- Risk/reward ratio
```

---

## Real-World Use Cases

### Day Traders
- Intraday setups with technical indicators
- Quick screening for RSI extremes
- Options chain analysis
- Risk-managed position sizing

### Swing Traders
- 2-5 day setups
- Technical + fundamental confirmation
- News catalyst detection
- Portfolio-aware recommendations

### Long-term Investors
- Fundamental deep dives
- SEC filing analysis
- Multi-year trend assessment
- Company comparison

### Options Traders
- Options chain analysis
- IV percentile tracking
- Risk management
- Trade performance review

### Portfolio Managers
- Multi-stock screening
- Sector analysis
- Risk assessment
- Performance reporting

---

## Key Features

✅ **Multiple Analysis Layers**
- Technical (chart patterns, momentum)
- Fundamental (valuation, health, quality)
- Sentiment (news, market events)
- Integrated (confidence-weighted)

✅ **Real-Time Data**
- Market prices (live)
- News (40,000+ sources)
- SEC filings (latest)
- Options data (current)

✅ **Risk Management**
- Position sizing by risk %
- ATR-based stop/target
- Portfolio-aware recommendations
- Drawdown analysis

✅ **Enterprise Features**
- SEC EDGAR access
- Options chain analysis
- Multi-year historical data
- S&P 500 screening

✅ **Zero Learning Curve**
- Works in Claude (no new tools)
- Natural language queries
- Conversational analysis
- Instant results

---

## Performance

| Task | Time | Scale |
|------|------|-------|
| Single stock analysis | ~5 sec | AAPL |
| Multi-stock comparison | ~10 sec | 5 stocks |
| S&P 500 screening | ~30 sec | 500 stocks |
| Complete deep dive | ~15 sec | 3 layers + news |

---

## Comparison with Alternatives

| Feature | Traditional | fintools-mcp |
|---------|-------------|--------------|
| **Cost** | $100-300/month | $0 |
| **Setup time** | 30+ min | 2 min |
| **UI to learn** | 5+ separate | 1 (Claude) |
| **Data integration** | Manual | Automatic |
| **Analysis speed** | 20 min | 10 sec |
| **News sources** | 3-5 | 40,000+ |
| **Consistency** | Variable | Systematic |
| **Customization** | Limited | Unlimited |

---

## Project Structure

```
fintools-mcp/
├── fintools_mcp/
│   ├── server.py                 # Main technical server
│   ├── sec_server.py             # Fundamental + news server
│   ├── sec_filings.py            # SEC filing fetcher
│   ├── sec_fundamental.py        # Fundamental analyzer
│   ├── combined_analyzer.py      # Integration layer
│   ├── news_fetcher.py           # News + sentiment
│   ├── data.py                   # Market data wrapper
│   ├── indicators/               # Technical indicators
│   └── analysis/                 # Analysis modules
└── tests/
    └── Comprehensive test suite
```

---

## Getting Started

### 5-Minute Quick Start
1. `pip install -e .`
2. Update Claude Desktop config
3. Restart Claude
4. Ask: "Analyze Apple"

### Full Setup (with NewsAPI)
1. Install package
2. Configure Claude
3. Get free NewsAPI key
4. Set `NEWSAPI_KEY` environment variable
5. Start analyzing

---

## The Bottom Line

**fintools-mcp brings enterprise-grade financial analysis to Claude Desktop.**

What took 25 minutes on 5 separate tools now takes 10 seconds in Claude.

No subscriptions. No complicated setup. Just ask Claude.

---

## Documentation Files

- **CLAUDE_DESKTOP_SETUP.md** — Integration guide
- **SEC_SETUP.md** — SEC tools documentation
- **NEWSAPI_SETUP.md** — News configuration
- **NEWS_TOOL_SUMMARY.md** — Sentiment features

---

**MIT License | Free & Open Source | Production Ready**
