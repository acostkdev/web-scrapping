import feedparser
import json
import os
import re

# 🔹 Configuración de Temas y Feeds
topics_feeds = {
    "01_Inteligencia_Artificial": [
        "https://www.technologyreview.com/feed/",       # MIT Tech Review
        "https://www.wired.com/feed/category/gear/latest/rss", # IA y Herramientas
        "https://openai.com/news/rss.xml"               # Noticias de OpenAI
    ],
    "02_Salud_Mental": [
        "https://www.psychologytoday.com/intl/front/feed",
        "https://greatergood.berkeley.edu/rss"          # Bienestar basado en ciencia
    ],
    "03_Sociedad_Digital": [
        "https://www.eff.org/rss/updates.xml",          # Privacidad y Vigilancia
        "https://www.theguardian.com/technology/rss"    # Control de información
    ]
}

def fetch_rss(url, max_entries=15):
    """Extrae datos del feed."""
    feed = feedparser.parse(url)
    items = []
    # Obtener el nombre del sitio, si falla usar parte de la URL
    source_name = feed.feed.get("title", url.split("/")[2])
    
    for e in feed.entries[:max_entries]:
        items.append({
            "title": e.get("title", ""),
            "link": e.get("link", ""),
            "published": e.get("published", e.get("updated", "")),
            "summary": e.get("summary", e.get("description", "")),
        })
    return source_name, items

def sanitize(name):
    """Sanitiza nombres para archivos en Linux."""
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(" ", "_").lower()

# 🔹 Ejecución principal
base_dir = "investigation_output"

for topic, urls in topics_feeds.items():
    # Crear carpeta por cada tema principal
    topic_path = os.path.join(base_dir, topic)
    os.makedirs(topic_path, exist_ok=True)
    
    for url in urls:
        try:
            source_name, data = fetch_rss(url)
            filename = f"{sanitize(source_name)}.json"
            filepath = os.path.join(topic_path, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            print(f"✅ [{topic}] Guardado: {source_name}")
            
        except Exception as err:
            print(f"❌ Error en {url}: {err}")

print(f"\nProceso completado. Revisa la carpeta correspondiente")