# Ejercicio: Análisis de Sentimientos en Español

## De Qué Va

Clasificar textos en español como **positivo**, **negativo** o **neutro** usando machine learning. Creamos nuestro propio dataset con 90 frases (30 de cada categoría) y entrenamos clasificadores con TF-IDF.

No usé librerías externas de sentimientos (como TextBlob o VADER) porque están enfocadas en inglés. En su lugar construí un pipeline completo: dataset → vectorización → entrenamiento → evaluación. Así se ve cómo funcionan estos sistemas desde cero.

---

## El Pipeline

1. **Dataset:** 90 textos etiquetados a mano en 3 categorías
2. **Vectorización:** TF-IDF con n-gramas de palabras (1 y 2 términos)
3. **Modelos:** Naive Bayes Multinomial y Logistic Regression
4. **Evaluación:** Precisión, recall, F1 y matriz de confusión
5. **Predicción:** Probar con frases nuevas no vistas

---

## Resultados

### Accuracy: ~55% (Naive Bayes / Logistic Regression)

Sobre 3 clases el azar daría 33%. 55% con solo 90 muestras no está mal para un ejercicio académico. Con más datos (500+ textos por categoría) esto subiría a 80-90%.

### Predicciones en Texto Nuevo

| Frase | Predicción | Confianza |
|-------|-----------|-----------|
| "Qué increíble experiencia, todo salió perfecto" | POSITIVO | 67%  |
| "Odio cuando esto pasa, es realmente molesto" | NEGATIVO | 51%  |
| "La junta técnica se llevará a cabo en la sala B" | NEUTRO | 69%  |
| "Estoy harto de esta situación, ya no aguanto más" | NEGATIVO | 67%  |
| "Feliz cumpleaños, que tengas un día maravilloso" | POSITIVO | 49%  |
| "El informe fue entregado exitosamente al cliente" | NEUTRO | 43%  |

Todas correctas. Las que tienen menos confianza son las que comparten vocabulario con otras categorías.

---

- Logistic Regression y Naive Bayes son buenos baseline para sentimientos
- Los n-gramas de palabras (unigramas + bigramas) capturan mejor el contexto
- Para español hay que hacer dataset propio porque las librerías existentes son inglés-céntricas
- El tamaño del dataset importa MUCHO: 90 textos apenas da para un prototipo
