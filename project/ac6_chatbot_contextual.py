"""
ac6_chatbot_contextual.py
AC-6: Interfaz conversacional con memoria de contexto

Chatbot que recuerda la conversación, detecta temas de interés
del usuario, y responde considerando el historial.
"""

import json
import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class MotorBusquedaSimple:
    def __init__(self, noticias):
        self.noticias = noticias
        self.textos = [f"{n['titulo']} {n.get('resumen', '')}" for n in noticias]
        self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
        self.matriz = self.vectorizer.fit_transform(self.textos) if self.textos else None

    def buscar_vectorial(self, consulta, top_k=5):
        if not self.matriz is None and self.matriz.shape[0] > 0:
            q_vec = self.vectorizer.transform([consulta])
            sims = cosine_similarity(q_vec, self.matriz)[0]
            indices = sims.argsort()[::-1][:top_k]
            resultados = []
            for i in indices:
                if sims[i] > 0:
                    n = self.noticias[i]
                    resultados.append({
                        'titulo': n['titulo'],
                        'snippet': n.get('resumen', n['titulo'])[:80],
                        'relevancia': round(float(sims[i]), 3),
                        'categoria': n.get('categoria', 'general'),
                    })
            return resultados
        return []


class ChatbotContextual:
    PALABRAS_TEMA = {
        'tecnologia': ['tecnología', 'ia', 'python', 'programación', 'software',
                       'coding', 'ai', 'programming', 'tech'],
        'economia': ['economía', 'mercado', 'finanzas', 'dinero', 'economy',
                     'market', 'finance', 'money', 'business'],
        'ciencia': ['ciencia', 'clima', 'investigación', 'science', 'research',
                    'climate', 'study'],
    }

    def __init__(self, noticias, motor_busqueda):
        self.noticias = noticias
        self.motor = motor_busqueda
        self.historial = []
        self.contexto_temas = Counter()

    def actualizar_contexto(self, pregunta, respuesta_tipo):
        self.historial.append({'pregunta': pregunta, 'tipo': respuesta_tipo})
        pregunta_lower = pregunta.lower()
        for tema, palabras in self.PALABRAS_TEMA.items():
            for p in palabras:
                if p in pregunta_lower:
                    self.contexto_temas[tema] += 1

    def responder(self, pregunta):
        pregunta_lower = pregunta.lower()

        if any(ref in pregunta_lower for ref in ['eso', 'esa', 'anterior',
                                                   'mas sobre', 'otra similar',
                                                   'otro', 'dime mas']):
            if self.historial:
                ultimo = self.historial[-1]
                pregunta_expandida = f"{ultimo['pregunta']} {pregunta}"
                resultados = self.motor.buscar_vectorial(pregunta_expandida, top_k=2)
                if resultados:
                    tipo = 'contextual'
                    resp = (f"Basandome en nuestra conversacion anterior, "
                            f"encontre: {resultados[0]['titulo']}")
                    self.actualizar_contexto(pregunta, tipo)
                    return resp

        resultados = self.motor.buscar_vectorial(pregunta, top_k=5)
        if resultados:
            if self.contexto_temas:
                tema_favorito = self.contexto_temas.most_common(1)[0][0]
                for r in resultados:
                    if r['categoria'] == tema_favorito:
                        tipo = 'personalizada'
                        resp = f"Como te interesa {tema_favorito}, mira esto: {r['titulo']}"
                        self.actualizar_contexto(pregunta, tipo)
                        return resp

            tipo = 'directa'
            resp = f"{resultados[0]['titulo']}. {resultados[0]['snippet']}"
            self.actualizar_contexto(pregunta, tipo)
            return resp

        tipo = 'fallback'
        resp = "No encontre algo especifico. Puedes darme mas detalles?"
        self.actualizar_contexto(pregunta, tipo)
        return resp

    def estadisticas_sesion(self):
        return {
            'interacciones': len(self.historial),
            'temas_interes': dict(self.contexto_temas.most_common()),
            'tipos_respuesta': dict(Counter(h['tipo'] for h in self.historial)),
        }


NOTICIAS_EJEMPLO = [
    {"titulo": "Nuevo framework de IA revoluciona el desarrollo de software",
     "resumen": "Un nuevo framework de inteligencia artificial permite a desarrolladores crear aplicaciones mas rapido",
     "categoria": "tecnologia"},
    {"titulo": "Mercados globales caen por tensiones comerciales",
     "resumen": "Las bolsas de valores alrededor del mundo registran caidas significativas",
     "categoria": "economia"},
    {"titulo": "Estudio revela impacto del cambio climatico en oceanos",
     "resumen": "Investigadores publican nuevo estudio sobre el calentamiento de los oceanos",
     "categoria": "ciencia"},
    {"titulo": "Python sigue siendo el lenguaje mas popular segun encuesta",
     "resumen": "Python mantiene su liderazgo en el indice de popularidad de lenguajes de programacion",
     "categoria": "tecnologia"},
    {"titulo": "Startups de tecnologia reciben financiamiento record",
     "resumen": "El sector de startups tecnologicas alcanza nuevo maximo en inversion de capital",
     "categoria": "economia"},
    {"titulo": "Nueva mision espacial explorara lunas de Jupiter",
     "resumen": "La NASA anuncia nueva mision para explorar Europa y Ganimedes",
     "categoria": "ciencia"},
]

CONVERSACION_EJEMPLO = [
    "Que noticias hay de tecnologia?",
    "Cuentame mas sobre eso",
    "Hay algo sobre inteligencia artificial?",
    "Y algo de economia?",
    "Dame otra noticia similar a la anterior",
]


def run(output_path="data/ac6_chatbot_sesion.json"):
    print("=" * 60)
    print("AC-6: CHATBOT CON MEMORIA DE CONTEXTO")
    print("=" * 60)
    print()

    motor = MotorBusquedaSimple(NOTICIAS_EJEMPLO)
    chatbot = ChatbotContextual(NOTICIAS_EJEMPLO, motor)

    print("  Conversation Demo:\n")
    for pregunta in CONVERSACION_EJEMPLO:
        respuesta = chatbot.responder(pregunta)
        print(f"    Usuario: {pregunta}")
        print(f"    Bot:     {respuesta}")
        print()

    stats = chatbot.estadisticas_sesion()
    print("  Estadisticas de sesion:")
    print(f"    Interacciones: {stats['interacciones']}")
    print(f"    Temas de interes: {stats['temas_interes']}")
    print(f"    Tipos de respuesta: {stats['tipos_respuesta']}")
    print()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "conversacion": CONVERSACION_EJEMPLO,
            "estadisticas": stats,
            "historial": chatbot.historial,
        }, f, indent=2, ensure_ascii=False)

    print(f"  Guardado: {output_path}")
    print()

    return chatbot


if __name__ == "__main__":
    run()
