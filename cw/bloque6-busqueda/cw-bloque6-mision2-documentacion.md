# Misión 2: Operación Vector de Consulta - TF-IDF

**Agente Especial:** Jesus Kevin Aguirre Acosta

---

## Qué es TF-IDF (y por qué no es tan complicado como suena)

TF-IDF es una fórmula que asigna un "peso" a cada palabra en un documento. La idea es simple:

- **TF (Term Frequency):** ¿Qué tan frecuente es una palabra en el documento? Si aparece mucho, tiene peso alto.
- **IDF (Inverse Document Frequency):** ¿Qué tan rara es la palabra en TODO el corpus? Si aparece en muchos documentos, su IDF es bajo (no es discriminante). Si aparece en pocos, su IDF es alto (muy discriminante).

**Ejemplo:**
- La palabra "el" aparece en TODOS los documentos → IDF bajo → no sirve para distinguir
- La palabra "evacuación" aparece en 1 o 2 documentos → IDF alto → excelente para distinguir

**La fórmula:** `TF-IDF = TF × IDF`

---

## Similitud Coseno: Cómo Comparar Documentos

Imagina que cada documento es un punto en el espacio. Cada palabra es una dimensión. El TF-IDF convierte cada documento en un vector (una posición en ese espacio).

Para encontrar documentos similares a una consulta, **medimos el ángulo entre su vector y el de cada documento**. Eso se llama similitud coseno.

- Ángulo pequeño (coseno cercano a 1) = documentos similares
- Ángulo grande (coseno cercano a 0) = documentos diferentes

Es lo que usan los motores de búsqueda para rankear resultados.

---

## Implementación Paso a Paso

### 1. Preparar los Textos

```python
corpus_mision2 = {
    "a1": "Protocolo de evacuación silenciosa en instalaciones subterráneas.",
    "a2": "Guía de rutas de escape y puntos de reunión sin alarmas audibles.",
    "a3": "Receta de cocina: pasta con tomate y albahaca para el personal.",
    "a4": "Mapa de salidas de emergencia y señalética fotoluminiscente.",
    "a5": "Informe meteorológico: probabilidad de lluvia en la región este.",
}

consulta_mision2 = "evacuación silenciosa rutas de escape emergencia"
```

Noten que a3 es una receta y a5 es un informe meteorológico. Nada que ver con evacuación. a1, a2 y a4 sí están relacionados.

### 2. Vectorizar con TF-IDF

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizador = TfidfVectorizer(
    lowercase=True,
    stop_words=None,
    max_features=100
)
matriz_tfidf = vectorizador.fit_transform(textos_combinados)
```

Esto:
- Crea un vector TF-IDF para cada texto
- Usa 36 términos únicos encontrados (dimensiones del espacio vectorial)
- Convierte todo a minúsculas

### 3. Calcular Similitud Coseno

```python
from sklearn.metrics.pairwise import cosine_similarity

vector_consulta = matriz_tfidf[-1]  # último vector (la consulta)
matriz_documentos = matriz_tfidf[:-1]  # todos excepto el último

similitudes = cosine_similarity(vector_consulta, matriz_documentos)[0]
```

Para cada documento, calcula cuán similar es a la consulta (valor entre 0 y 1).

### 4. Rankear

```python
ranking = []
for idx, doc_id in enumerate(doc_ids):
    score = similitudes[idx]
    ranking.append((doc_id, score, documentos[idx]))

ranking.sort(key=lambda x: x[1], reverse=True)
```

Ordena de mayor a menor similitud.

---

## Resultados

### Top-3 Documentos Más Relevantes:

```
1. a1: 0.3579
   "Protocolo de evacuación silenciosa en instalaciones subterráneas."

2. a2: 0.3398
   "Guía de rutas de escape y puntos de reunión sin alarmas audibles."

3. a4: 0.2419
   "Mapa de salidas de emergencia y señalética fotoluminiscente."
```

**Análisis:**

- **a1 es el ganador** porque contiene las palabras clave "evacuación" y "silenciosa" de la consulta.
- **a2 está cerca** porque tiene "rutas de escape" e "emergencia".
- **a4 es tercero** porque solo tiene "emergencia".
- **a3 y a5** están abajo porque son sobre cocina y meteorología. Tienen puntuaciones muy bajas (0.0344 y 0.0372).

### Ranking Completo:

```
a1: 0.3579  ← evacuación (match!)
a2: 0.3398  ← rutas de escape e emergencia (match!)
a4: 0.2419  ← emergencia (parcial)
a5: 0.0372  ← nada que ver
a3: 0.0344  ← nada que ver
```

---

## Por Qué Esto es Mejor que Búsqueda Booleana

Recuerden Misión 1, donde hacíamos AND booleano. Allí, una palabra o no estaba, o no estaba (binario).

Con TF-IDF:
- No necesitas que TODAS las palabras estén presentes
- Los documentos se rankean por relevancia parcial
- Las palabras raras pesan más (más discriminantes)
- Funciona bien incluso si la consulta es larga y vaga

Si con AND booleano no encontrábamos nadaEstudiante Web Scraping  

---

Solo:

1. Convierteles textos a vectores (pesos de palabras)
2. Mide ángulos entre vectores
3. Ranking automático

---
