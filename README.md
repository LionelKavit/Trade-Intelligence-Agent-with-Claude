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
