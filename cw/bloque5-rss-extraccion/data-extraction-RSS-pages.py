import feedparser
import json

def fetch_rss(url, max_entries=20):
    """Extrae ítems de un feed RSS/Atom. Devuelve lista de diccionarios."""
    try:
        feed = feedparser.parse(url)
        items = []
        for e in feed.entries[:max_entries]:
            items.append({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "published": e.get("published", e.get("updated", "")),
                "summary": e.get("summary", e.get("description", "")),
            })
        return items
    except Exception as err:
        return [{"error": str(err), "url": url}]

"""url = "https://pyfound.blogspot.com/feeds/posts/default?alt=rss" """

""" Pagina de la ONU """
""" url = "https://news.un.org/feed/subscribe/es/audio-product/all/audio-rss.xml" """

""" Pagina de la NASA """
"""url = "https://www.jpl.nasa.gov/feeds/news/" """

""" Feed de españa"""
url = "https://www.boe.es/rss/boe.php?s=1"
items = fetch_rss(url, max_entries=15)
print(json.dumps(items, indent=2, ensure_ascii=False))
