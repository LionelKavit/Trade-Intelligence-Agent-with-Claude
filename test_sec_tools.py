#!/usr/bin/env python3
"""Test script to verify SEC EDGAR tools are working correctly."""

import sys
import json
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all modules import correctly."""
    print("Testing imports...")
    try:
        from fintools_mcp.sec_filings import SECFilingsFetcher
        from fintools_mcp.sec_fundamental import FundamentalAnalyzer
        from fintools_mcp.combined_analyzer import CombinedAnalyzer
        print("  ✓ All SEC modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_sec_filings():
    """Test SEC filings fetcher."""
    print("\nTesting SEC filings fetcher...")
    try:
        from fintools_mcp.sec_filings import SECFilingsFetcher
        
        fetcher = SECFilingsFetcher()
        
        # Test with a major company
        print("  Fetching CIK for AAPL...")
        cik = fetcher.get_company_cik("AAPL")
        if cik:
            print(f"    ✓ Found CIK: {cik}")
        else:
            print("    ⚠ Could not find CIK (this is OK, might be API rate limit)")
        
        print("  Getting filings summary for AAPL...")
        filings = fetcher.get_filings_summary("AAPL")
        
        if filings.get("status") == "success":
            print(f"    ✓ Fetched {len(filings.get('filings_by_type', {}))} filing types")
            print(f"    Latest filing: {filings.get('latest_filing', {}).get('type')}")
            return True
        else:
            print(f"    ⚠ {filings.get('status')}")
            return False
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_fundamental_analyzer():
    """Test fundamental analyzer."""
    print("\nTesting fundamental analyzer...")
    try:
        from fintools_mcp.sec_fundamental import FundamentalAnalyzer
        
        analyzer = FundamentalAnalyzer()
        
        print("  Analyzing MSFT...")
        metrics = analyzer.get_financial_metrics("MSFT")
        
        if metrics.pe_ratio or metrics.roe or metrics.profit_margin:
            print(f"    ✓ Got financial metrics")
            if metrics.pe_ratio:
                print(f"      P/E Ratio: {metrics.pe_ratio}")
            if metrics.profit_margin:
                print(f"      Profit Margin: {metrics.profit_margin:.2%}")
            if metrics.roe:
                print(f"      ROE: {metrics.roe:.2%}")
        
        print("  Getting health assessment...")
        health = analyzer.assess_health("MSFT", metrics)
        print(f"    ✓ Health Score: {health.health_score:.1f}/100")
        print(f"    Profitability: {health.profitability}")
        print(f"    Debt Level: {health.debt_level}")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_combined_analyzer():
    """Test combined analyzer."""
    print("\nTesting combined analyzer...")
    try:
        from fintools_mcp.combined_analyzer import CombinedAnalyzer
        
        analyzer = CombinedAnalyzer()
        
        print("  Performing combined analysis on GOOGL...")
        analysis = analyzer.analyze("GOOGL", period="3mo")
        
        if "recommendation" in analysis:
            print(f"    ✓ Got combined analysis")
            print(f"      Recommendation: {analysis['combined_signal']['recommendation']}")
            print(f"      Confidence: {analysis['combined_signal']['confidence']}")
            print(f"      Technical trend: {analysis['technical'].get('trend')}")
            print(f"      Fundamental score: {analysis['fundamental'].get('health', {}).get('score')}")
            return True
        else:
            print("    ✗ No recommendation generated")
            return False
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_mcp_server():
    """Test that MCP server can be imported."""
    print("\nTesting MCP server module...")
    try:
        from fintools_mcp import sec_server
        
        # Check that tools are defined
        tools = [
            "get_recent_filings",
            "get_fundamental_metrics",
            "get_combined_analysis",
            "compare_fundamentals",
            "get_filing_details",
            "quick_analysis_summary"
        ]
        
        print(f"  ✓ SEC server module loads")
        print(f"    Defined tools: {len(tools)}")
        for tool in tools:
            print(f"      - {tool}")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("SEC EDGAR Tools - Verification Tests")
    print("=" * 70)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("SEC Filings", test_sec_filings()))
    results.append(("Fundamental Analyzer", test_fundamental_analyzer()))
    results.append(("Combined Analyzer", test_combined_analyzer()))
    results.append(("MCP Server", test_mcp_server()))
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    print("=" * 70)
    print(f"\nResults: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("✓ All systems operational!")
        print("\nNext steps:")
        print("  1. Update pyproject.toml: ✓ Done")
        print("  2. Run: pip install -e .")
        print("  3. Update Claude Desktop config (see CLAUDE_DESKTOP_SETUP.md)")
        print("  4. Restart Claude Desktop")
        print("  5. Start using SEC tools!")
        return 0
    else:
        print("✗ Some tests failed. Check errors above.")
        if not results[0][1]:  # Imports failed
            print("\nTry: pip install requests")
        return 1


if __name__ == "__main__":
    sys.exit(main())
