"""
fase8_reporting.py
Sistema de Monitoreo de Noticias - Fase 8

Genera reporte HTML usando Jinja2 como template engine.
"""

import json
from datetime import datetime
from collections import Counter
from pathlib import Path
from jinja2 import Template, Environment, FileSystemLoader


def run(dataset_path="data/dataset_sentiment.json", output_path="data/reporte.html"):
    print("=" * 60)
    print("FASE 8: REPORTE Y VISUALIZACIÓN")
    print("=" * 60)
    print()
    
    with open(dataset_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    
    cats = Counter(a.get("category", "general") for a in articles)
    pols = Counter(a.get("sentiment", {}).get("polarity", "neutro") for a in articles)
    fuentes = set(a.get("source", "").split("/")[2] if "//" in a.get("source", "") else a.get("source", "") for a in articles)
    score_neto = sum(a.get("sentiment", {}).get("score", 0) for a in articles)
    
    # cargar template Jinja2
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("reporte.html")
    
    html = template.render(
        titulo="Sistema de Monitoreo de Noticias Web 2026",
        fecha=datetime.now().strftime("%Y-%m-%d %H:%M"),
        total=len(articles),
        fuentes=len(fuentes),
        categorias=len(cats),
        positivos=pols.get("positivo", 0),
        negativos=pols.get("negativo", 0),
        score_neto=f"{score_neto:+.2f}",
        categorias_list=cats.most_common(),
        articulos=articles,
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Reporte HTML generado: project/{output_path}")
    print(f"   Abre con: file://{Path(output_path).resolve()}")
    
    return html


if __name__ == "__main__":
    run()
