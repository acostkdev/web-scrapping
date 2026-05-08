"""
Misión 2: Operación Vector de Consulta - Recuperación por TF-IDF
Expediente X v2: Sistemas de Recuperación de Información

Objetivo: Implementar búsqueda y ranking usando TF-IDF y similitud coseno.
Devolver top-3 documentos más relevantes frente a una consulta en lenguaje natural.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def ejecutar_mision2():
    """Ejecuta misión 2: búsqueda vectorial con TF-IDF."""
    
    # corpus para esta misión
    corpus_mision2 = {
        "a1": "Protocolo de evacuación silenciosa en instalaciones subterráneas.",
        "a2": "Guía de rutas de escape y puntos de reunión sin alarmas audibles.",
        "a3": "Receta de cocina: pasta con tomate y albahaca para el personal.",
        "a4": "Mapa de salidas de emergencia y señalética fotoluminiscente.",
        "a5": "Informe meteorológico: probabilidad de lluvia en la región este.",
    }
    
    consulta_mision2 = "evacuación silenciosa rutas de escape emergencia"
    
    print("=" * 70)
    print("MISIÓN 2: OPERACIÓN VECTOR DE CONSULTA - BÚSQUEDA POR TF-IDF")
    print("=" * 70)
    print()
    
    # paso 1: mostrar corpus
    print("📋 CORPUS (5 documentos):")
    for doc_id, texto in corpus_mision2.items():
        print(f"  {doc_id}: {texto}")
    print()
    
    # paso 2: mostrar consulta
    print(f"🔍 CONSULTA: \"{consulta_mision2}\"")
    print()
    
    # paso 3: preparar textos para vectorización
    # orden importante: documentos primero, consulta al final
    doc_ids = list(corpus_mision2.keys())
    documentos = [corpus_mision2[doc_id] for doc_id in doc_ids]
    textos_combinados = documentos + [consulta_mision2]
    
    print("🔨 VECTORIZANDO CON TF-IDF...")
    vectorizador = TfidfVectorizer(
        lowercase=True,
        stop_words=None,  # mantener todas las palabras para este análisis
        max_features=100
    )
    matriz_tfidf = vectorizador.fit_transform(textos_combinados)
    print(f"  Matriz TF-IDF: {matriz_tfidf.shape[0]} textos × {matriz_tfidf.shape[1]} términos")
    print()
    
    # paso 4: calcular similitud coseno
    # el último vector es la consulta
    vector_consulta = matriz_tfidf[-1]
    matriz_documentos = matriz_tfidf[:-1]
    
    # calcular similitud entre consulta y cada documento
    similitudes = cosine_similarity(vector_consulta, matriz_documentos)[0]
    
    # paso 5: crear ranking
    print("📊 CALCULANDO SIMILITUD COSENO:")
    ranking = []
    for idx, doc_id in enumerate(doc_ids):
        score = similitudes[idx]
        ranking.append((doc_id, score, documentos[idx]))
    
    # ordenar por similitud descendente
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    print()
    print("✅ RANKING FINAL (Top-3 documentos más relevantes):")
    print()
    
    for posicion, (doc_id, score, texto) in enumerate(ranking[:3], 1):
        print(f"  {posicion}. {doc_id}: {score:.4f}")
        print(f"     \"{texto}\"")
        print()
    
    # paso 6: análisis adicional
    print("📈 ANÁLISIS DEL RANKING COMPLETO (todos los documentos):")
    for doc_id, score, texto in ranking:
        print(f"  {doc_id}: {score:.4f}")
    print()
    
    print("=" * 70)
    print("FIN DE MISIÓN 2")
    print("=" * 70)
    
    return ranking


if __name__ == "__main__":
    ranking = ejecutar_mision2()
