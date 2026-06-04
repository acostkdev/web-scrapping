"""
ac7_enriquecer_kg.py
AC-7: Enriquecimiento del Knowledge Graph con Wikidata

Conecta entidades del grafo de conocimiento local con Wikidata
usando RDF, owl:sameAs y consultas SPARQL.
"""

import json
import time
from pathlib import Path

from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, SKOS
from SPARQLWrapper import SPARQLWrapper, JSON


DATA = Namespace("http://simanw.org/data/")


class KnowledgeGraph:
    def __init__(self):
        self.graph = Graph()
        self.graph.bind("data", DATA)
        self.graph.bind("owl", OWL)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("skos", SKOS)

    def agregar_categoria(self, nombre, wikidata_id, etiqueta):
        sujeto = DATA[nombre]
        self.graph.add((sujeto, RDF.type, SKOS.Concept))
        self.graph.add((sujeto, RDFS.label, Literal(nombre, lang="es")))
        return sujeto

    def total_triples(self):
        return len(self.graph)


class EnriquecedorKG:
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.WD = Namespace("http://www.wikidata.org/entity/")
        self.WDT = Namespace("http://www.wikidata.org/prop/direct/")
        self.kg.graph.bind("wd", self.WD)
        self.kg.graph.bind("wdt", self.WDT)
        self.enlaces_externos = []

    def enlazar_entidad(self, entidad_local, wikidata_id, etiqueta):
        self.kg.graph.add((entidad_local, OWL.sameAs, self.WD[wikidata_id]))
        self.kg.graph.add((entidad_local, SKOS.exactMatch, self.WD[wikidata_id]))
        self.kg.graph.add((self.WD[wikidata_id], RDFS.label, Literal(etiqueta, lang="es")))
        self.enlaces_externos.append({
            'local': str(entidad_local).split('/')[-1],
            'wikidata': wikidata_id,
            'etiqueta': etiqueta,
        })

    def agregar_datos_externos(self, entidad_local, propiedades):
        for prop, valor in propiedades.items():
            self.kg.graph.add((entidad_local, self.WDT[prop], Literal(valor)))

    def consulta_enriquecimiento(self):
        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?local ?externo ?etiqueta
        WHERE {
            ?local owl:sameAs ?externo .
            ?externo rdfs:label ?etiqueta .
        }
        """
        return list(self.kg.graph.query(query))

    def generar_query_wikidata(self, tema):
        queries = {
            'tecnologia': """
# Herramientas de NLP en Wikidata
SELECT ?item ?itemLabel ?description WHERE {
  ?item wdt:P31 wd:Q7397 .          # instancia de software
  ?item wdt:P366 wd:Q30642 .        # uso: NLP
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
            'ciencia': """
# Articulos sobre cambio climatico
SELECT ?item ?itemLabel ?date WHERE {
  ?item wdt:P31 wd:Q13442814 .      # instancia de articulo cientifico
  ?item wdt:P921 wd:Q7942 .         # tema: cambio climatico
  ?item wdt:P577 ?date .
  FILTER(YEAR(?date) >= 2024)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en". }
}
LIMIT 10""",
        }
        return queries.get(tema, "# No hay consulta predefinida para este tema")


def run(output_path="data/ac7_kg_enriquecido.json", graphml_path="data/ac7_kg_enriquecido.rdf"):
    print("=" * 60)
    print("AC-7: ENRIQUECIMIENTO DEL KG CON WIKIDATA")
    print("=" * 60)
    print()

    kg = KnowledgeGraph()
    enriquecedor = EnriquecedorKG(kg)

    # Crear categorias del proyecto y enlazar a Wikidata
    categorias = [
        ("categoria_tecnologia", "Q11016", "Tecnologia de la informacion"),
        ("categoria_economia", "Q159810", "Economia"),
        ("categoria_ciencia", "Q336", "Ciencia"),
        ("categoria_politica", "Q7188", "Gobierno"),
        ("categoria_salud", "Q159121", "Salud"),
    ]

    for nombre, wid, etiqueta in categorias:
        sujeto = kg.agregar_categoria(nombre, wid, etiqueta)
        enriquecedor.enlazar_entidad(sujeto, wid, etiqueta)
        print(f"  Enlazado: {nombre} -> Wikidata:{wid} ({etiqueta})")

    # Agregar propiedades externas simuladas
    enriquecedor.agregar_datos_externos(DATA["categoria_tecnologia"], {
        "P279": "Sector economico terciario",
        "P910": "Categoria: Tecnologia de la informacion",
    })
    print("  Propiedades externas agregadas a categoria_tecnologia")

    print(f"\n  Triples totales: {kg.total_triples()}")
    print(f"  Enlaces externos: {len(enriquecedor.enlaces_externos)}")

    print("\n  Enlaces locales -> Wikidata (via SPARQL):")
    for resultado in enriquecedor.consulta_enriquecimiento():
        local = str(resultado[0]).split('/')[-1]
        externo = str(resultado[1]).split('/')[-1]
        etiqueta = str(resultado[2])
        print(f"    {local} -> {externo} ({etiqueta})")

    print("\n  Query sugerida para Wikidata (tecnologia):")
    print(enriquecedor.generar_query_wikidata('tecnologia'))

    # Guardar
    Path(output_path).parent.mkdir(exist_ok=True)

    graph_data = {
        "triples_totales": kg.total_triples(),
        "enlaces_externos": enriquecedor.enlaces_externos,
        "formato": "RDF/XML (OWL + SKOS)",
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print(f"  JSON guardado: {output_path}")

    kg.graph.serialize(destination=graphml_path, format="xml")
    print(f"  RDF/XML guardado: {graphml_path}")

    # Probar consulta real a Wikidata
    print("\n  Consultando Wikidata (top 3 software de NLP)...")
    sparql = SPARQLWrapper(
        "https://query.wikidata.org/sparql",
        agent="SIMANW-AC7/1.0"
    )
    sparql.setQuery("""
        SELECT ?itemLabel WHERE {
          ?item wdt:P31 wd:Q7397 .
          ?item wdt:P366 wd:Q30642 .
          SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }
        LIMIT 3
    """)
    sparql.setReturnFormat(JSON)

    intentos = 3
    for intento in range(intentos):
        try:
            results = sparql.query().convert()
            for r in results['results']['bindings']:
                print(f"    - {r.get('itemLabel', {}).get('value', 'N/A')}")
            break
        except Exception as e:
            espera = (intento + 1) * 10
            if "429" in str(e) and intento < intentos - 1:
                print(f"    Rate-limited, esperando {espera}s (intento {intento+2}/{intentos})...")
                time.sleep(espera)
            else:
                print(f"    Error de conexion: {e}")
                break
    print()

    return enriquecedor


if __name__ == "__main__":
    run()
