import feedparser
import json
import re

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
    

def clean_text(text):
    """Limpieza básica: quitar tags HTML, solo letras y espacios, minúsculas."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text

def normalize_items(items):
    """Añade campo 'text_clean' a cada ítem (título + resumen limpios)."""
    for it in items:
        if "error" in it:
            continue
        title = it.get("title", "")
        summary = it.get("summary", "")
        it["text_clean"] = clean_text(title) + " " + clean_text(summary)
    return items


"""url = "https://pyfound.blogspot.com/feeds/posts/default?alt=rss" """

""" Pagina de la ONU """
url = "https://news.un.org/feed/subscribe/es/audio-product/all/audio-rss.xml"

""" Pagina de la NASA """
"""url = "https://www.jpl.nasa.gov/feeds/news/" """

""" Feed de españa"""
"""url = "https://www.boe.es/rss/boe.php?s=1" """

items = fetch_rss(url, max_entries=15)

items_norm = normalize_items(items)
for i, it in enumerate(items_norm[:3]):
    if "error" not in it:
        print("--- Ítem", i+1, "---")
        print("text_clean:", it.get("text_clean", "")[:200], "...")
        print()
