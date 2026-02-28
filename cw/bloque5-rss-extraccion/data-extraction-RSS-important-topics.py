import feedparser
import re

# 1. CONFIGURACIÓN DE TU TEMARIO
TEMARIO = {
    "IA en la vida diaria": ["ia", "inteligencia artificial", "algoritmo", "tecnología", "digital"],
    "Salud mental y bienestar": ["salud mental", "ansiedad", "bienestar", "psicológico", "estrés"],
    "Algoritmos y Sociedad": ["privacidad", "datos", "vigilancia", "desinformación", "redes sociales"]
}

def clean_text(text):
    if not text: return ""
    text = re.sub(r"<[^>]+>", " ", text) # Quitar HTML
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE) # Solo letras/espacios
    return text.lower().strip()

def realizar_actividad(url):
    feed = feedparser.parse(url)
    print(f"--- RESULTADOS PARA: {feed.feed.title} ---\n")

    # Diccionario para guardar hallazgos por tema
    hallazgos = {tema: [] for tema in TEMARIO}

    for entry in feed.entries:
        # Unimos título y resumen para buscar en todo el texto
        contenido_completo = clean_text(entry.get("title", "") + " " + entry.get("summary", ""))
        
        # Lógica de clasificación: revisamos cada tema del temario
        for tema, palabras_clave in TEMARIO.items():
            if any(palabra in contenido_completo for palabra in palabras_clave):
                hallazgos[tema].append({
                    "titulo": entry.title,
                    "link": entry.link
                })

    # Imprimir el reporte final
    for tema, articulos in hallazgos.items():
        print(f"📌 TEMA: {tema.upper()}")
        if not articulos:
            print("   No se encontraron noticias recientes sobre este tema.")
        for a in articulos[:2]: # Limitamos a 2 por tema para el reporte
            print(f"   - {a['titulo']}\n     Link: {a['link']}")
        print("-" * 50)

# URL de la ONU (puedes probar con las otras que tenías comentadas)
url_onu = "https://news.un.org/feed/subscribe/es/audio-product/all/audio-rss.xml"
realizar_actividad(url_onu)