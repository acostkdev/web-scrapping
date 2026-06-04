"""
fase1_scraper_feeds.py
Sistema de Monitoreo de Noticias - Fase 1

Extrae artículos desde feeds RSS usando Scrapy (producción) o feedparser (rápido).
feedparser sigue disponible como fallback para pruebas rápidas.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()


def scrape_con_scrapy(urls, output="data/dataset_scrapy.json"):
    """
    Ejecuta el spider de Scrapy para extraer artículos.
    Retorna la ruta del archivo generado.
    """
    urls_str = ",".join(urls)
    cmd = [
        sys.executable, "-m", "scrapy", "crawl", "rss_spider",
        "-a", f"urls={urls_str}",
        "-O", output,
    ]
    
    print(f"  Ejecutando Scrapy spider...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_DIR)
    
    if result.returncode != 0:
        print(f"  ⚠ Scrapy falló: {result.stderr[:200]}")
        print(f"  Usando feedparser como fallback...")
        return None
    
    print(f"  ✓ Scrapy completado")
    return output


def scrape_con_feedparser(urls, max_por_feed=10):
    """Fallback rápido usando feedparser."""
    import feedparser
    import time
    
    todos = []
    errores = []
    
    for url in urls:
        try:
            feed = feedparser.parse(url)
            items = []
            for e in feed.entries[:max_por_feed]:
                items.append({
                    "title": e.get("title", ""),
                    "link": e.get("link", ""),
                    "published": e.get("published", e.get("updated", "")),
                    "summary": e.get("summary", e.get("description", "")),
                    "source": url,
                    "scraped_at": datetime.now().isoformat(),
                })
            todos.extend(items)
            print(f"    {len(items)} artículos de {url[:50]}...")
        except Exception as e:
            errores.append({"url": url, "error": str(e)})
            print(f"    ERROR: {e}")
        time.sleep(0.3)
    
    return todos, errores


def run(feed_urls, usar_scrapy=True, output_path="data/dataset_crudo.json"):
    print("=" * 60)
    print("FASE 1: SCRAPER DE FEEDS RSS")
    print("=" * 60)
    print()
    print(f"Fuentes: {len(feed_urls)}")
    print()
    
    if usar_scrapy:
        out = scrape_con_scrapy(feed_urls)
        if out:
            print(f"\n✅ Scrapy generó: {out}")
            # Scrapy ya guardó en JSON, cargamos para retornar
            with open(out, encoding="utf-8") as f:
                lines = json.load(f)
            dataset = {
                "metadata": {"total": len(lines), "fuentes": len(feed_urls), "scraper": "scrapy"},
                "articles": lines,
            }
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)
            return dataset
    
    # fallback
    print("📡 Usando feedparser...")
    articles, errors = scrape_con_feedparser(feed_urls)
    
    dataset = {
        "metadata": {
            "total_articles": len(articles),
            "sources": len(feed_urls),
            "errors": len(errors),
            "scraper": "feedparser",
            "scraped_at": datetime.now().isoformat(),
        },
        "articles": articles,
        "errors": errors,
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Dataset guardado: {output_path}")
    print(f"   {len(articles)} artículos")
    if errors:
        print(f"   ⚠ {len(errors)} errores")
    
    return dataset


DEFAULT_FEEDS = [
    "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/mexico/portada",
    "https://www.reddit.com/r/python/.rss",
    "https://hnrss.org/frontpage",
    "https://feeds.bbci.co.uk/news/rss.xml",
]


if __name__ == "__main__":
    usar_scrapy = "--feedparser" not in sys.argv
    run(DEFAULT_FEEDS, usar_scrapy=usar_scrapy)
