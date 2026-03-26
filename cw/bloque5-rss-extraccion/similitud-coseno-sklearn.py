from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
import nltk
from nltk.corpus import stopwords
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def obtener_stopwords_spanish() -> List[str]:
    """Encapsula la obtención de stopwords para cumplir con Single Responsibility."""
    return stopwords.words('spanish')

def cargar_documentos(directorio: str) -> Tuple[List[str], List[str]]:
    """
    Carga de forma recursiva todos los archivos .json de un directorio.
    
    Aplica el principio DRY al utilizar rglob y maneja la extracción
    de datos de forma desacoplada.
    """
    base_path = Path(directorio)
    
    if not base_path.is_dir():
        raise ValueError(f"La ruta proporcionada no es un directorio válido: {directorio}")

    # rglob("*.json") equivale a glob("**//*.json"), buscando recursivamente
    filepaths = sorted(base_path.rglob("*.json"))

    nombres = []
    documentos = []

    for path in filepaths:
        try:
            # Encapsulamos la lectura para asegurar integridad
            contenido = path.read_text(encoding="utf-8")
            nombres.append(path.name)
            documentos.append(contenido)
        except (Exception, UnicodeDecodeError) as e:
            # En una arquitectura real, aquí usarías un Logger
            print(f"Error al procesar {path}: {e}")

    return nombres, documentos


def calcular_tfidf(documentos):
    """Calcula la matriz TF-IDF a partir de una lista de textos."""
    if not documentos:
        raise ValueError("La lista de documentos está vacía. No se puede calcular TF-IDF.")
    
    vectorizador = TfidfVectorizer(
        lowercase=True,      # pasar todo a minúsculas
        stop_words=obtener_stopwords_spanish()
    )
    matriz_tfidf = vectorizador.fit_transform(documentos)
    return matriz_tfidf, vectorizador


def matriz_similitud_coseno(matriz_tfidf):
    """Devuelve la matriz de similitud de coseno entre todos los documentos."""
    return cosine_similarity(matriz_tfidf)


if __name__ == "__main__":
    # 1. Cargar documentos
    nombres, documentos = cargar_documentos("investigation_output")

    # 2. Calcular TF-IDF
    matriz_tfidf, vectorizador = calcular_tfidf(documentos)

    # 3. Calcular similitud de coseno entre todos los pares de documentos
    sim_matrix = matriz_similitud_coseno(matriz_tfidf)

    # 4. Mostrar resultados
    print("Documentos cargados:")
    for i, nombre in enumerate(nombres):
        print(f"{i}: {nombre}")

    print("\nMatriz de similitud de coseno:")
    print(sim_matrix)

    # Ejemplo: similitud entre el documento 0 y el 1
    if len(nombres) >= 2:
        print(
            f"\nSimilitud de coseno entre '{nombres[0]}' y '{nombres[1]}': "
            f"{sim_matrix[0, 1]:.4f}"
        )