"""
Fact Checker Service - Wikipedia API Integration
Based on your documentation: Epic 2 - Fact Checker Service
"""

import requests
from typing import Dict, Optional
from app.config import WIKIPEDIA_USER_AGENT


def fact_check(query: str) -> Dict:
    """
    Verify a fact using Wikipedia API
    
    Args:
        query: The fact to verify
    
    Returns:
        Dictionary with summary, verified status, and source URL
    """
    if not query or len(query.strip()) < 3:
        return {
            "query": query,
            "summary": "Query too short to verify.",
            "verified": False,
            "source_url": None
        }
    
    try:
        # Wikipedia API endpoint
        url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "limit": 1
        }
        
        headers = {
            "User-Agent": WIKIPEDIA_USER_AGENT
        }
        
        # Make API request
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Check if we got any results
        search_results = data.get("query", {}).get("search", [])
        
        if not search_results:
            return {
                "query": query,
                "summary": "No relevant Wikipedia articles found.",
                "verified": False,
                "source_url": None
            }
        
        # Get the first result
        first_result = search_results[0]
        page_title = first_result.get("title", "")
        
        # Get the page content
        page_params = {
            "action": "query",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": page_title,
            "format": "json"
        }
        
        page_response = requests.get(url, params=page_params, headers=headers, timeout=10)
        page_response.raise_for_status()
        page_data = page_response.json()
        
        # Extract the page content
        pages = page_data.get("query", {}).get("pages", {})
        page_content = ""
        page_id = ""
        
        for pid, content in pages.items():
            page_id = pid
            page_content = content.get("extract", "")
            break
        
        # Build source URL
        source_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
        
        # Check if the query appears in the content
        verified = query.lower() in page_content.lower()
        
        return {
            "query": query,
            "summary": page_content[:300] + ("..." if len(page_content) > 300 else ""),
            "verified": verified,
            "source_url": source_url,
            "page_title": page_title
        }
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Wikipedia API error: {e}")
        return {
            "query": query,
            "summary": "Fact-checking service temporarily unavailable.",
            "verified": False,
            "source_url": None
        }
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return {
            "query": query,
            "summary": "An error occurred during fact-checking.",
            "verified": False,
            "source_url": None
        }