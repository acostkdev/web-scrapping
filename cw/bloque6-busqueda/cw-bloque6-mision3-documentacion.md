# Misión 3: El Cifrado de Colección - Filtro Híbrido

**Agente Especial:** Aguirre Acosta Jesus Kevin | 20120951

---

## El Concepto: Por Qué Necesitamos un Filtro Híbrido

En Misión 1 usamos AND booleano. En Misión 2 usamos TF-IDF puro. Pero en la vida real la información tiene **datos** que no deberías ignorar.

La idea aquí es:
1. **Filtro booleano primero** (solo documentos con cierto metadato pasan)
2. **Ranking vectorial después** (TF-IDF + coseno sobre el subconjunto)

---

## El Problema

Tenemos 5 documentos con diferentes niveles de clasificación:

| Doc | Nivel | Texto |
|-----|-------|-------|
| x1 | PUBLICO | Boletín de prensa sobre obras... |
| x2 | **SIGILO** | Rumor operativo: el contacto cambió frecuencia... |
| x3 | PUBLICO | Convocatoria a curso de primeros auxilios... |
| x4 | **SIGILO** | Inventario de papelería y tóner... |
| x5 | RESERVADO | Lista de proveedores homologados... |

**Consulta:** "contacto frecuencia operativo handoff nocturno"

---

## Cómo lo Hice

### Filtro Booleano (Paso 1)

```python
documentos_sigilo = [doc for doc in documentos_mision3 if doc["nivel"] == "SIGILO"]
```

Simple. Solo los documentos con nivel exacto "SIGILO" pasan. Esto nos deja con **x2** y **x4**.

### TF-IDF + Similitud Coseno (Paso 2)

Misma técnica que Misión 2, pero aplicada solo a 2 documentos en lugar de 5. Más eficiente y más preciso.

```python
vectorizador = TfidfVectorizer(lowercase=True)
textos_con_consulta = textos_sigilo + [consulta_mision3]
matriz_tfidf = vectorizador.fit_transform(textos_con_consulta)

vector_consulta = matriz_tfidf[-1]
matriz_docs = matriz_tfidf[:-1]

similitudes = cosine_similarity(vector_consulta, matriz_docs)[0]
```

---

## Resultados

### Ranking de Documentos SIGILO

```
x2: 0.6222
x4: 0.0000
```

### Documento Ganador: **x2**

```
"Rumor operativo: el contacto cambió frecuencia; 
 verificar handoff nocturno. ###FIN###"
```

**Puntuación de similitud: 0.6222**

**¿Por qué ganó x2?**
- La consulta es "contacto frecuencia operativo handoff nocturno"
- x2 contiene PLABRAS CLAVE como "operativo", "contacto", "frecuencia", "handoff", "nocturno"
- x4 es inventario de papelería... no comparte NADA con la consulta
- Resultado: x2 gana por 0.6222 vs 0.0000

**Delimitador:** ###FIN###

---

## Por Qué el Filtro es Importante

| Documento | Texto | Similitud |
|-----------|-------|-----------|
| x1 | Obras en avenida ... tráfico lento | ~0.15 |
| x2 | Rumor operativo... | ~0.62 |
| x3 | Primeros auxilios voluntarios | ~0.10 |
| x4 | Papelería tóner almacén | ~0.00 |
| x5 | Proveedores catering | ~0.02 |

x2 gana igual, pero hay un problema: **documentos que no deberían estar en los resultados están compitiendo**. 


El filtro actúa como una **llave de acceso**:
- Los metadatos definen QUÉ documentos son candidatos
- El ranking define en qué ORDEN aparecen
- Esto previene "falsos positivos" semánticos

---

## Reflexión

En producción:

1. **Nunca** aplicas ranking sobre todo el universo de documentos
2. **Siempre** hay un paso previo de selección (filtro por metadatos, segmentación, etc.)
3. El resultado final es mejor tanto en precisión como en eficiencia

El filtro híbrido combina lo mejor del booleano (rápido, preciso en inclusión/exclusión) con lo mejor del vectorial (ranking fino, manejo de relevancia parcial).

