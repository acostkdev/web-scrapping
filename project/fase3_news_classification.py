"""
fase3_news_classification.py
Sistema de Monitoreo de Noticias - Fase 3

Clasifica artículos en categorías usando TF-IDF + Naive Bayes.
Como el dataset no viene etiquetado, asignamos categorías basadas
en palabras clave del contenido (keyword matching). Esto crea
etiquetas para entrenar el clasificador supervisado.
"""

import json
import re
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt


# keywords por categoría para etiquetado automático
CATEGORY_KEYWORDS = {
    "tecnologia": ["python", "software", "ai", "inteligencia", "machine learning",
                   "web", "data", "algorithm", "code", "digital", "computacion",
                   "app", "startup", "robot", "automatizacion", "programacion"],
    "politica": ["gobierno", "presidente", "congreso", "eleccion", "partido",
                 "senado", "diputado", "mexico", "politica", "ley", "reforma",
                 "votacion", "candidato", "ministro", "democracia"],
    "salud": ["salud", "medico", "hospital", "enfermedad", "paciente", "virus",
              "vacuna", "tratamiento", "clinica", "medicina", "covid", "salud"],
    "negocios": ["mercado", "empresa", "economia", "inversion", "banco",
                 "finanzas", "bolsa", "comercio", "negocio", "acciones",
                 "dolar", "inflacion", "pib", "presupuesto"],
    "ciencia": ["investigacion", "estudio", "cientifico", "naturaleza",
                "universidad", "laboratorio", "experimento", "fisica",
                "biologia", "quimica", "espacio", "planeta"],
}

ALL_KEYWORDS = {kw for kws in CATEGORY_KEYWORDS.values() for kw in kws}


def assign_category(article):
    """
    Asigna categoría basada en keywords en título y resumen.
    Si hay múltiples matches, la que más keywords tenga gana.
    """
    text = f"{article.get('title_clean', '')} {article.get('summary_clean', '')}"
    
    scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in text)
        if score > 0:
            scores[cat] = score
    
    if not scores:
        return "general"
    
    return max(scores, key=scores.get)


def vectorize(texts):
    """Convierte textos a matriz TF-IDF."""
    vectorizer = TfidfVectorizer(
        lowercase=True,
        max_features=2000,
        ngram_range=(1, 2),
        stop_words=None,
    )
    X = vectorizer.fit_transform(texts) 
    return X, vectorizer


def run(input_path="data/dataset_limpio.json",
        model_path="models/classifier.pkl",
        vectorizer_path="models/vectorizer.pkl",
        output_path="data/dataset_clasificado.json"):
    
    print("=" * 60)
    print("FASE 3: CLASIFICACIÓN DE NOTICIAS")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    print(f"Artículos: {len(articles)}")
    print()
    
    # asignar categorías
    print("🏷️ Asignando categorías por keywords...")
    for art in articles:
        art["category"] = assign_category(art)
    
    cat_counts = {}
    for art in articles:
        c = art["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1
    
    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print()
    
    # preparar datos para entrenamiento
    texts = [
        f"{a.get('title_clean', '')} {a.get('summary_clean', '')}"
        for a in articles
    ]
    labels = [a["category"] for a in articles]
    
    # vectorizar
    print("🔨 Vectorizando con TF-IDF...")
    X, vectorizer = vectorize(texts)
    print(f"  Matriz: {X.shape[0]} textos × {X.shape[1]} términos")
    print()
    
    # entrenar clasificador
    print("🤖 Entrenando Naive Bayes...")
    model = MultinomialNB(alpha=0.1)
    model.fit(X, labels)
    print("  Modelo entrenado")
    print()
    
    # evaluación rápida (mismas X, pero muestra qué tan bien aprende)
    preds = model.predict(X)
    print("📊 Evaluación (accuracy en training set):")
    acc = (preds == np.array(labels)).mean()
    print(f"  Accuracy: {acc:.2%}")
    print()
    
    for cat in sorted(set(labels)):
        mask = np.array(labels) == cat
        cat_acc = (preds[mask] == np.array(labels)[mask]).mean()
        print(f"  {cat}: {cat_acc:.0%} ({mask.sum()} muestras)")
    
    print()
    
    # matriz de confusión
    print("📊 Generando matriz de confusión...")
    cm = confusion_matrix(labels, preds, labels=sorted(set(labels)))
    fig, ax = plt.subplots(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(set(labels)))
    disp.plot(ax=ax, cmap="Blues", colorbar=True)
    ax.set_title("Matriz de Confusión - Clasificación de Noticias")
    plt.tight_layout()
    plt.savefig("data/confusion_matrix.png", dpi=150)
    plt.close()
    print(f"  Matriz guardada: data/confusion_matrix.png")
    print()
    
    # guardar modelo y vectorizador
    Path(model_path).parent.mkdir(exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(vectorizer_path, "wb") as f:
        pickle.dump(vectorizer, f)
    
    # guardar dataset con categorías
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Modelo guardado: {model_path}")
    print(f"✅ Vectorizador: {vectorizer_path}")
    print(f"✅ Dataset clasificado: {output_path}")
    
    return model, vectorizer


def predict(text, model_path="models/classifier.pkl", vectorizer_path="models/vectorizer.pkl"):
    """Clasifica un texto nuevo usando modelo guardado."""
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)
    
    X = vectorizer.transform([text])
    probs = model.predict_proba(X)[0]
    pred = model.classes_[probs.argmax()]
    return pred, {c: float(p) for c, p in zip(model.classes_, probs)}


if __name__ == "__main__":
    run()
