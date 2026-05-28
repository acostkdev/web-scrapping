"""
Mision C: Escribir Turtle y ver inferencia RDFS
Web Semantica - Actividades Extra
Usa rdflib para crear un grafo RDFS con datos universitarios
y hace inferencia basica de tipos.
"""

try:
    import rdflib
    from rdflib import Graph, Namespace, RDF, RDFS, Literal
    from rdflib.plugins.sparql import prepareQuery
except ImportError:
    print("rdflib no esta instalado. Ejecuta: pip install rdflib")
    exit(1)


EX = Namespace("http://example.org/universidad/")

g = Graph()
g.bind("ex", EX)

turtle_str = """
@prefix ex: <http://example.org/universidad/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Alicia rdf:type ex:Profesor .
ex:Bob rdf:type ex:Estudiante .

ex:Profesor rdfs:subClassOf ex:Persona .
ex:Estudiante rdfs:subClassOf ex:Persona .

ex:MatematicasI rdf:type ex:Asignatura .
ex:Alicia ex:ensena ex:MatematicasI .

ex:ensena rdf:type rdf:Property .
ex:ensena rdfs:domain ex:Profesor .
ex:ensena rdfs:range ex:Asignatura .

ex:Alicia ex:nombre "Alicia Garcia"@es .
"""

g.parse(data=turtle_str, format="turtle")

print("=" * 60)
print("MISION C: TURTLE E INFERENCIA RDFS")
print("=" * 60)
print(f"\nTriples cargados: {len(g)}")
print()

print("--- TODOS LOS TRIPLES ---")
for s, p, o in g:
    print(f"  {s}  {p}  {o}")

g_inferido = Graph()
g_inferido = g + g_inferido

from rdflib.util import guess_format

print("\n--- INFERENCIA BASICA (propagacion de rdfs:subClassOf) ---")
for s, p, o in g.triples((None, RDFS.subClassOf, None)):
    for sujeto in g.subjects(RDF.type, s):
        if (sujeto, RDF.type, o) not in g:
            g_inferido.add((sujeto, RDF.type, o))
            print(f"  Inferido: {sujeto} rdf:type {o}")

print(f"\nTriples incluyendo inferencia: {len(g_inferido)}")
print("\n--- TRIPLES DEL GRAFO INFERIDO ---")
for s, p, o in g_inferido:
    if (s, p, o) not in g:
        print(f"  [INF] {s}  {p}  {o}")

print("\n--- FIN MISION C ---")
