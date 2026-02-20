# Actividades de Contexto: Evaluación, Credibilidad y Sesgo

**Actividad:** Bloque 1 (6-15)  
**Archivo:** `cw-bloque1-actividades-contexto.md`

---

Este documento cubre 10 actividades complementarias sobre temas de recuperación de información. En lugar de hacer 10 documentos separados (que serían repetitivos), las agrupo por temática con análisis práctico.

---

## 1. Evaluación de Fuentes en la Web

No toda fuente en internet es igual. Criterios para evaluar:

- **Autoridad:** ¿Quién publica? ¿Tiene credenciales?
- **Actualidad:** ¿La información está vigente?
- **Propósito:** ¿Informar, vender, convencer, manipular?
- **Precisión:** ¿Cita fuentes verificables?

Como scrapers, podemos automatizar parte de esta evaluación: extraer metadatos de autor, fecha de publicación, dominio, y número de fuentes citadas.

## 2. Credibilidad de la Información

La credibilidad no es binaria. Una fuente puede ser confiable en tecnología pero no en medicina. Factores:

- Reputación del dominio/medio
- Correcciones publicadas (una fuente que se corrige es MÁS confiable que una que nunca admite errores)
- Transparencia sobre metodología

## 3. Sesgo Informativo

Todo medio tiene sesgo. No es necesariamente malo si es transparente. Tipos:

- **Sesgo por omisión:** qué historias NO se cubren
- **Sesgo por selección:** qué ángulo se le da a una historia
- **Sesgo por fuente:** quién es citado como experto
- **Sesgo por titular:** el titular no coincide con el contenido

Podríamos analizar sesgo con scraping: extraer titulares de múltiples fuentes sobre el mismo tema y comparar el lenguaje usado.

## 4. Fuentes Primarias vs. Secundarias

En scraping es crucial distinguir:

- **Primaria:** El dato original (un comunicado de prensa, un paper, una base de datos oficial)
- **Secundaria:** Alguien que reporta sobre la fuente primaria (un artículo de noticias)

Siempre que sea posible, hay que ir a la fuente primaria.

## 5. Propagación de Contenido Falso

Cómo viaja la desinformación:
1. Se crea (generalmente por intereses políticos o económicos)
2. Se amplifica (bots, cuentas coordinadas, páginas falsas)
3. Se legitima (medios poco rigurosos la retoman sin verificar)
4. Se viraliza (el algoritmo la recomienda porque genera engagement)

## 6. Economía de la Atención

El modelo de negocio de internet se basa en capturar atención. Los titulares sensacionalistas, las noticias falsas y el contenido polarizante generan más clics que el contenido equilibrado. El algoritmo no es malo, simplemente optimiza para lo que paga: engagement.

## 7. Alfabetización Mediática

Habilidad para:
- Identificar fuentes confiables
- Distinguir hecho de opinión
- Reconocer técnicas de manipulación (apelación emocional, falsa equivalencia)
- Verificar antes de compartir

## 8. Impacto de la Desinformación en Democracias

Casos documentados:
- Brexit (2016): campañas coordinadas de desinformación en Facebook
- Elecciones EE.UU. (2016): interferencia rusa mediante contenido polarizante
- Brasil (2018): desinformación masiva vía WhatsApp
- México: guerra sucia digital en procesos electorales

## 9. Verificación Automatizada

Técnicas que relacionan directamente con el curso:
- TF-IDF para detectar patrones lingüísticos de desinformación
- Clustering (K-Means) para agrupar contenido sospechoso
- Similitud coseno para encontrar noticias duplicadas con titulares alterados
- Monitoreo RSS para detectar cambios en fuentes

## 10. Ética en la Recuperación de Información

Principios:
- No extraer datos personales sin consentimiento
- Respetar robots.txt y términos de servicio
- No sobrecargar servidores (rate limiting)
- Documentar la procedencia de los datos
- Reconocer limitaciones de los métodos

---

## Reflexión Final

Estas 10 actividades no requieren código porque son conceptuales, pero cada una tiene implicaciones directas en cómo diseñamos sistemas de scraping y recuperación de información. Un buen scraper no solo extrae datos, entiende el contexto de lo que está extrayendo y las implicaciones éticas de hacerlo.
