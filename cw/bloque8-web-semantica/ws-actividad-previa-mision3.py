"""
Mision 3: Mini-grafo en Python y consultas tipo SPARQL
Web Semantica - Actividad Previa
Implementa un grafo simple con listas de diccionarios
y un motor de consultas basico tipo SPARQL.
"""


def consulta_simple(grafo, patron):
    """
    Busca en el grafo triples que coincidan con el patron.
    patron es un dict con llaves s, p, o.
    None significa "cualquier valor" (comodin).
    Regresa una lista de diccionarios con las asignaciones.
    """
    resultados = []
    for triple in grafo:
        coincide = True
        for llave in ["s", "p", "o"]:
            if patron[llave] is not None:
                if triple[llave] != patron[llave]:
                    coincide = False
                    break
        if coincide:
            asignacion = {}
            for llave in ["s", "p", "o"]:
                if patron[llave] is None:
                    asignacion[llave] = triple[llave]
            if asignacion:
                resultados.append(asignacion)
            else:
                resultados.append(triple)
    return resultados


# Construimos el grafo
G = [
    {"s": "ex:alicia", "p": "rdf:type", "o": "ex:Persona"},
    {"s": "ex:alicia", "p": "ex:nombre", "o": "\"Alicia Garcia\""},
    {"s": "ex:alicia", "p": "ex:conoce", "o": "ex:bob"},
    {"s": "ex:alicia", "p": "ex:autor", "o": "ex:libro42"},
    {"s": "ex:bob", "p": "rdf:type", "o": "ex:Persona"},
    {"s": "ex:bob", "p": "ex:nombre", "o": "\"Bob Martinez\""},
    {"s": "ex:libro42", "p": "rdf:type", "o": "ex:Libro"},
    {"s": "ex:libro42", "p": "ex:titulo", "o": "\"Aventuras en la Web Semantica\""},
    {"s": "ex:libro42", "p": "ex:autor", "o": "ex:alicia"},
]

print("=" * 60)
print("MISION 3: MINI-GRAFO Y CONSULTAS TIPO SPARQL")
print("=" * 60)

# TAREA A: Encontrar autores del libro ex:libro42
print("\n--- TAREA A: Autores de ex:libro42 ---")
patron_a = {"s": None, "p": "ex:autor", "o": "ex:libro42"}
resultados_a = consulta_simple(G, patron_a)
for r in resultados_a:
    print(f"  Autor: {r['s']}")

# TAREA B: Encontrar todas las personas y sus nombres
print("\n--- TAREA B: Personas y sus nombres ---")
personas = consulta_simple(G, {"s": None, "p": "rdf:type", "o": "ex:Persona"})
for p in personas:
    nombre_patron = {"s": p["s"], "p": "ex:nombre", "o": None}
    nombres = consulta_simple(G, nombre_patron)
    for n in nombres:
        print(f"  Persona: {p['s']} -> Nombre: {n['o']}")

# Consulta adicional: todos los triples del grafo
print("\n--- TODOS LOS TRIPLES DEL GRAFO ---")
for t in G:
    print(f"  {t['s']}  {t['p']}  {t['o']}")

print("\n--- FIN MISION 3 ---")
