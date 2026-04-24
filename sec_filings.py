"""SEC EDGAR filings fetcher using the modern SEC data API."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests
import yfinance as yf


# SEC requires a proper User-Agent header for all requests
USER_AGENT = "Sample Company Name AdminContact@example.com"


@dataclass
class Filing:
    """Represents a single SEC filing."""
    ticker: str
    form_type: str  # 10-K, 10-Q, 8-K, etc.
    filed_date: str  # YYYY-MM-DD
    filing_url: str
    accession_number: str
    fiscal_period_end: Optional[str] = None
    company_name: Optional[str] = None


@dataclass
class FilingContent:
    """Raw filing content and metadata."""
    filing: Filing
    content: str  # First 10,000 chars of filing
    sections: dict[str, str]  # MD&A, Risk Factors, etc.


class SECFilingsFetcher:
    """Fetch SEC EDGAR filings for companies."""
    
    COMPANY_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
    SUBMISSIONS_API_BASE = "https://data.sec.gov/submissions"
    
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize SEC filings fetcher.
        
        Args:
            cache_dir: Directory to cache filings (optional, defaults to ~/.fintools_cache)
        """
        # Use home directory cache by default for better compatibility
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.fintools_cache")
        else:
            cache_dir = os.path.expanduser(cache_dir)
        
        self.cache_dir = cache_dir
        
        # Try to create cache directory, but don't fail if we can't
        try:
            os.makedirs(cache_dir, exist_ok=True)
        except OSError as e:
            # If we can't create cache dir, just continue without caching
            pass
    
    def get_company_cik(self, ticker: str) -> Optional[str]:
        """Get CIK (Central Index Key) from ticker symbol.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            CIK number as 10-digit zero-padded string, or None if not found
        """
        try:
            # Use SEC's official company tickers list
            response = requests.get(
                self.COMPANY_TICKERS_URL,
                headers={"User-Agent": USER_AGENT},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ticker_upper = ticker.upper()
                
                for item in data.values():
                    if item.get('ticker', '').upper() == ticker_upper:
                        # Return CIK as 10-digit zero-padded string
                        cik_str = str(item.get('cik_str', ''))
                        return cik_str.zfill(10)
        except Exception as e:
            pass
        
        return None
    
    def get_recent_filings(
        self,
        ticker: str,
        form_types: list[str] | None = None,
        max_results: int = 10
    ) -> list[Filing]:
        """Get recent SEC filings for a company.
        
        Args:
            ticker: Stock symbol
            form_types: List of form types to fetch (e.g., ['10-K', '10-Q', '8-K'])
            max_results: Maximum number of filings to return
            
        Returns:
            List of Filing objects
        """
        if form_types is None:
            form_types = ['10-K', '10-Q', '8-K']
        
        cik = self.get_company_cik(ticker)
        if not cik:
            return []
        
        filings = []
        
        try:
            # Fetch from SEC data API using the company submissions endpoint
            url = f"{self.SUBMISSIONS_API_BASE}/CIK{cik}.json"
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=10
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            
            # Get company name
            company_name = data.get('name', ticker.upper())
            
            # Get recent filings
            recent_filings = data.get('filings', {}).get('recent', {})
            
            if not recent_filings:
                return []
            
            # Extract filing data
            forms = recent_filings.get('form', [])
            filings_dates = recent_filings.get('filingDate', [])
            accession_numbers = recent_filings.get('accessionNumber', [])
            report_dates = recent_filings.get('reportDate', [])
            
            # Build filing list
            count = 0
            for i in range(len(forms)):
                if count >= max_results:
                    break
                
                form_type = forms[i]
                
                # Filter by form types
                if form_type not in form_types:
                    continue
                
                filing_date = filings_dates[i] if i < len(filings_dates) else ''
                accession = accession_numbers[i] if i < len(accession_numbers) else ''
                report_date = report_dates[i] if i < len(report_dates) else ''
                
                # Convert accession number format: 0001193125-21-069921 -> 0001193125-21-069921
                accession_formatted = accession
                
                # Build filing URL
                accession_url_format = accession.replace('-', '')
                filing_url = (
                    f"https://www.sec.gov/cgi-bin/viewer?"
                    f"action=view&cik={cik}&accession_number={accession}&xbrl_type=v"
                )
                
                filing = Filing(
                    ticker=ticker.upper(),
                    form_type=form_type,
                    filed_date=filing_date,
                    filing_url=filing_url,
                    accession_number=accession,
                    fiscal_period_end=report_date,
                    company_name=company_name
                )
                
                filings.append(filing)
                count += 1
        
        except Exception as e:
            pass
        
        return filings
    
    def get_filing_content(self, filing: Filing, max_chars: int = 20000) -> Optional[FilingContent]:
        """Fetch filing content from SEC.
        
        Args:
            filing: Filing object
            max_chars: Maximum characters to fetch
            
        Returns:
            FilingContent with extracted sections
        """
        try:
            # Get filing HTML
            response = requests.get(
                filing.filing_url,
                headers={"User-Agent": USER_AGENT},
                timeout=10
            )
            if response.status_code != 200:
                return None
            
            content = response.text[:max_chars]
            
            # Extract common sections using regex
            sections = {}
            
            # Try to extract MD&A
            mda_match = re.search(
                r'(MANAGEMENT[\'"]?S DISCUSSION|MD&A|Management\'s Discussion and Analysis)',
                content,
                re.IGNORECASE
            )
            if mda_match:
                start = max(0, mda_match.start() - 500)
                end = min(len(content), mda_match.end() + 3000)
                sections['md_and_a'] = content[start:end]
            
            # Try to extract Risk Factors
            risk_match = re.search(
                r'(RISK FACTORS|RISKS)',
                content,
                re.IGNORECASE
            )
            if risk_match:
                start = max(0, risk_match.start() - 200)
                end = min(len(content), risk_match.end() + 2000)
                sections['risk_factors'] = content[start:end]
            
            # Try to extract Business Summary
            business_match = re.search(
                r'(BUSINESS|OVERVIEW|Our Business)',
                content,
                re.IGNORECASE
            )
            if business_match:
                start = max(0, business_match.start() - 200)
                end = min(len(content), business_match.end() + 2000)
                sections['business_summary'] = content[start:end]
            
            return FilingContent(
                filing=filing,
                content=content,
                sections=sections
            )
        
        except Exception as e:
            pass
        
        return None
    
    def get_filings_summary(self, ticker: str) -> dict:
        """Get a summary of recent filings for a ticker.
        
        Args:
            ticker: Stock symbol
            
        Returns:
            Dictionary with filing summary
        """
        filings = self.get_recent_filings(ticker)
        
        if not filings:
            return {
                "ticker": ticker.upper(),
                "status": "no_filings_found",
                "filings": []
            }
        
        # Group filings by type
        filings_by_type = {}
        for filing in filings:
            form_type = filing.form_type
            if form_type not in filings_by_type:
                filings_by_type[form_type] = []
            
            filings_by_type[form_type].append({
                "filed_date": filing.filed_date,
                "fiscal_period_end": filing.fiscal_period_end,
                "url": filing.filing_url,
                "accession": filing.accession_number
            })
        
        return {
            "ticker": ticker.upper(),
            "company_name": filings[0].company_name or ticker,
            "status": "success",
            "filings_by_type": filings_by_type,
            "latest_filing": {
                "type": filings[0].form_type,
                "filed": filings[0].filed_date,
                "url": filings[0].filing_url
            }
        }

