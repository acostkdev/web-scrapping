"""
ac5_comparacion_busqueda.py
AC-5: Evaluación comparativa de modelos de búsqueda

Compara formalmente el modelo booleano vs. el modelo vectorial
usando las mismas consultas y métricas de precisión/recall.
"""

import json
import re
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class ComparadorModelos:
    def __init__(self, documentos):
        self.documentos = documentos
        self.textos = [f"{d['titulo']} {d['cuerpo']}" for d in documentos]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.matriz = self.vectorizer.fit_transform(self.textos)

        self.indice = {}
        for i, texto in enumerate(self.textos):
            for palabra in texto.lower().split():
                palabra = re.sub(r'[^\w]', '', palabra)
                if not palabra:
                    continue
                if palabra not in self.indice:
                    self.indice[palabra] = set()
                self.indice[palabra].add(i)

    def busqueda_booleana(self, consulta):
        terminos = consulta.lower().split()
        if not terminos:
            return []
        terminos_limpios = [re.sub(r'[^\w]', '', t) for t in terminos if t]
        if not terminos_limpios:
            return []
        resultado = self.indice.get(terminos_limpios[0], set()).copy()
        for t in terminos_limpios[1:]:
            resultado &= self.indice.get(t, set())
        return sorted(resultado)

    def busqueda_vectorial(self, consulta, top_k=5):
        q_vec = self.vectorizer.transform([consulta])
        sims = cosine_similarity(q_vec, self.matriz)[0]
        indices = sims.argsort()[::-1][:top_k]
        return [(int(i), round(float(sims[i]), 4)) for i in indices if sims[i] > 0]

    def evaluar_ambos(self, consulta, relevantes):
        bool_result = self.busqueda_booleana(consulta)
        bool_precision = len(set(bool_result) & set(relevantes)) / max(len(bool_result), 1)
        bool_recall = len(set(bool_result) & set(relevantes)) / max(len(relevantes), 1)

        vec_todos = [idx for idx, _ in self.busqueda_vectorial(consulta, top_k=len(self.documentos))]
        vec_top_k = vec_todos[:len(bool_result)] if bool_result else vec_todos[:3]
        vec_precision = len(set(vec_top_k) & set(relevantes)) / max(len(vec_top_k), 1)
        vec_recall = len(set(vec_top_k) & set(relevantes)) / max(len(relevantes), 1)

        return {
            'consulta': consulta,
            'booleano': {
                'recuperados': len(bool_result),
                'precision': round(bool_precision, 3),
                'recall': round(bool_recall, 3),
            },
            'vectorial': {
                'recuperados': len(vec_top_k),
                'precision': round(vec_precision, 3),
                'recall': round(vec_recall, 3),
            },
        }


NOTICIAS = [
    {"titulo": "IA y machine learning", "cuerpo": "inteligencia artificial deep learning redes neuronales transformers"},
    {"titulo": "Mercados financieros", "cuerpo": "inflacion tasas interes banco central politica monetaria mercados volatilidad"},
    {"titulo": "Cambio climatico", "cuerpo": "cambio climatico emisiones carbono calentamiento temperatura global cientifico"},
    {"titulo": "Datos abiertos gobierno", "cuerpo": "datos abiertos transparencia gobierno informacion publica"},
    {"titulo": "Ciberseguridad", "cuerpo": "ciberseguridad hackers vulnerabilidad proteccion datos privacidad"},
]


def run(output_path="data/ac5_comparacion.json"):
    print("=" * 60)
    print("AC-5: COMPARACION BOOLEANO VS VECTORIAL")
    print("=" * 60)
    print()

    comparador = ComparadorModelos(NOTICIAS)

    consultas_eval = [
        {"consulta": "inteligencia artificial", "relevantes": [0]},
        {"consulta": "mercados economia", "relevantes": [1]},
        {"consulta": "gobierno datos abiertos", "relevantes": [3]},
        {"consulta": "cientifico clima", "relevantes": [2]},
    ]

    print(f"{'Consulta':<30} | {'Modelo':<10} | {'Recup':>5} | {'Prec':>6} | {'Recall':>6}")
    print("-" * 75)

    sum_bool_p, sum_vec_p = 0, 0
    sum_bool_r, sum_vec_r = 0, 0
    resultados = []

    for ce in consultas_eval:
        resultado = comparador.evaluar_ambos(ce['consulta'], ce['relevantes'])
        resultados.append(resultado)
        b = resultado['booleano']
        v = resultado['vectorial']
        sum_bool_p += b['precision']
        sum_vec_p += v['precision']
        sum_bool_r += b['recall']
        sum_vec_r += v['recall']
        print(f"{ce['consulta']:<30} | {'Booleano':<10} | {b['recuperados']:>5} "
              f"| {b['precision']:>6.3f} | {b['recall']:>6.3f}")
        print(f"{'':30} | {'Vectorial':<10} | {v['recuperados']:>5} "
              f"| {v['precision']:>6.3f} | {v['recall']:>6.3f}")
        print()

    n = len(consultas_eval)
    print("-" * 75)
    print(f"{'PROMEDIO':<30} | {'Booleano':<10} | {'':>5} "
          f"| {sum_bool_p/n:.3f} | {sum_bool_r/n:.3f}")
    print(f"{'':30} | {'Vectorial':<10} | {'':>5} "
          f"| {sum_vec_p/n:.3f} | {sum_vec_r/n:.3f}")

    mejor = 'vectorial' if sum_vec_p > sum_bool_p else 'booleano'
    print(f"\n  Conclusion: El modelo {mejor} tiene mejor precision promedio.")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\n  Guardado: {output_path}")
    print()

    return resultados


if __name__ == "__main__":
    run()
