"""
fase2_nlp_preprocessing.py
Sistema de Monitoreo de Noticias - Fase 2

Limpia, tokeniza y normaliza los textos extraídos.
Elimina HTML, stopwords básicas, puntuación.
Guarda corpus limpio para fases de clasificación y análisis.
"""

import json
import re
import string
from pathlib import Path

from nltk.stem import SnowballStemmer

_stemmer = SnowballStemmer("spanish")

def stem_token(token):
    return _stemmer.stem(token)

# stopwords básicas en español e inglés
STOPWORDS = set("""
a ante bajo cabe con contra de desde durante en entre hacia hasta mediante
para por según sin so sobre tras y e o u el la los las lo un una unos unas
que es por al del como más pero sus le va ha hay fue era haber poder muy
se no me te su mi tu mis tus nuestro nuestra vuestro vuestra
this that and for are but not with you all can had her was one our
the of in to a is it on have has we be or an i we they he she its
""".split())


def clean_html(text):
    """Remueve etiquetas HTML usando lxml cuando está disponible."""
    if "lxml" in str(type(text)):
        return text
    try:
        from lxml import html
        doc = html.fromstring(f"<div>{text}</div>")
        return doc.text_content()
    except:
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'&[a-zA-Z]+;', ' ', text)
        return text


def clean_text(text):
    """
    Pipeline de limpieza completo.
    """
    text = clean_html(text)
    text = text.lower()
    text = re.sub(r'[^\w\sáéíóúñü]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text):
    """Divide texto en tokens, filtra vacíos y stopwords, aplica stemming."""
    tokens = text.split()
    filtered = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    return [stem_token(t) for t in filtered]


def preprocess_article(article):
    """
    Limpia título y resumen de un artículo.
    Devuelve artículo con campos limpios + tokens.
    """
    title_raw = article.get("title", "")
    summary_raw = article.get("summary", "")
    
    title_clean = clean_text(title_raw)
    summary_clean = clean_text(summary_raw)
    
    # tokens combinados título + resumen
    combined = f"{title_clean} {summary_clean}"
    tokens = tokenize(combined)
    
    processed = dict(article)
    processed.update({
        "title_clean": title_clean,
        "summary_clean": summary_clean,
        "tokens": tokens,
        "token_count": len(tokens),
    })
    
    return processed


def run(input_path="data/dataset_crudo.json", output_path="data/dataset_limpio.json"):
    """
    Procesa dataset crudo y guarda versión limpia.
    """
    print("=" * 60)
    print("FASE 2: PREPROCESAMIENTO NLP")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        dataset = json.load(f)
    
    articles = dataset["articles"]
    print(f"Artículos a procesar: {len(articles)}")
    print()
    
    processed = []
    for i, art in enumerate(articles):
        if i < 3 or (i + 1) % 10 == 0:
            print(f"  [{i+1}/{len(articles)}] {art.get('title','')[:50]}...")
        processed.append(preprocess_article(art))
    
    print()
    
    token_counts = [a["token_count"] for a in processed]
    all_tokens = set()
    for a in processed:
        all_tokens.update(a["tokens"])
    
    print(f"📊 Estadísticas del corpus:")
    print(f"  Total artículos: {len(processed)}")
    print(f"  Vocabulario único: {len(all_tokens)} términos")
    print(f"  Promedio tokens/artículo: {sum(token_counts)/len(token_counts):.0f}")
    print(f"  Min tokens: {min(token_counts)}, Max tokens: {max(token_counts)}")
    print(f"  Stemming: Snowball (inglés/español)")
    print()
    
    output = {
        "metadata": {
            "original_articles": len(articles),
            "vocabulary_size": len(all_tokens),
            "avg_tokens": sum(token_counts) / len(token_counts),
        },
        "articles": processed,
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Corpus limpio guardado: {output_path}")
    
    return output


if __name__ == "__main__":
    run()
