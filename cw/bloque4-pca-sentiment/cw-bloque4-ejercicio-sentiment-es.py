"""
Ejercicio: Análisis de Sentimientos en Español
Bloque 4 - Ejercicios Prácticos de Python

Clasifica textos en español como positivos, negativos o neutros
usando TF-IDF + clasificador supervisado.
Dataset ampliado para mejor precisión.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np


def ejecutar_sentiment():
    """Entrena clasificador de sentimientos en español y evalúa."""
    
    textos = [
        # ===== POSITIVOS (30) =====
        "Me encantó este curso, muy bien explicado todo",
        "Excelente servicio, lo recomiendo ampliamente",
        "La película está increíble, me fascinó la trama",
        "El producto superó mis expectativas, estoy feliz",
        "Qué gran noticia, me alegra mucho escuchar eso",
        "El equipo trabajó increíble, logramos el objetivo",
        "Me encanta la nueva versión, está mucho mejor",
        "La atención al cliente fue maravillosa",
        "Estoy muy agradecido por todo el apoyo recibido",
        "Este es el mejor restaurante de la ciudad",
        "La canción es hermosa, no dejo de escucharla",
        "Qué bonito lugar, definitivamente volveré",
        "Estoy feliz con los resultados obtenidos este mes",
        "Me fascina esta aplicación, es súper útil",
        "El servicio fue rápido y eficiente, muy contento",
        "Una experiencia increíble, superó todo lo que esperaba",
        "Recomiendo este hotel, la vista es espectacular",
        "Me encanta el nuevo diseño, es muy moderno",
        "El equipo es excelente, trabajan muy bien juntos",
        "La calidad del producto es impresionante",
        "Pasé unas vacaciones maravillosas en la playa",
        "El concierto estuvo genial, el mejor de mi vida",
        "Me siento agradecido por esta oportunidad única",
        "Los cambios implementados mejoraron todo el sistema",
        "Qué alegría recibir esta noticia tan esperada",
        "La obra de teatro es fantástica, muy recomendable",
        "Mi familia está feliz con la nueva casa",
        "El profesor explica muy bien, aprendo mucho",
        "Estoy emocionado por el viaje que viene",
        "Todo salió perfecto en la presentación final",
        
        # ===== NEGATIVOS (30) =====
        "Pésimo servicio, nunca había tenido una experiencia tan mala",
        "El producto llegó dañado, una decepción total",
        "La peor compra que he hecho, no lo recomiendo",
        "El software es terrible, lleno de errores",
        "La atención fue horrible, el personal es grosero",
        "Me enoja que siempre hagan lo mismo, es frustrante",
        "Qué pérdida de tiempo, no sirve para nada",
        "El curso fue aburrido y mal estructurado",
        "No me gustó para nada, esperaba mucho más",
        "El soporte técnico es inexistente, fatal",
        "La comida estaba fría y sin sabor, una basura",
        "El peor hotel donde me he hospedado",
        "Estoy harto de esta situación tan incómoda",
        "El servicio al cliente es deplorable, no contestan",
        "Qué decepción, esperaba mucho más de este producto",
        "El envío tardó semanas, una experiencia horrible",
        "No lo compres, es una estafa total",
        "El sistema falla constantemente, es inservible",
        "La atención médica fue terrible, muy poco profesional",
        "La aplicación se cierra sola todo el tiempo, fatal",
        "El vuelo se canceló sin previo aviso, terrible",
        "Qué mal servicio, no volveré nunca más",
        "El ruido del hotel no me dejó dormir, pésimo",
        "Los precios son excesivos para la calidad que ofrecen",
        "No cumplieron con lo prometido, una vergüenza",
        "La interfaz es confusa y difícil de usar",
        "Perdí mi dinero con esta compra, estoy enojado",
        "La reunión fue improductiva y aburrida",
        "Me arrepiento de haber comprado esto, es malísimo",
        "El trato que recibí fue grosero y desagradable",
        
        # ===== NEUTROS (30) =====
        "El evento se realizará el próximo jueves en la tarde",
        "La reunión está programada para las 3 pm",
        "El reporte fue entregado según lo acordado",
        "La versión 2.0 incluye nuevas funcionalidades",
        "El horario de atención es de lunes a viernes",
        "Se requiere registro previo para ingresar",
        "El documento está disponible en formato PDF",
        "La convocatoria cierra el 15 de diciembre",
        "Los resultados se publicarán en la página web",
        "El sistema se actualizará el fin de semana",
        "El pago puede realizarse en línea o en tienda",
        "La dirección fue confirmada por correo electrónico",
        "La sesión informativa será el martes a las 10 am",
        "El paquete incluye envío gratuito a todo el país",
        "La contraseña debe tener al menos 8 caracteres",
        "El formulario debe llenarse con datos verificables",
        "La junta directiva se reunirá mensualmente",
        "El costo total del proyecto se detalla en el anexo",
        "Los interesados deben enviar su solicitud antes del lunes",
        "El certificado se emite en un plazo de 10 días hábiles",
        "La política de devoluciones está publicada en el sitio web",
        "Se requiere firma del supervisor para autorizar el permiso",
        "El inventario se actualiza cada trimestre",
        "La capacitación está programada para la primera semana",
        "El informe incluye gráficas comparativas del periodo",
        "Los usuarios pueden registrarse con su correo electrónico",
        "El mantenimiento preventivo se realiza cada seis meses",
        "La encuesta estará disponible hasta el viernes",
        "El presupuesto fue aprobado por el comité financiero",
        "Las instrucciones están disponibles en tres idiomas",
    ]
    
    etiquetas = ["positivo"] * 30 + ["negativo"] * 30 + ["neutro"] * 30
    
    print("=" * 70)
    print("EJERCICIO: ANÁLISIS DE SENTIMIENTOS EN ESPAÑOL")
    print("=" * 70)
    print()
    print("DATASET: {0} textos ({1} por categoría)".format(
        len(textos), len(textos)//3))
    print()
    
    X_train, X_test, y_train, y_test = train_test_split(
        textos, etiquetas, test_size=0.3, random_state=42, stratify=etiquetas
    )
    print("  Train: {0} | Test: {1}".format(len(X_train), len(X_test)))
    print()
    
    print("VECTORIZANDO CON TF-IDF (word unigramas + bigramas)...")
    vectorizador = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=1000,
    )
    X_train_vec = vectorizador.fit_transform(X_train)
    X_test_vec = vectorizador.transform(X_test)
    print("  Vocabulario: {0} términos".format(X_train_vec.shape[1]))
    print()
    
    print("ENTRENANDO MODELOS:")
    print()
    
    modelos = {
        "Naive Bayes (Multinomial)": MultinomialNB(alpha=0.5),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, C=2.0),
    }
    
    resultados = {}
    
    for nombre, modelo in modelos.items():
        modelo.fit(X_train_vec, y_train)
        preds = modelo.predict(X_test_vec)
        acc = accuracy_score(y_test, preds)
        resultados[nombre] = {"preds": preds, "accuracy": acc}
        print("  {0:<35} → Accuracy: {1:.2%}".format(nombre, acc))
    
    print()
    
    mejor_nombre = max(resultados, key=lambda k: resultados[k]["accuracy"])
    mejor_modelo = modelos[mejor_nombre]
    
    print("MEJOR MODELO: {0}".format(mejor_nombre))
    print()
    
    print("REPORTE DE CLASIFICACIÓN ({0}):".format(mejor_nombre))
    mejor_preds = resultados[mejor_nombre]["preds"]
    print(classification_report(y_test, mejor_preds, digits=3))
    
    print("MATRIZ DE CONFUSIÓN:")
    clases = ["negativo", "neutro", "positivo"]
    cm = confusion_matrix(y_test, mejor_preds, labels=clases)
    print("{:>12}".format(""), end="")
    for c in clases:
        print("{:>10}".format(c), end="")
    print()
    for i, fila in enumerate(cm):
        print("{:>12}".format(clases[i]), end="")
        for v in fila:
            print("{:>10}".format(v), end="")
        print()
    print()
    
    frases_nuevas = [
        "Qué increíble experiencia, todo salió perfecto",
        "Odio cuando esto pasa, es realmente molesto",
        "La junta técnica se llevará a cabo en la sala B",
        "Estoy harto de esta situación, ya no aguanto más",
        "Feliz cumpleaños, que tengas un día maravilloso",
        "El informe fue entregado exitosamente al cliente",
    ]
    
    frases_vec = vectorizador.transform(frases_nuevas)
    predicciones = mejor_modelo.predict(frases_vec)
    probabilidades = mejor_modelo.predict_proba(frases_vec)
    clases_m = mejor_modelo.classes_
    
    print("PREDICCIONES EN TEXTO NUEVO:")
    for frase, pred, probs in zip(frases_nuevas, predicciones, probabilidades):
        proba_str = " | ".join(
            "{0}: {1:.0%}".format(c, p) for c, p in zip(clases_m, probs)
        )
        print("  \"{0}\"".format(frase))
        print("    → {0}  ({1})".format(pred.upper(), proba_str))
        print()
    
    print("TÉRMINOS MÁS INFORMATIVOS POR CATEGORÍA:")
    if hasattr(mejor_modelo, "coef_"):
        coefs = mejor_modelo.coef_
        feature_names = vectorizador.get_feature_names_out()
        for i, clase in enumerate(clases_m):
            top_n = 8
            top_indices = np.argsort(coefs[i])[-top_n:][::-1]
            top_terminos = [(feature_names[j], coefs[i][j]) for j in top_indices]
            print("  [{0}]".format(clase.upper()))
            for term, coef in top_terminos:
                print("    + {0}: {1:.3f}".format(term, coef))
            bottom_indices = np.argsort(coefs[i])[:top_n]
            bottom_terminos = [(feature_names[j], coefs[i][j]) for j in bottom_indices]
            for term, coef in bottom_terminos:
                print("    - {0}: {1:.3f}".format(term, coef))
            print()
    
    print("=" * 70)
    print("EJERCICIO COMPLETADO")


if __name__ == "__main__":
    ejecutar_sentiment()
