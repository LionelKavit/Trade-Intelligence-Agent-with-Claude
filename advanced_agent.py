"""
Advanced Financial Agent with MCP tool integration.

This version properly connects to fintools-mcp and uses its tools via Claude's tool_use feature.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

from anthropic import Anthropic

from mcp_client import MCPClient


class AdvancedFinancialAgent:
    """Advanced AI agent with proper MCP tool integration."""
    
    SYSTEM_PROMPT = """You are an expert financial analyst AI assistant with access to real-time financial analysis tools.

You have access to professional-grade financial tools that provide:
- Technical indicators (RSI, MACD, ATR, EMAs, Fibonacci levels)
- Stock quotes and market data
- Support and resistance level identification
- Trend scoring and analysis
- Options chain analysis with IV metrics
- Risk-based position sizing
- Trade performance analytics
- Multi-ticker comparison

Your role is to:
1. Analyze stocks using technical and fundamental analysis
2. Help develop and validate trading strategies
3. Size positions according to risk management principles
4. Identify trading opportunities and setups
5. Evaluate trade performance and improve trading systems

Always:
- Use the available tools to provide data-backed analysis
- Be precise with calculations and terminology
- Emphasize risk management in all recommendations
- Ask clarifying questions when user intent is unclear
- Provide context and reasoning for your recommendations"""
    
    def __init__(self, mcp_client: MCPClient):
        """Initialize the agent.
        
        Args:
            mcp_client: Connected MCPClient instance
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        self.client = Anthropic(api_key=api_key)
        self.mcp_client = mcp_client
        self.conversation_history = []
        self.tools = []
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize tool definitions from MCP client."""
        mcp_tools = self.mcp_client.get_tools()
        
        # Convert to Anthropic tool format
        self.tools = [
            {
                "name": tool["name"],
                "description": tool["description"],
                "input_schema": tool.get("input_schema", {
                    "type": "object",
                    "properties": {},
                    "required": []
                })
            }
            for tool in mcp_tools
        ]
    
    def chat(self, user_message: str) -> str:
        """Send a message and get a response, processing tool calls as needed.
        
        Args:
            user_message: User's input message
        
        Returns:
            Final response text
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
        })
        
        # Agentic loop
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                system=self.SYSTEM_PROMPT,
                tools=self.tools,
                messages=self.conversation_history,
            )
            
            # Check if we should stop
            if response.stop_reason == "end_turn":
                # Extract final text response
                for content in response.content:
                    if hasattr(content, "text"):
                        final_response = content.text
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": response.content
                        })
                        return final_response
                break
            
            # Check if there are tool uses
            if response.stop_reason == "tool_use":
                # Add assistant's response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Process tool calls
                tool_results = []
                for content in response.content:
                    if content.type == "tool_use":
                        tool_name = content.name
                        tool_input = content.input
                        tool_use_id = content.id
                        
                        print(f"  Calling tool: {tool_name}")
                        
                        # Call the tool (in production, this would call the MCP server)
                        result = self._call_tool(tool_name, tool_input)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": json.dumps(result)
                        })
                
                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
            else:
                # Unexpected stop reason
                break
        
        # Fallback response
        return "Analysis complete. Please ask another question or request more specific analysis."
    
    def _call_tool(self, tool_name: str, tool_input: dict) -> dict:
        """Call a tool through the MCP client.
        
        Args:
            tool_name: Name of the tool
            tool_input: Input arguments for the tool
        
        Returns:
            Tool result
        """
        # In a real implementation, this would make actual MCP calls
        # For now, it's a placeholder
        return self.mcp_client.call_tool(tool_name, **tool_input)
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> dict:
        """Get a summary of the current conversation."""
        return {
            "messages": len(self.conversation_history),
            "turns": len([m for m in self.conversation_history if m["role"] == "user"]),
            "history_preview": self.conversation_history[-3:] if self.conversation_history else []
        }


def cli_chat_advanced(mcp_client: MCPClient):
    """Advanced CLI chat interface with tool support."""
    agent = AdvancedFinancialAgent(mcp_client)
    
    print("\n" + "=" * 70)
    print("Advanced Financial Analysis Agent")
    print("=" * 70)
    print("\nConnected to Claude AI with fintools-mcp tools\n")
    print("Commands:")
    print("  'quit' or 'exit' - Exit the chat")
    print("  'reset' - Reset conversation history")
    print("  'summary' - Show conversation summary")
    print("  'tools' - List available tools\n")
    
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
            
            if user_input.lower() == "summary":
                summary = agent.get_conversation_summary()
                print(f"\nConversation Summary:")
                print(f"  Messages: {summary['messages']}")
                print(f"  Turns: {summary['turns']}\n")
                continue
            
            if user_input.lower() == "tools":
                print("\nAvailable Tools:")
                for tool in agent.tools:
                    print(f"  • {tool['name']}: {tool['description']}")
                print()
                continue
            
            print("\nAnalyzing...\n")
            response = agent.chat(user_input)
            print(f"Agent: {response}\n")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
    finally:
        mcp_client.stop()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Financial Analysis Agent")
    parser.add_argument("--mode", choices=["cli", "api"], default="cli",
                       help="Run mode")
    args = parser.parse_args()
    
    # Initialize MCP client
    mcp_path = Path(__file__).parent / "fintools_mcp" / "server.py"
    mcp_client = MCPClient(mcp_path)
    mcp_client.start()
    
    try:
        if args.mode == "cli":
            cli_chat_advanced(mcp_client)
    finally:
        mcp_client.stop()
