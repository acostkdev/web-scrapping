"""
fase6_chatbot.py
Sistema de Monitoreo de Noticias - Fase 6

Chatbot simple que responde consultas sobre los artículos usando
intent matching con regex y recuperación TF-IDF.
"""

import json
import re
from fase5_search_engine import search


INTENTS = [
    (r"(cuantos|cuantas|total|how many|count)", "count"),
    (r"(busca|search|find|encuentra|que dice|about)", "search"),
    (r"(categoria|categorias|categoria|categories|category)", "categories"),
    (r"(positivo|positivas|negativo|negativas|sentimiento)", "sentiment"),
    (r"(fuente|source|fuentes|sources)", "sources"),
    (r"(ayuda|help|comandos|que puedes|what can)", "help"),
]


def detect_intent(text):
    """Detecta la intención del usuario."""
    text = text.lower()
    for pattern, intent in INTENTS:
        if re.search(pattern, text):
            return intent
    return "search"


def handle_count(articles):
    """Responde cuántos artículos hay."""
    cats = {}
    for a in articles:
        c = a.get("category", "general")
        cats[c] = cats.get(c, 0) + 1
    
    lines = [f"📊 Total: {len(articles)} artículos"]
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        lines.append(f"  {cat}: {count}")
    return "\n".join(lines)


def handle_categories(articles):
    """Lista categorías disponibles."""
    cats = set(a.get("category", "general") for a in articles)
    return f"Categorías: {', '.join(sorted(cats))}"


def handle_sentiment(articles):
    """Resumen de sentimientos."""
    from collections import Counter
    pols = Counter(a.get("sentiment", {}).get("polarity", "neutro") for a in articles)
    return f"Positivo: {pols.get('positivo', 0)} | Neutro: {pols.get('neutro', 0)} | Negativo: {pols.get('negativo', 0)}"


def handle_sources(articles):
    """Lista fuentes únicas."""
    srcs = set()
    for a in articles:
        s = a.get("source", "")
        if s:
            srcs.add(s.split("/")[2] if "//" in s else s)
    return f"Fuentes ({len(srcs)}): " + ", ".join(sorted(srcs))


def handle_search(query, articles):
    """Busca artículos relevantes."""
    results, cat = search(query, articles)
    if not results:
        return "No encontré nada relevante."
    
    lines = [f"Top resultados para: \"{query}\""]
    if cat:
        lines.append(f"Categoría sugerida: {cat}")
    lines.append("")
    
    for i, (idx, score) in enumerate(results[:5]):
        art = articles[idx]
        title = art.get("title", "")[:60]
        source = art.get("source", "")[:30]
        lines.append(f"{i+1}. [{score:.3f}] {title}")
        lines.append(f"   {source}")
    
    return "\n".join(lines)


def chat(articles):
    """Bucle de chat interactivo."""
    print("🤖 Chatbot de Noticias (escribe 'salir' o 'exit' para terminar)")
    print("   Comandos: ayuda, cuantos articulos, categorias, sentimiento, fuentes")
    print("   O busca: 'busca python', 'find mexico', etc.")
    print()
    
    while True:
        try:
            query = input("  Tú: ").strip()
        except EOFError:
            break
        
        if not query:
            continue
        
        if query.lower() in ("salir", "exit", "quit"):
            print("  Chatbot: ¡Hasta luego!")
            break
        
        if query.lower() in ("ayuda", "help"):
            print("  Chatbot: Pregúntame sobre los artículos, busca noticias,")
            print("           o usa comandos como 'cuantos articulos'.")
            continue
        
        intent = detect_intent(query)
        
        if intent == "count":
            response = handle_count(articles)
        elif intent == "categories":
            response = handle_categories(articles)
        elif intent == "sentiment":
            response = handle_sentiment(articles)
        elif intent == "sources":
            response = handle_sources(articles)
        elif intent == "help":
            response = "Comandos: ayuda, cuantos articulos, categorias, sentimiento, fuentes, busca <tema>"
        else:
            response = handle_search(query, articles)
        
        print(f"  Chatbot: {response}")
        print()


def run(input_path="data/dataset_sentiment.json"):
    print("=" * 60)
    print("FASE 6: CHATBOT DE CONSULTAS")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    print(f"Chatbot cargado con {len(articles)} artículos")
    print()
    
    # demo automática
    print("📋 Demo de consultas:")
    queries = ["cuantos articulos hay", "categorias", "sentimiento", "busca python"]
    for q in queries:
        intent = detect_intent(q)
        if intent == "count":
            r = handle_count(articles)
        elif intent == "categories":
            r = handle_categories(articles)
        elif intent == "sentiment":
            r = handle_sentiment(articles)
        else:
            r = handle_search(q, articles)
        print(f"  Q: {q}")
        print(f"  A: {r.split(chr(10))[0]}")
        print()
    
    print("💬 Modo interactivo:")
    chat(articles)


if __name__ == "__main__":
    run()
