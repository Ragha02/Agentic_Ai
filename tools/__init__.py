# tools/__init__.py
"""
Content Creation Pipeline Tools

This module contains utility tools for the content creation pipeline:
- Free web search functions
- Wikipedia integration
- Content research tools
"""

from .search_tools import (
    free_web_search,
    search_wikipedia,
    get_search_context,
    search_reddit
)

__version__ = "1.0.0"
__author__ = "Content Pipeline Team"

# Make search tools easily importable
__all__ = [
    'free_web_search',
    'search_wikipedia',
    'get_search_context',
    'search_reddit'
]

# Available search methods
AVAILABLE_SEARCH_METHODS = [
    "DuckDuckGo (free, no API key)",
    "Wikipedia (free)",
    "Reddit (free, limited)",
]

def get_available_search_methods():
    """Return list of available free search methods"""
    return AVAILABLE_SEARCH_METHODS