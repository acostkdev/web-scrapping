"""
Ejercicio: Reducción de Dimensionalidad (PCA y SVD)
Bloque 4 - Ejercicios Prácticos de Python

Objetivo: Aplicar PCA y SVD para reducir dimensiones en un corpus de texto
y visualizar cómo se agrupan los documentos en 2D.
Utilizamos TF-IDF como representación inicial, luego reducimos.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA, TruncatedSVD


def ejecutar_reduccion():
    """Ejecuta PCA y SVD sobre un corpus de ejemplo y grafica los resultados."""
    
    documento = [
        "Inteligencia artificial y machine learning transforman la industria",
        "Redes neuronales profundas para clasificación de imágenes",
        "Procesamiento de lenguaje natural con transformers y BERT",
        "La computación en la nube escala recursos bajo demanda",
        "Arquitectura serverless reduce costos operativos en la nube",
        "Microservicios y contenedores facilitan despliegues continuos",
        "Vecinos cercanos clustering K-means análisis de datos",
        "Métodos de clasificación supervisada como SVM y random forest",
        "Predicción de series temporales con modelos autorregresivos",
        "Deep learning aplicado a visión por computadora",
        "Optimización de hiperparámetros con grid search y Bayesian optimization",
        "Ataques de phishing detectados mediante algoritmos de ML",
        "El coche autónomo usa visión artificial para navegación",
        "Chatbots con modelos de lenguaje generativos",
        "Aprendizaje reforzado para juegos y robótica",
        "Bases de datos NoSQL como MongoDB y Cassandra",
        "API RESTful y GraphQL para comunicación entre servicios",
        "Docker y Kubernetes orquestan contenedores en producción",
        "Ciberseguridad con detección de anomalías en redes",
        "Ética y sesgo en algoritmos de inteligencia artificial",
    ]
    
    doc_etiquetas = [
        "ML", "Deep Learning", "NLP", "Cloud", "Cloud",
        "Cloud", "ML", "ML", "ML", "Computer Vision",
        "ML", "Security", "Computer Vision", "NLP", "RL",
        "DB", "API", "DevOps", "Security", "Ethics"
    ]
    
    print("=" * 70)
    print("EJERCICIO: REDUCCIÓN DE DIMENSIONALIDAD PCA/SVD")
    print("=" * 70)
    print()
    
    # paso 1: vectorizar con TF-IDF
    print("vectorizando {0} documentos con TF-IDF...".format(len(documento)))
    vectorizador = TfidfVectorizer(max_features=100, stop_words="english")
    matriz_tfidf = vectorizador.fit_transform(documento)
    vocab_size = matriz_tfidf.shape[1]
    print("  vocabulario: {0} términos".format(vocab_size))
    print("  Matriz original: {0} docs x {1} dims".format(*matriz_tfidf.shape))
    print()
    
    # paso 2: aplicar PCA (densifica la matriz)
    print("PLICANDO PCA (50 componentes → 2)...")
    pca = PCA(n_components=2, random_state=42)
    pca_denso = matriz_tfidf.toarray()
    coords_pca = pca.fit_transform(pca_denso)
    varianza_explicada = pca.explained_variance_ratio_
    print("  Varianza explicada PC1: {0:.2%}".format(varianza_explicada[0]))
    print("  Varianza explicada PC2: {0:.2%}".format(varianza_explicada[1]))
    print("  Varianza total 2D: {0:.2%}".format(sum(varianza_explicada)))
    print()
    
    # paso 3: aplicar SVD (trabaja directo sobre sparse)
    print("APLICANDO SVD (TruncatedSVD, 50 componentes → 2)...")
    svd = TruncatedSVD(n_components=2, random_state=42)
    coords_svd = svd.fit_transform(matriz_tfidf)
    varianza_svd = svd.explained_variance_ratio_
    print("  Varianza explicada SVD1: {0:.2%}".format(varianza_svd[0]))
    print("  Varianza explicada SVD2: {0:.2%}".format(varianza_svd[1]))
    print("  Varianza total 2D (SVD): {0:.2%}".format(sum(varianza_svd)))
    print()
    
    # paso 4: graficar comparativa PCA vs SVD
    print("GENERANDO GRÁFICAS...")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    categorias = list(set(doc_etiquetas))
    colores = plt.cm.tab10(np.linspace(0, 1, len(categorias)))
    color_map = {cat: colores[i] for i, cat in enumerate(categorias)}
    
    # PCA plot
    ax = axes[0]
    for i, label in enumerate(doc_etiquetas):
        ax.scatter(coords_pca[i, 0], coords_pca[i, 1],
                   color=color_map[label], label=label if label not in [l for l in doc_etiquetas[:i]] else "",
                   alpha=0.8, s=60)
        ax.annotate(str(i+1), (coords_pca[i, 0], coords_pca[i, 1]),
                    fontsize=8, xytext=(3, 3), textcoords="offset points")
    ax.set_title("PCA (varianza: {0:.1%})".format(sum(varianza_explicada)))
    ax.set_xlabel("PC1 ({0:.1%})".format(varianza_explicada[0]))
    ax.set_ylabel("PC2 ({0:.1%})".format(varianza_explicada[1]))
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
    ax.axvline(0, color="gray", linestyle="--", linewidth=0.5)
    ax.legend(fontsize=7, loc="best")
    
    # SVD plot
    ax = axes[1]
    for i, label in enumerate(doc_etiquetas):
        ax.scatter(coords_svd[i, 0], coords_svd[i, 1],
                   color=color_map[label], label=label if label not in [l for l in doc_etiquetas[:i]] else "",
                   alpha=0.8, s=60)
        ax.annotate(str(i+1), (coords_svd[i, 0], coords_svd[i, 1]),
                    fontsize=8, xytext=(3, 3), textcoords="offset points")
    ax.set_title("SVD (varianza: {0:.1%})".format(sum(varianza_svd)))
    ax.set_xlabel("SVD1 ({0:.1%})".format(varianza_svd[0]))
    ax.set_ylabel("SVD2 ({0:.1%})".format(varianza_svd[1]))
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.5)
    ax.axvline(0, color="gray", linestyle="--", linewidth=0.5)
    ax.legend(fontsize=7, loc="best")
    
    plt.suptitle("Reducción de Dimensionalidad: PCA vs SVD sobre corpus TF-IDF", fontsize=13)
    plt.tight_layout()
    plt.savefig("pca_svd_comparison.png", dpi=150)
    print("  Gráfica guardada: pca_svd_comparison.png")
    plt.close()
    
    # análisis por categoría
    print()
    print("ANÁLISIS DE CLUSTERS POR CATEGORÍA:")
    from collections import Counter
    print()
    
    # mostrar qué documentos se agrupan cerca en PCA
    print("  PCA - Documentos que quedaron cerca entre sí:")
    distancias_pca = []
    for i in range(len(coords_pca)):
        for j in range(i+1, len(coords_pca)):
            dist = np.linalg.norm(coords_pca[i] - coords_pca[j])
            distancias_pca.append((dist, i, j, doc_etiquetas[i], doc_etiquetas[j]))
    distancias_pca.sort()
    
    for dist, i, j, cat_i, cat_j in distancias_pca[:5]:
        print("    #{0} y #{1} ({2}, {3}): distancia={4:.3f}".format(i+1, j+1, cat_i, cat_j, dist))
    print()
    
    print("=" * 70)
    print("EJERCICIO COMPLETADO")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_reduccion()
