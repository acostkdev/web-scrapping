"""
Mision D: Consultas SPARQL
Web Semantica - Actividades Extra
Ejecuta consultas SPARQL SELECT, ASK y FILTER sobre un grafo RDFS.
"""

try:
    import rdflib
    from rdflib import Graph, Namespace, RDF, RDFS, Literal
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
ex:Alicia ex:nombre "Alicia Garcia"@es .
ex:Bob ex:nombre "Bob Martinez"@en .
ex:MatematicasI rdf:type ex:Asignatura .
ex:Alicia ex:ensena ex:MatematicasI .
"""

g.parse(data=turtle_str, format="turtle")

print("=" * 60)
print("MISION D: CONSULTAS SPARQL")
print("=" * 60)
print(f"\nTriples en el grafo: {len(g)}")

# Consulta 1: SELECT - nombres de todas las Personas (inferidas o explicitas)
print("\n--- CONSULTA 1: Personas y sus nombres ---")
q1 = prepareQuery("""
    PREFIX ex: <http://example.org/universidad/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?persona ?nombre WHERE {
        ?persona rdf:type/rdfs:subClassOf* ex:Persona .
        ?persona ex:nombre ?nombre .
    }
""")
for r in g.query(q1):
    print(f"  {r.persona} -> {r.nombre}")

# Consulta 2: ASK - Bob es subClassOf Persona?
print("\n--- CONSULTA 2: Bob es subClassOf Persona? ---")
q2 = prepareQuery("""
    PREFIX ex: <http://example.org/universidad/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    ASK {
        ex:Bob rdfs:subClassOf ex:Persona .
    }
""")
resultado_ask = g.query(q2)
print(f"  Bob rdfs:subClassOf ex:Persona? {resultado_ask.askAnswer}")

# Consulta 3: SELECT con FILTER para nombres en espanol
print("\n--- CONSULTA 3: Nombres en espanol (@es) ---")
q3 = prepareQuery("""
    PREFIX ex: <http://example.org/universidad/>

    SELECT ?persona ?nombre WHERE {
        ?persona ex:nombre ?nombre .
        FILTER (LANG(?nombre) = "es")
    }
""")
for r in g.query(q3):
    print(f"  {r.persona} -> {r.nombre}")

print("\n--- FIN MISION D ---")
