#!/usr/bin/env python3
"""
main.py - Sistema Inteligente de Monitoreo y Análisis de Noticias Web 2026

Ejecuta pipeline completo: scraping → NLP → clasificación → sentimiento → búsqueda → grafo → reporte.

Uso:
    python3 main.py               # pipeline completo (Scrapy)
    python3 main.py --feedparser  # pipeline con feedparser (más rápido)
    python3 main.py --skip-scrape # saltar scraping
    python3 main.py --chat        # solo chatbot interactivo
    python3 main.py --report      # solo generar reporte
    python3 main.py --ac1         # AC-1: rastreo paginado (Hacker News)
    python3 main.py --ac2         # AC-2: análisis estadístico de discurso
    python3 main.py --ac3         # AC-3: clasificador multimodelo
    python3 main.py --ac4         # AC-4: análisis de hilo de discusión
    python3 main.py --ac5         # AC-5: comparación booleano vs vectorial
    python3 main.py --ac6         # AC-6: chatbot con memoria de contexto
    python3 main.py --ac7         # AC-7: enriquecimiento KG con Wikidata
"""

import os
import sys
from pathlib import Path

# cambiar al directorio del proyecto
os.chdir(Path(__file__).parent)

SCRAPE = "--skip-scrape" not in sys.argv
USE_SCRAPY = "--feedparser" not in sys.argv
CHAT_ONLY = "--chat" in sys.argv
REPORT_ONLY = "--report" in sys.argv
AC1 = "--ac1" in sys.argv
AC2 = "--ac2" in sys.argv
AC3 = "--ac3" in sys.argv
AC4 = "--ac4" in sys.argv
AC5 = "--ac5" in sys.argv
AC6 = "--ac6" in sys.argv
AC7 = "--ac7" in sys.argv


def title(msg):
    print()
    print("╔" + "═" * 58 + "╗")
    print(f"  {msg}")
    print("╚" + "═" * 58 + "╝")


def run_all():
    if AC1:
        title("AC-1: RASTREO CON PAGINACION")
        from ac1_scraper_paginado import run as run_ac1
        run_ac1()
        return

    if AC2:
        title("AC-2: ANALISIS ESTADISTICO DE DISCURSO")
        from ac2_analisis_discurso import run as run_ac2
        run_ac2()
        return

    if AC3:
        title("AC-3: CLASIFICADOR MULTIMODELO")
        from ac3_multimodelo import run as run_ac3
        run_ac3()
        return

    if AC4:
        title("AC-4: ANALISIS DE HILO DE DISCUSION")
        from ac4_hilo_discusion import run as run_ac4
        run_ac4()
        return

    if AC5:
        title("AC-5: COMPARACION BOOLEANO VS VECTORIAL")
        from ac5_comparacion_busqueda import run as run_ac5
        run_ac5()
        return

    if AC6:
        title("AC-6: CHATBOT CON MEMORIA DE CONTEXTO")
        from ac6_chatbot_contextual import run as run_ac6
        run_ac6()
        return

    if AC7:
        title("AC-7: ENRIQUECIMIENTO DEL KG CON WIKIDATA")
        from ac7_enriquecer_kg import run as run_ac7
        run_ac7()
        return

    if SCRAPE and not CHAT_ONLY and not REPORT_ONLY:
        title("FASE 1: SCRAPER DE FEEDS RSS")
        from fase1_scraper_feeds import run as run_f1, DEFAULT_FEEDS
        run_f1(DEFAULT_FEEDS, usar_scrapy=USE_SCRAPY)
    else:
        print("⏩ Fase 1 saltada")

    if not CHAT_ONLY and not REPORT_ONLY:
        title("FASE 2: PREPROCESAMIENTO NLP")
        from fase2_nlp_preprocessing import run as run_f2
        run_f2()

    if not CHAT_ONLY and not REPORT_ONLY:
        title("FASE 3: CLASIFICACIÓN DE NOTICIAS")
        from fase3_news_classification import run as run_f3
        run_f3()

    if not CHAT_ONLY and not REPORT_ONLY:
        title("FASE 4: ANÁLISIS DE SENTIMIENTOS")
        from fase4_sentiment_analysis import run as run_f4
        run_f4()

    if not CHAT_ONLY and not REPORT_ONLY:
        title("FASE 5: MOTOR DE BÚSQUEDA")
        from fase5_search_engine import run as run_f5
        run_f5()

    if CHAT_ONLY:
        title("FASE 6: CHATBOT")
        from fase6_chatbot import run as run_f6
        run_f6()
        return

    if not REPORT_ONLY:
        title("FASE 7: GRAFO DE CONOCIMIENTO")
        from fase7_knowledge_graph import run as run_f7
        run_f7()

    title("FASE 8: REPORTE")
    from fase8_reporting import run as run_f8
    run_f8()

    print()
    print("=" * 60)
    print("✅ SISTEMA COMPLETO")
    print("=" * 60)
    print("📁 Datos:   project/data/")
    print("📁 Modelos: project/models/")
    print("📄 Reporte: project/data/reporte.html")
    print("💬 Chatbot: python3 main.py --chat")


if __name__ == "__main__":
    run_all()
