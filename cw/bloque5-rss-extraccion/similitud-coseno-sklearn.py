from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


documentos = [
    "El aprendizaje automatico es una rama de la inteligencia artificial que permite a las maquinas aprender sin ser programadas explicitamente",
    "La salud publica se enfoca en la prevencion de enfermedades y la promocion de estilos de vida saludables en la poblacion",
    "El futbol es uno de los deportes mas populares del mundo con millones de aficionados en todos los continentes",
    "Los sistemas de inteligencia artificial pueden analizar grandes volumenes de datos para encontrar patrones",
    "La educacion moderna incorpora tecnologias digitales para mejorar la experiencia de aprendizaje de los estudiantes",
    "El cambio climatico afecta a los ecosistemas y la biodiversidad del planeta de manera acelerada",
    "La inflacion es el aumento generalizado de precios en una economia durante un periodo determinado",
    "La educacion en linea ha crecido significativamente en los ultimos anos permitiendo el acceso al conocimiento",
    "El deporte profesional genera una industria multimillonaria que mueve recursos en todo el mundo",
    "La prevencion de enfermedades requiere politicas publicas efectivas y acceso a servicios de salud"
]


nombres = [
    "doc1_ia.txt",
    "doc2_salud.txt",
    "doc3_deportes.txt",
    "doc4_ia_datos.txt",
    "doc5_educacion.txt",
    "doc6_clima.txt",
    "doc7_economia.txt",
    "doc8_educacion_linea.txt",
    "doc9_deporte_industria.txt",
    "doc10_salud_prevencion.txt"
]


stop_words_es = ["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "es", "lo", "como", "mas", "pero", "sus", "le", "ya", "o", "este", "si", "porque", "este", "entre", "cuando", "muy", "sin", "sobre", "tambien", "me", "hasta", "hay", "donde", "quien", "desde", "todo", "son", "dos", "tiene", "era", "mucha", "cada", "ellos", "ellas", "nos", "les", "te", "mis", "tus", "sus"]
vectorizador = TfidfVectorizer(lowercase=True, stop_words=stop_words_es)
matriz_tfidf = vectorizador.fit_transform(documentos)


sim_matrix = cosine_similarity(matriz_tfidf)

print("Documentos cargados:")
for i, nombre in enumerate(nombres):
    print(f"{i}: {nombre}")

print("\nMatriz de similitud de coseno:")
for i in range(len(documentos)):
    fila = " ".join(f"{sim_matrix[i][j]:.3f}" for j in range(len(documentos)))
    print(f"  Doc{i}: {fila}")

if len(nombres) >= 2:
    print(
        f"\nSimilitud de coseno entre '{nombres[0]}' y '{nombres[1]}': "
        f"{sim_matrix[0, 1]:.4f}"
    )