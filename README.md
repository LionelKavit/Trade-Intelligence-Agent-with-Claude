# Trade-Intelligence-Agent-with-Claude

A reliable quant research tool that uses real market data to test and monitor strategies, backing it with fundamental research and market news – all in one. It transforms Claude into a professional-grade **trade intelligence agent** with **19 AI-powered financial analysis tools** that work seamlessly in Claude Desktop. Think of it as a:
1. Trader's Toolkit (technical indicators, position sizing, options analysis)
2. Powered by AI (Claude reasons about the data and answers your questions)
3. In Natural Language (you just ask questions in English)


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

### Please refer to the following files to see different setups and their analyses reports:

1. NVDA_Equity_Analysis_Apr29_2026 -> For Equity Research

2. USChina_Macro_Analysis_Apr29_2026 -> For Macro Analysis

3. NVDA_AMD_TSM_Peer_Comparison_Apr29_2026 -> For Peer Comparison

4. TSM_Options_Analysis_LiveData_Apr29_2026 -> For Options Chain Analysis

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
