"""
fase7_knowledge_graph.py
Sistema de Monitoreo de Noticias - Fase 7

Construye un grafo de conocimiento basado en co-ocurrencia de
entidades (palabras capitalizadas, nombres propios) dentro de los artículos.
Usa networkx para modelar el grafo.
"""

import json
import re
from collections import defaultdict
import networkx as nx

# spaCy NER: disponible si el modelo está instalado
try:
    import spacy
    _nlp = spacy.load("es_core_news_sm", disable=["parser", "lemmatizer"])
    USANDO_SPACY = True
except:
    _nlp = None
    USANDO_SPACY = False


def extract_entities(text):
    """
    Extrae entidades candidatas.
    Usa spaCy NER si está disponible, fallback a regex.
    """
    if USANDO_SPACY and _nlp:
        doc = _nlp(text[:100000])  # limitar longitud
        entities = list(set(ent.text.strip() for ent in doc.ents))
        return [e for e in entities if len(e) > 2]

    matches = re.findall(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,3}', text)
    filtered = []
    for m in matches:
        words = m.split()
        if len(words) >= 2 or (len(m) > 3 and m[0].isupper()):
            filtered.append(m.strip())
    return filtered


def build_graph(articles, min_cooccurrence=2):
    """
    Construye grafo de co-ocurrencia de entidades.
    Nodos = entidades, Aristas = co-aparición en mismo artículo.
    """
    G = nx.Graph()
    
    doc_entities = []
    for art in articles:
        text = f"{art.get('title', '')} {art.get('summary', '')}"
        entities = extract_entities(text)
        # filtrar entidades únicas por documento
        unique_entities = list(set(entities))
        doc_entities.append(unique_entities)
        
        for ent in unique_entities:
            if not G.has_node(ent):
                G.add_node(ent, weight=1)
            else:
                G.nodes[ent]["weight"] += 1
    
    # co-ocurrencias: si dos entidades aparecen juntas en ≥N documentos
    cooc = defaultdict(int)
    for entities in doc_entities:
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                pair = tuple(sorted([entities[i], entities[j]]))
                cooc[pair] += 1
    
    for (e1, e2), count in cooc.items():
        if count >= min_cooccurrence:
            G.add_edge(e1, e2, weight=count)
    
    return G


def graph_summary(G):
    """Resumen del grafo."""
    if G.number_of_nodes() == 0:
        return "Grafo vacío"
    
    top_nodes = sorted(G.nodes(data=True), key=lambda x: -x[1].get("weight", 0))[:10]
    top_edges = sorted(G.edges(data=True), key=lambda x: -x[2].get("weight", 0))[:10]
    
    lines = [
        f"Nodos: {G.number_of_nodes()}",
        f"Aristas: {G.number_of_edges()}",
        "",
        "Top entidades:",
    ]
    for node, data in top_nodes:
        lines.append(f"  {node} ({data.get('weight', 0)} docs)")
    
    if top_edges:
        lines.append("")
        lines.append("Top relaciones (co-ocurrencias):")
        for e1, e2, data in top_edges:
            lines.append(f"  {e1} ↔ {e2} ({data.get('weight', 0)} docs)")
    
    return "\n".join(lines)


def plot_graph(G, output="data/knowledge_graph.png"):
    """Visualiza el grafo de conocimiento."""
    if G.number_of_nodes() == 0:
        print("  Grafo vacío, no se genera gráfica")
        return
    
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(12, 8))
    
    pos = nx.spring_layout(G, k=0.5, iterations=30, seed=42)
    node_sizes = [G.nodes[n].get("weight", 1) * 80 for n in G.nodes()]
    edge_widths = [G.edges[e].get("weight", 1) * 0.5 for e in G.edges()]
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#4CAF50", alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.3, edge_color="#333")
    
    # labels solo para los nodos más importantes
    top_n = sorted(G.nodes(), key=lambda n: G.nodes[n].get("weight", 0), reverse=True)[:15]
    labels = {n: n for n in top_n}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Grafo de Conocimiento - Entidades y Relaciones", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    print(f"  Gráfica guardada: {output}")


def run(input_path="data/dataset_sentiment.json",
        graph_path="data/knowledge_graph.json",
        graphml_path="data/knowledge_graph.graphml"):
    
    print("=" * 60)
    print("FASE 7: GRAFO DE CONOCIMIENTO")
    print("=" * 60)
    print()
    
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)
    
    articles = data["articles"]
    metodo = "spaCy NER" if USANDO_SPACY else "regex (fallback)"
    print(f"Extrayendo entidades de {len(articles)} artículos...")
    print(f"  Método: {metodo}")
    
    G = build_graph(articles, min_cooccurrence=1)
    
    print()
    print("📊 Resumen del grafo:")
    print(graph_summary(G))
    print()
    
    # guardar como JSON
    graph_data = {
        "nodes": [{"id": n, "weight": G.nodes[n].get("weight", 1)} for n in G.nodes()],
        "edges": [{"source": u, "target": v, "weight": G.edges[u, v].get("weight", 1)}
                  for u, v in G.edges()],
    }
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Grafo JSON: {graph_path}")
    
    # guardar como GraphML
    try:
        nx.write_graphml(G, graphml_path)
        print(f"✅ Grafo GraphML: {graphml_path}")
    except:
        print("  ⚠ No se pudo guardar GraphML")
    
    # graficar
    plot_graph(G)
    
    return G


if __name__ == "__main__":
    run()
