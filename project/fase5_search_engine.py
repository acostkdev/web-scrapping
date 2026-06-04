"""
fase5_search_engine.py
Sistema de Monitoreo de Noticias - Fase 5

Motor de búsqueda con índice invertido y ranking TF-IDF.
Permite buscar artículos por consultas en lenguaje natural.
"""

import json
import re
import pickle
import math
from collections import defaultdict


def build_inverted_index(articles):
    """
    Índice invertido: término → [(doc_id, tf), ...]
    TF = frecuencia del término en el documento.
    """
    index = defaultdict(list)
    
    for i, art in enumerate(articles):
        tokens = art.get("tokens", [])
        tf_counts = defaultdict(int)
        for t in tokens:
            tf_counts[t] += 1
        
        total_tokens = len(tokens)
        for term, count in tf_counts.items():
            tf = count / total_tokens if total_tokens > 0 else 0
            index[term].append((i, tf))
    
    return dict(index)


def build_tfidf_index(articles):
    """
    Precalcula TF-IDF para cada término en cada documento.
    """
    index = build_inverted_index(articles)
    n_docs = len(articles)
    
    # IDF por término
    idf_cache = {}
    for term, postings in index.items():
        df = len(postings)
        idf_cache[term] = math.log((n_docs + 1) / (df + 1)) + 1
    
    # TF-IDF por (doc_id, término)
    tfidf_index = {}
    for term, postings in index.items():
        idf = idf_cache[term]
        tfidf_index[term] = [(doc_id, tf * idf) for doc_id, tf in postings]
    
    return tfidf_index, idf_cache


def search(query, articles, vectorizer_path="models/vectorizer.pkl",
            model_path="models/classifier.pkl"):
    """
    Búsqueda por similitud TF-IDF.
    Si el clasificador está disponible, también devuelve categoría predicha.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    import pickle
    from pathlib import Path
    
    # cargar vectorizador
    try:
        with open(vectorizer_path, "rb") as f:
            vectorizer = pickle.load(f)
    except:
        vectorizer = TfidfVectorizer(lowercase=True, max_features=2000, ngram_range=(1, 2))
    
    texts = [f"{a.get('title_clean', '')} {a.get('summary_clean', '')}" for a in articles]
    
    X = vectorizer.fit_transform(texts + [query])
    query_vec = X[-1]
    doc_vecs = X[:-1]
    
    sims = cosine_similarity(query_vec, doc_vecs)[0]
    results = sorted(
        [(i, float(sims[i])) for i in range(len(articles))],
        key=lambda x: -x[1]
    )
    
    # cargar clasificador si existe
    cat_pred = None
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        q_vec = vectorizer.transform([query])
        cat_pred = model.classes_[model.predict(q_vec)[0]]
    except:
        pass
    
    return results, cat_pred


def run(input_path="data/dataset_sentiment.json",
        index_path="data/search_index.json"):
    
    print("=" * 60)
    print("FASE 5: MOTOR DE BÚSQUEDA")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    print(f"Indexando {len(articles)} artículos...")
    print()
    
    index, idf = build_tfidf_index(articles)
    
    index_data = {
        "metadata": {
            "n_docs": len(articles),
            "vocabulary": len(index),
        },
        "index": {term: postings for term, postings in list(index.items())[:100]},
        "top_terms": sorted(idf.items(), key=lambda x: -x[1])[:30],
    }
    
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Índice TF-IDF: {len(index)} términos")
    print(f"  Top términos por IDF (más discriminantes):")
    for term, val in index_data["top_terms"][:8]:
        print(f"    {term}: {val:.3f}")
    print()
    
    # demo de búsqueda
    queries = ["python", "mexico", "ai intelligence"]
    print("🔍 Demo de búsqueda:")
    for q in queries:
        results, cat = search(q, articles)
        top = results[0] if results else None
        if top:
            title = articles[top[0]].get("title", "")[:50]
            print(f"  \"{q}\" → [{top[1]:.3f}] {title}")
    print()
    
    print(f"✅ Índice guardado: {index_path}")
    
    return index


if __name__ == "__main__":
    run()
