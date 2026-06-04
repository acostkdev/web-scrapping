"""
ac2_analisis_discurso.py
AC-2: Nube de palabras y estadísticas de un discurso

Analiza textos largos: n-gramas, riqueza léxica por secciones,
entidades nombradas, y comparativa entre múltiples textos.
"""

import json
import re
from collections import Counter

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import bigrams, trigrams


class AnalisisDiscurso:
    def __init__(self, idioma='spanish'):
        self.stop_words = set(stopwords.words(idioma))
        self.idioma = idioma

    def analizar(self, texto, titulo="Documento"):
        oraciones = sent_tokenize(texto, language=self.idioma)
        tokens = word_tokenize(texto.lower(), language=self.idioma)
        tokens_alfa = [t for t in tokens if t.isalpha() and len(t) > 2]
        tokens_filtrados = [t for t in tokens_alfa if t not in self.stop_words]

        bigs = list(bigrams(tokens_filtrados))
        trigs = list(trigrams(tokens_filtrados))

        cuarto = max(len(tokens_filtrados) // 4, 1)
        riqueza_secciones = []
        for i in range(4):
            seccion = tokens_filtrados[i*cuarto:(i+1)*cuarto]
            if seccion:
                rl = len(set(seccion)) / len(seccion)
                riqueza_secciones.append(round(rl, 4))

        tokens_original = word_tokenize(texto, language=self.idioma)
        posibles_entidades = [
            t for t in tokens_original
            if t[0].isupper() and t.isalpha() and len(t) > 2
            and t.lower() not in self.stop_words
        ]

        return {
            'titulo': titulo,
            'oraciones': len(oraciones),
            'palabras_totales': len(tokens_alfa),
            'vocabulario_unico': len(set(tokens_filtrados)),
            'riqueza_lexica_global': round(
                len(set(tokens_filtrados)) / max(len(tokens_filtrados), 1), 4
            ),
            'riqueza_por_seccion': riqueza_secciones,
            'promedio_palabras_oracion': round(
                len(tokens_alfa) / max(len(oraciones), 1), 1
            ),
            'top_unigramas': Counter(tokens_filtrados).most_common(10),
            'top_bigramas': Counter(bigs).most_common(7),
            'top_trigramas': Counter(trigs).most_common(5),
            'posibles_entidades': Counter(posibles_entidades).most_common(8),
        }

    def comparar_textos(self, analisis_lista):
        comparativa = []
        for a in analisis_lista:
            comparativa.append({
                'titulo': a['titulo'],
                'palabras': a['palabras_totales'],
                'vocabulario': a['vocabulario_unico'],
                'riqueza': a['riqueza_lexica_global'],
                'promedio_oracion': a['promedio_palabras_oracion'],
            })
        return comparativa


TEXTOS = {
    "discurso_educacion": (
        "La educación es la herramienta más poderosa para transformar "
        "una sociedad. En México, la inversión en educación debe ser prioritaria para "
        "garantizar el desarrollo económico y social. Los jóvenes mexicanos merecen "
        "oportunidades de calidad en todos los niveles educativos. Las universidades "
        "tecnológicas y los institutos de investigación son pilares fundamentales para "
        "la innovación. La ciencia y la tecnología son motores del progreso nacional. "
        "El Instituto Tecnológico de Morelia ha formado generaciones de ingenieros que "
        "contribuyen al desarrollo del país. La inteligencia artificial y la programación "
        "son competencias esenciales para el futuro laboral. México necesita más "
        "profesionales en ciencias computacionales y recuperación de información."
    ),
    "texto_cientifico": (
        "El procesamiento de lenguaje natural permite a las computadoras "
        "comprender y generar texto humano. Los modelos de aprendizaje profundo como BERT "
        "y GPT han revolucionado este campo. La representación vectorial de documentos "
        "mediante TF-IDF sigue siendo fundamental para sistemas de recuperación de información. "
        "Los algoritmos de clasificación como Naive Bayes y SVM logran alta precisión en "
        "categorización de texto. El análisis de sentimientos combina técnicas léxicas con "
        "aprendizaje automático para determinar la polaridad emocional de un texto."
    ),
}


def run(output_path="data/ac2_analisis.json"):
    print("=" * 60)
    print("AC-2: ANALISIS ESTADISTICO DE DISCURSOS")
    print("=" * 60)
    print()

    analizador = AnalisisDiscurso()
    resultados = []

    for nombre, texto in TEXTOS.items():
        print(f"  Analizando: {nombre}")
        analisis = analizador.analizar(texto, nombre)
        resultados.append(analisis)

    for analisis in resultados:
        print(f"\n  --- {analisis['titulo']} ---")
        print(f"    Oraciones: {analisis['oraciones']}")
        print(f"    Palabras: {analisis['palabras_totales']}")
        print(f"    Vocabulario: {analisis['vocabulario_unico']}")
        print(f"    Riqueza léxica: {analisis['riqueza_lexica_global']}")
        print(f"    Prom. palabras/oración: {analisis['promedio_palabras_oracion']}")
        print(f"    Riqueza por sección: {analisis['riqueza_por_seccion']}")
        print(f"    Top bigramas: {analisis['top_bigramas'][:4]}")
        print(f"    Posibles entidades: {[e[0] for e in analisis['posibles_entidades'][:5]]}")

    print("\n  --- COMPARATIVA ---")
    comp = analizador.comparar_textos(resultados)
    for c in comp:
        print(f"    {c['titulo']:<25} Palabras:{c['palabras']:>4}  "
              f"Vocab:{c['vocabulario']:>4}  Riqueza:{c['riqueza']:.3f}  "
              f"P/Oracion:{c['promedio_oracion']:.1f}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"\n  Guardado: {output_path}")
    print()

    return resultados


if __name__ == "__main__":
    run()
