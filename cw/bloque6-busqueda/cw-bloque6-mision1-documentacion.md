# Misión 1: La Telaraña de Tokens - Índice Invertido

**Agente Especial:** Jesus Kevin Aguirre Acosta  

---

## ¿Qué es un Índice Invertido?

Básicamente es como el índice al final de un libro, pero al revés. Si en un libro normal buscas "Capítulo 3" y encuentras una página, en un índice invertido buscas una **palabra** y obtienes **todos los documentos** donde aparece.

Por ejemplo:
- Índice normal: `Documento 1 → [palabra1, palabra2, palabra3]`
- Índice invertido: `palabra1 → [Documento 1, Documento 3]`

## Cómo Lo Implementé

El código tiene tres partes principales:

### 1. Limpiar y Tokenizar Texto

```python
def limpiar_y_tokenizar(texto):
    texto = texto.lower()
    for p in string.punctuation:
        texto = texto.replace(p, " ")
    return [t for t in texto.split() if t]
```

Lo que hace:
- Convierte todo a minúsculas (case-insensitive, así "Red" y "red" son lo mismo)
- Elimina puntuación (puntos, comas, etc.)
- Divide el texto en palabras individuales (tokens)

Es simple pero funciona bien para este caso. No usé regex complicado porque para una búsqueda booleana básica no lo necesita.

### 2. Construir el Índice Invertido

```python
def construir_indice_invertido(corpus):
    indice = {}
    
    for doc_id, texto in corpus.items():
        tokens = limpiar_y_tokenizar(texto)
        tokens_unicos = set(tokens)
        
        for token in tokens_unicos:
            if token not in indice:
                indice[token] = []
            indice[token].append(doc_id)
    
    for token in indice:
        indice[token].sort()
    
    return indice
```

Esto:
1. Recorre cada documento
2. Tokeniza el texto
3. Para cada palabra, añade el documento a la lista de "documentos que contienen esta palabra"
4. Ordena las listas para que sean predecibles

La estructura final es un diccionario donde:
- **Clave**: una palabra (término)
- **Valor**: lista de documentos que contienen esa palabra

### 3. Búsqueda Booleana AND

```python
def busqueda_booleana_and(indice, termino1, termino2):
    postings1 = set(indice.get(termino1.lower(), []))
    postings2 = set(indice.get(termino2.lower(), []))
    resultado = postings1 & postings2
    return sorted(list(resultado))
```

El AND booleano es una **intersección de conjuntos**. Si quieres documentos que tengan AMBAS palabras, necesitas los documentos que aparecen en ambas listas. El símbolo `&` en Python hace exactamente eso.

---

## Ejecución y Resultados

Usé este corpus para la prueba:

```python
corpus_mision1 = {
    "d1": "La red de agentes interceptó tráfico sospechoso en el nodo norte.",
    "d2": "El agente de campo reportó actividad normal en la red interna.",
    "d3": "Manual de procedimientos: la red no debe apagarse sin autorización.",
    "d4": "Mantenimiento programado del agente automático de respaldo.",
}
```

### Salida del Índice Invertido (muestra):

```
'agente' → ['d2', 'd4']
'red' → ['d1', 'd2', 'd3']
'manual' → ['d3']
'tráfico' → ['d1']
```

### Consulta: "agente" AND "red"

- Documentos con 'agente': d2, d4
- Documentos con 'red': d1, d2, d3
- **Intersección (AND):** d2

**Resultado:**
```
 ['d2']
```

El único documento que tiene AMBAS palabras es **d2: "El agente de campo reportó actividad normal en la red interna."**

---

## Por Qué Importa Esto

Un índice invertido es la base de cualquier motor de búsqueda. Sin él, cada búsqueda tendría que escanear TODOS los documentos línea por línea. Con un índice, accedes directamente a una lista pequeña de documentos relevantes.

También es lo que permite hacer búsquedas booleanas complejas: si quieres "agente AND red AND NOT automático", solo necesitas intersectar las listas del índice. Súper eficiente.

## Reflexión

Lo interesante aquí es que aunque el índice invertido parece complicado al principio, en realidad es solo:
1. Dividir textos en palabras
2. Recordar en qué documento aparece cada palabra
3. Usar eso para responder preguntas tipo "¿dónde aparece X?"

Es pragmático y funciona. La parte más importante es entender que estamos **invirtiendo** la relación: de "documento → palabras" a "palabra → documentos".

