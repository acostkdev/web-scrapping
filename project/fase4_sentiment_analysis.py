"""
fase4_sentiment_analysis.py
Sistema de Monitoreo de Noticias - Fase 4

Analiza polaridad de artículos usando VADER (inglés) y léxico español.
Genera distribución de sentimientos por categoría con gráficas.
"""

import json
import re
from collections import Counter

from nltk.sentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import numpy as np


# léxico español
POSITIVAS = set("bueno excelente increible maravilloso fantastico extraordinario genial perfecto feliz alegre hermoso grandioso positivo exitoso beneficio mejora avance logro triunfo ganar victoria orgulloso esperanza prometedor innovador impresionante destacado lider eficiente solucion apoyo crecimiento prosperidad maravilla alegria exito".split())

NEGATIVAS = set("malo terrible horrible pesimo fatal desastroso peor decepcion fracaso perder perdida crisis peligro amenaza riesgo dano miedo preocupacion alerta conflicto guerra violencia corrupcion fraude escandalo caos emergencia tragedia desgracia dolor problema dificil debil fracasar fatal pesimo detesto odio horrible asco".split())

_vader = SentimentIntensityAnalyzer()


def es_ingles(texto):
    """Detecta si el texto parece inglés."""
    eng_words = {"the", "and", "for", "are", "but", "not", "you", "all", "can", "had", "was", "our", "has", "have", "been", "will", "more", "about", "than", "some", "would", "your"}
    tokens = texto.lower().split()
    if not tokens:
        return True
    eng_count = sum(1 for t in tokens if t in eng_words)
    return eng_count / len(tokens) > 0.15


def analyze_sentiment(text, title=""):
    """Analiza sentimiento: VADER para inglés, léxico español para español."""
    combined = f"{title} {text}"
    
    if es_ingles(combined):
        scores = _vader.polarity_scores(combined)
        compound = scores["compound"]
        if compound >= 0.3:
            pol = "positivo"
        elif compound <= -0.3:
            pol = "negativo"
        else:
            pol = "neutro"
        return {"polarity": pol, "score": compound, "method": "vader"}
    
    # español: léxico
    tokens = combined.lower().split()
    pos = sum(1 for t in tokens if t in POSITIVAS)
    neg = sum(1 for t in tokens if t in NEGATIVAS)
    score = pos - neg
    
    if score > 1:
        pol = "positivo"
    elif score < -1:
        pol = "negativo"
    else:
        pol = "neutro"
    
    return {"polarity": pol, "score": score, "method": "lexicon_es"}


def plot_sentiment_by_category(articles, output="data/sentiment_by_category.png"):
    data = {}
    for a in articles:
        cat = a.get("category", "general")
        pol = a.get("sentiment", {}).get("polarity", "neutro")
        if cat not in data:
            data[cat] = Counter()
        data[cat][pol] += 1
    
    cats = sorted(data.keys())
    pos = [data[c]["positivo"] for c in cats]
    neg = [data[c]["negativo"] for c in cats]
    neu = [data[c]["neutro"] for c in cats]
    
    x = np.arange(len(cats))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - 0.25, pos, 0.25, label="Positivo", color="#4CAF50")
    ax.bar(x, neu, 0.25, label="Neutro", color="#FFC107")
    ax.bar(x + 0.25, neg, 0.25, label="Negativo", color="#F44336")
    ax.set_title("Sentimiento por Categoría")
    ax.set_xticks(x)
    ax.set_xticklabels(cats, rotation=30)
    ax.legend()
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()


def plot_polarity_hist(articles, output="data/polarity_distribution.png"):
    scores = [a.get("sentiment", {}).get("score", 0) for a in articles]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(scores, bins=15, color="#2196F3", edgecolor="white")
    ax.axvline(0, color="red", linestyle="--", alpha=0.5)
    ax.set_title("Distribución de Polaridad")
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()


def run(input_path="data/dataset_clasificado.json", output_path="data/dataset_sentiment.json"):
    print("=" * 60)
    print("FASE 4: ANÁLISIS DE SENTIMIENTOS")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    print(f"Analizando {len(articles)} artículos...")
    print()
    
    metodos = Counter()
    for art in articles:
        text = f"{art.get('title_clean', '')} {art.get('summary_clean', '')}"
        result = analyze_sentiment(text, art.get("title", ""))
        art["sentiment"] = result
        metodos[result["method"]] += 1
    
    pols = Counter(a["sentiment"]["polarity"] for a in articles)
    total = sum(a["sentiment"]["score"] for a in articles)
    
    print("📊 Resumen:")
    print(f"  Positivos: {pols.get('positivo', 0)}")
    print(f"  Negativos: {pols.get('negativo', 0)}")
    print(f"  Neutros:   {pols.get('neutro', 0)}")
    print(f"  Score neto: {total:+}")
    for m, c in metodos.most_common():
        print(f"  Método usado: {m} ({c} textos)")
    print()
    
    plot_polarity_hist(articles)
    plot_sentiment_by_category(articles)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dataset con sentimientos: {output_path}")
    return data


if __name__ == "__main__":
    run()
