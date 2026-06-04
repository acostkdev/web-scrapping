"""
ac4_hilo_discusion.py
AC-4: Análisis de hilos de discusión de red social

Analiza un hilo de discusión: evolución del sentimiento,
detección de subtemas con clustering, resumen automático.
"""

import json
import re
from collections import Counter, defaultdict

from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class AnalizadorHiloDiscusion:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.mensajes = []

    def cargar_hilo(self, mensajes):
        self.mensajes = mensajes
        for msg in self.mensajes:
            scores = self.sia.polarity_scores(msg['texto'])
            msg['sentimiento'] = scores['compound']

    def evolucion_sentimiento(self, ventana=3):
        sentimientos = [m['sentimiento'] for m in self.mensajes]
        evolucion = []
        for i in range(len(sentimientos)):
            inicio = max(0, i - ventana + 1)
            promedio_ventana = sum(sentimientos[inicio:i+1]) / (i - inicio + 1)
            evolucion.append({
                'posicion': i + 1,
                'sentimiento_puntual': round(sentimientos[i], 3),
                'tendencia': round(promedio_ventana, 3),
            })
        return evolucion

    def detectar_subtemas(self, n_clusters=3):
        textos = [m['texto'] for m in self.mensajes]
        vec = TfidfVectorizer(max_features=500, stop_words='english')
        X = vec.fit_transform(textos)

        n_clusters = min(n_clusters, len(textos))
        km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = km.fit_predict(X)

        subtemas = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            subtemas[cluster_id].append(i)

        terminos = vec.get_feature_names_out()
        subtemas_info = {}
        for cluster_id, indices in subtemas.items():
            centroide = km.cluster_centers_[cluster_id]
            top_idx = centroide.argsort()[-5:][::-1]
            keywords = [terminos[j] for j in top_idx]
            subtemas_info[cluster_id] = {
                'keywords': keywords,
                'n_mensajes': len(indices),
            }

        return subtemas_info

    def usuarios_mas_activos(self, top_n=5):
        participacion = Counter(m['usuario'] for m in self.mensajes)
        return participacion.most_common(top_n)

    def resumen_hilo(self):
        total = len(self.mensajes)
        sent_promedio = sum(m['sentimiento'] for m in self.mensajes) / total
        positivos = sum(1 for m in self.mensajes if m['sentimiento'] > 0.05)
        negativos = sum(1 for m in self.mensajes if m['sentimiento'] < -0.05)

        hashtags = Counter()
        for m in self.mensajes:
            tags = re.findall(r'#(\w+)', m['texto'])
            hashtags.update(tags)

        return {
            'total_mensajes': total,
            'participantes': len(set(m['usuario'] for m in self.mensajes)),
            'sentimiento_promedio': round(sent_promedio, 3),
            'tono': ('positivo' if sent_promedio > 0.05
                     else 'negativo' if sent_promedio < -0.05 else 'mixto'),
            'positivos_pct': round(100 * positivos / total, 1),
            'negativos_pct': round(100 * negativos / total, 1),
            'hashtags_top': hashtags.most_common(5),
            'usuarios_activos': self.usuarios_mas_activos(3),
        }


HILO_IA = [
    {"usuario": "@dev_laura", "texto": "Just tried the new AI coding assistant and it's amazing! #AI #coding",
     "timestamp": "10:00"},
    {"usuario": "@tech_mike", "texto": "I agree, the code suggestions are incredibly accurate #AI",
     "timestamp": "10:05"},
    {"usuario": "@skeptic_joe", "texto": "But what about job displacement? This AI thing worries me a lot",
     "timestamp": "10:08"},
    {"usuario": "@dev_laura", "texto": "Good point Joe, but I think it's a tool not a replacement #AItools",
     "timestamp": "10:12"},
    {"usuario": "@data_sara", "texto": "The real concern is bias in training data, we need better datasets",
     "timestamp": "10:15"},
    {"usuario": "@tech_mike", "texto": "True, but the progress is undeniable. Exciting times! #innovation",
     "timestamp": "10:20"},
    {"usuario": "@skeptic_joe", "texto": "I lost my freelance gig because of AI. This is terrible for workers",
     "timestamp": "10:25"},
    {"usuario": "@prof_chen", "texto": "Research shows AI creates more jobs than it destroys historically",
     "timestamp": "10:30"},
    {"usuario": "@data_sara", "texto": "We need regulation and ethical guidelines urgently #AIethics",
     "timestamp": "10:35"},
    {"usuario": "@dev_laura", "texto": "Totally agree with Sara. Responsible AI development is key #responsible",
     "timestamp": "10:40"},
    {"usuario": "@tech_mike", "texto": "Companies investing in AI training for employees is the best approach",
     "timestamp": "10:45"},
    {"usuario": "@prof_chen", "texto": "Great discussion everyone! The future needs both innovation and responsibility",
     "timestamp": "10:50"},
]


def run(output_path="data/ac4_hilo_analisis.json"):
    print("=" * 60)
    print("AC-4: ANALISIS DE HILO DE DISCUSION")
    print("=" * 60)
    print()

    analizador = AnalizadorHiloDiscusion()
    analizador.cargar_hilo(HILO_IA)

    resumen = analizador.resumen_hilo()
    print("  Resumen del Hilo:")
    print(f"    Mensajes: {resumen['total_mensajes']}")
    print(f"    Participantes: {resumen['participantes']}")
    print(f"    Tono general: {resumen['tono']} ({resumen['sentimiento_promedio']:+.3f})")
    print(f"    Positivos: {resumen['positivos_pct']}% | Negativos: {resumen['negativos_pct']}%")
    print(f"    Hashtags: {resumen['hashtags_top']}")
    print(f"    Mas activos: {resumen['usuarios_activos']}")

    print("\n  Evolucion del Sentimiento:")
    evolucion = analizador.evolucion_sentimiento(ventana=3)
    for e in evolucion:
        barra = "+" * int(max(0, e['tendencia'] * 10))
        barra += "-" * int(max(0, -e['tendencia'] * 10))
        print(f"    Msg {e['posicion']:>2}: [{e['sentimiento_puntual']:+.2f}] "
              f"tendencia: {e['tendencia']:+.3f} |{barra}")

    print("\n  Subtemas Detectados:")
    subtemas = analizador.detectar_subtemas(n_clusters=3)
    for cluster_id, info in subtemas.items():
        print(f"    Subtema {cluster_id+1} ({info['n_mensajes']} msgs): {info['keywords']}")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "resumen": resumen,
            "evolucion": evolucion,
            "subtemas": {str(k): v for k, v in subtemas.items()},
            "mensajes": HILO_IA,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n  Guardado: {output_path}")
    print()

    return analizador


if __name__ == "__main__":
    run()
