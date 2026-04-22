# Ejercicio: Reducción de Dimensionalidad con PCA y SVD

## Qué Hicimos

PCA y SVD son técnicas para reducir la dimensionalidad de datos. En este ejercicio partimos de 20 documentos sobre tecnología (ML, Cloud, NLP, etc.) vectorizados con TF-IDF a **99 dimensiones** (términos). Luego reducimos eso a solo **2 dimensiones** para ver si los temas relacionados se agrupan solos.

### PCA vs SVD

- **PCA** (Principal Component Analysis): busca direcciones de máxima varianza. Densifica la matriz.
- **SVD** (TruncatedSVD): similar pero trabaja directo sobre matrices sparse, que es como TF-IDF guarda los datos.

Acá ambas hacen lo mismo: proyectar 99 dimensiones a 2 para visualización.

---

## Resultados

### Varianza Explicada

```
PCA: PC1=7.79% + PC2=6.96% = 14.75% total
SVD: SVD1=4.69% + SVD2=5.76% = 10.46% total
```

O sea que con 2D solo retenemos ~15% de la información original. Es normal. De 99 dimensiones a 2 se pierde mucha varianza. Para eso existe el codo de varianza (elegir cuántas dimensiones mantener, como 10 o 20).

### Agrupaciones

Los documentos que quedaron más cerca en el espacio 2D:

```
#3 y #9 (NLP, ML): distancia=0.000
#15 y #17 (RL, API): distancia=0.036
#4 y #5 (Cloud, Cloud): distancia=0.040
```

Cloud docs (#4 y #5) se agrupan bien juntos, que es lo esperado.

---

## Para Qué Sirve

- Visualización de datos de alta dimensión
- Compresión (reducir espacio de almacenamiento)
- Preprocesamiento para ML (menos dimensiones = menos overfitting)
- Análisis exploratorio (ver clusters naturales)

---

## Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `cw-bloque4-ejercicio-pca-svd.py` | Código del ejercicio |
| `pca_svd_comparison.png` | Gráfica comparativa PCA vs SVD |
