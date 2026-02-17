## Qué es?

Verificar información es el proceso de confirmar si una afirmación es verdadera, falsa o engañosa usando evidencia verificable. No es nuevo (los periódicos siempre tuvieron correctores), pero con la velocidad de internet se volvió una disciplina en sí misma.

## Técnicas Comunes

1. **Verificación de fuentes:** ¿Quién lo dijo? ¿Es una fuente primaria? ¿Tiene historial de confiabilidad?
2. **Búsqueda inversa de imágenes:** Subir una imagen a Google Images o TinEye para ver si ha sido manipulada o está fuera de contexto
3. **Análisis de metadatos:** Fotos y documentos tienen metadatos EXIF que revelan fecha, cámara, ubicación, software de edición
4. **Corroboración cruzada:** La misma información aparece en múltiples fuentes independientes?
5. **Análisis de lenguaje:** Noticias falsas suelen usar lenguaje emocional extremo, mayúsculas sostenidas, signos de exclamación múltiples

## Herramientas Populares

| Herramienta | Para qué sirve |
|-------------|----------------|
| Google Fact Check Tools | Buscador de verificaciones ya publicadas |
| TinEye / Google Images | Búsqueda inversa de imágenes |
| Wayback Machine | Ver contenido original de una página aunque haya sido modificada o borrada |
| Bellingcat Toolkit | Colección de herramientas OSINT |
| Snopes / AFP Factual | Bases de datos de verificaciones |


## Mini-ejercicio Conceptual

Si quisieras verificar si una imagen fue sacada de contexto:
1. Extraes la URL de la imagen del artículo (scraping básico)
2. Haces búsqueda inversa (API de Google o script con requests)
3. Comparas fechas de publicación vs. fecha original de la imagen
4. Revisas si la imagen aparece en contextos diferentes
