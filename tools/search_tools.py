"""
Free web search tools for content research
No API keys required
"""

import requests
from urllib.parse import quote_plus
import time


def free_web_search(query, num_results=5):
    """Free web search using DuckDuckGo instant answers"""
    try:
        # DuckDuckGo instant answer API (free, no API key needed)
        url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1"
        response = requests.get(url, timeout=10)
        data = response.json()

        results = []

        # Get abstract if available
        if data.get('Abstract'):
            results.append({
                'title': data.get('AbstractText', 'Summary'),
                'content': data.get('Abstract'),
                'source': data.get('AbstractURL', 'DuckDuckGo')
            })

        # Get related topics
        for topic in data.get('RelatedTopics', [])[:3]:
            if isinstance(topic, dict) and topic.get('Text'):
                results.append({
                    'title': topic.get('Text', '')[:50] + '...',
                    'content': topic.get('Text', ''),
                    'source': topic.get('FirstURL', 'DuckDuckGo')
                })

        return results[:num_results] if results else [
            {'title': 'No results', 'content': f'No specific information found for: {query}', 'source': 'N/A'}
        ]

    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
        return [
            {'title': 'Search Error', 'content': f'Could not search for: {query}. Using internal knowledge.',
             'source': 'Error'}
        ]


def search_wikipedia(query, num_results=3):
    """Free Wikipedia search"""
    try:
        import wikipedia
        wikipedia.set_lang("en")

        # Search for pages
        search_results = wikipedia.search(query, results=num_results)
        results = []

        for title in search_results[:num_results]:
            try:
                page = wikipedia.page(title)
                summary = wikipedia.summary(title, sentences=3)
                results.append({
                    'title': page.title,
                    'content': summary,
                    'source': page.url
                })
            except:
                continue

        return results if results else [
            {'title': 'No Wikipedia results', 'content': f'No Wikipedia articles found for: {query}', 'source': 'N/A'}
        ]

    except ImportError:
        return [
            {'title': 'Wikipedia not available', 'content': 'Install wikipedia package: pip install wikipedia',
             'source': 'N/A'}
        ]
    except Exception as e:
        print(f"Wikipedia search error: {e}")
        return [
            {'title': 'Wikipedia Error', 'content': f'Wikipedia search failed for: {query}', 'source': 'Error'}
        ]


def get_search_context(topic, max_results=5):
    """Get comprehensive search context using multiple free sources"""
    print(f"🔍 Searching for information about: {topic}")

    search_results = []

    # Method 1: DuckDuckGo
    print("  📡 Searching DuckDuckGo...")
    ddg_results = free_web_search(topic)
    search_results.extend(ddg_results)

    # Small delay to be respectful to APIs
    time.sleep(1)

    # Method 2: Wikipedia
    print("  📚 Searching Wikipedia...")
    wiki_results = search_wikipedia(topic)
    search_results.extend(wiki_results)

    # Format results for the agent
    context = "WEB SEARCH RESULTS:\n"
    context += "=" * 40 + "\n"

    for i, result in enumerate(search_results[:max_results], 1):
        context += f"\n{i}. {result['title']}\n"
        context += f"   Content: {result['content'][:400]}...\n"
        context += f"   Source: {result['source']}\n"
        context += "-" * 40 + "\n"

    context += f"\nTotal sources found: {len(search_results[:max_results])}\n"
    context += "=" * 40 + "\n"

    print(f"  ✅ Found {len(search_results[:max_results])} sources")

    return context


# Additional free search methods you can add:

def search_reddit(query, limit=3):
    """Search Reddit for discussions (free)"""
    try:
        url = f"https://www.reddit.com/search.json?q={quote_plus(query)}&limit={limit}"
        headers = {'User-Agent': 'ContentPipeline/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        results = []
        for post in data.get('data', {}).get('children', []):
            post_data = post.get('data', {})
            if post_data.get('title') and post_data.get('selftext'):
                results.append({
                    'title': post_data['title'],
                    'content': post_data['selftext'][:300],
                    'source': f"https://reddit.com{post_data.get('permalink', '')}"
                })

        return results

    except Exception as e:
        print(f"Reddit search error: {e}")
        return []


def search_news_free(query):
    """Search for news using free RSS feeds"""
    try:
        # You can add RSS feed parsing here
        # Example: BBC, Reuters, etc. have free RSS feeds
        pass
    except Exception as e:
        print(f"News search error: {e}")
        return []