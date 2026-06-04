"""
ac3_multimodelo.py
AC-3: Clasificador multimodelo con selección automática

Entrena múltiples clasificadores (Naive Bayes, SVM, Logistic Regression,
Random Forest) y selecciona el mejor usando validación cruzada.
"""

import json
import pickle
from pathlib import Path

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold


class SelectorModelo:
    def __init__(self):
        self.modelos = {
            'Naive Bayes': MultinomialNB(alpha=0.1),
            'SVM Lineal': LinearSVC(max_iter=3000, C=1.0),
            'Logistic Regression': LogisticRegression(max_iter=1000, C=1.0),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        }
        self.vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
        self.mejor_modelo = None
        self.resultados = {}

    def evaluar_todos(self, textos, etiquetas, cv_folds=3):
        X = self.vectorizer.fit_transform(textos)
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

        for nombre, modelo in self.modelos.items():
            try:
                scores = cross_val_score(modelo, X, etiquetas, cv=cv, scoring='accuracy')
                self.resultados[nombre] = {
                    'accuracy_mean': round(scores.mean(), 4),
                    'accuracy_std': round(scores.std(), 4),
                    'scores': [round(s, 4) for s in scores.tolist()],
                }
            except Exception as e:
                self.resultados[nombre] = {'error': str(e)}

        validos = {k: v for k, v in self.resultados.items() if 'accuracy_mean' in v}
        if validos:
            mejor_nombre = max(validos, key=lambda k: validos[k]['accuracy_mean'])
            self.mejor_modelo = (mejor_nombre, self.modelos[mejor_nombre])
            self.mejor_modelo[1].fit(X, etiquetas)

        return self.resultados

    def predecir(self, textos):
        if not self.mejor_modelo:
            raise ValueError("Primero ejecuta evaluar_todos()")
        X = self.vectorizer.transform(textos)
        return self.mejor_modelo[1].predict(X)

    def reporte(self):
        lineas = ["Modelo                  | Accuracy   | Std Dev"]
        lineas.append("-" * 50)
        for nombre, res in sorted(
            self.resultados.items(),
            key=lambda x: x[1].get('accuracy_mean', 0),
            reverse=True
        ):
            if 'accuracy_mean' in res:
                marca = " ★" if self.mejor_modelo and nombre == self.mejor_modelo[0] else ""
                lineas.append(
                    f"{nombre:<23} | {res['accuracy_mean']:.4f}     | "
                    f"{res['accuracy_std']:.4f}{marca}"
                )
            else:
                lineas.append(
                    f"{nombre:<23} | ERROR      | {res.get('error', '')[:20]}"
                )
        return "\n".join(lineas)


DATOS = {
    "textos": [
        "inteligencia artificial deep learning redes neuronales transformers",
        "programacion software desarrollo aplicaciones web python javascript",
        "startup tecnologica innovacion digital plataforma cloud",
        "ciberseguridad hackers vulnerabilidad proteccion datos privacidad",
        "inflacion tasas interes banco central politica monetaria",
        "bolsa acciones mercado valores inversion rendimiento portafolio",
        "desempleo recesion economica crisis laboral empleo informal",
        "comercio exportaciones importaciones balanza aranceles tratado",
        "investigacion cientifica laboratorio experimento publicacion revista",
        "cambio climatico emisiones carbono calentamiento temperatura global",
        "vacuna medicamento ensayo clinico pacientes tratamiento hospital",
        "espacio cohete satelite mision astronauta exploracion lunar",
        "elecciones presidente candidato partido campana votacion democracia",
        "congreso legisladores reforma ley aprobacion dictamen senado",
        "seguridad policia crimen organizado justicia tribunal sentencia",
        "gobierno programa social presupuesto politica publica decreto",
    ],
    "etiquetas": [
        'tecnologia', 'tecnologia', 'tecnologia', 'tecnologia',
        'economia', 'economia', 'economia', 'economia',
        'ciencia', 'ciencia', 'ciencia', 'ciencia',
        'politica', 'politica', 'politica', 'politica',
    ],
    "prueba": [
        "nueva aplicacion de machine learning para detectar fraudes",
        "el presidente anuncio reformas al sistema de justicia",
        "los mercados cerraron con perdidas por tercer dia consecutivo",
    ],
}


def run(output_path="data/ac3_resultados.json", model_path="models/ac3_modelo.pkl"):
    print("=" * 60)
    print("AC-3: CLASIFICADOR MULTIMODELO")
    print("=" * 60)
    print()

    selector = SelectorModelo()
    resultados = selector.evaluar_todos(DATOS["textos"], DATOS["etiquetas"], cv_folds=3)

    print(selector.reporte())
    print(f"\n  Modelo seleccionado: {selector.mejor_modelo[0]}")

    print("\n  Predicciones con el mejor modelo:")
    predicciones = selector.predecir(DATOS["prueba"])
    for texto, pred in zip(DATOS["prueba"], predicciones):
        print(f"    [{pred}] {texto[:55]}...")

    Path(model_path).parent.mkdir(exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(selector, f)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "resultados": resultados,
            "mejor_modelo": selector.mejor_modelo[0] if selector.mejor_modelo else None,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n  Guardado: {output_path}")
    print()

    return selector


if __name__ == "__main__":
    run()
