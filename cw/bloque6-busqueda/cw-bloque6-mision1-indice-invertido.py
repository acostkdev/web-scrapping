"""
Misión 1: La Telaraña de Tokens - Índice Invertido Básico
Expediente X v2: Sistemas de Recuperación de Información

Objetivo: Construir un índice invertido case-insensitive y resolver
una consulta booleana AND sobre un corpus de documentos.
"""

import string
import json


def limpiar_y_tokenizar(texto):
    """
    Convierte texto a minúsculas, elimina puntuación básica y devuelve tokens.
    Funciona bien para el caso de uso, sin overcomplicarse con regex avanzado.
    """
    texto = texto.lower()
    # remover puntuación simple
    for p in string.punctuation:
        texto = texto.replace(p, " ")
    # dividir por espacios y filtrar vacíos
    return [t for t in texto.split() if t]


def construir_indice_invertido(corpus):
    """
    Recibe diccionario {doc_id: texto} y devuelve índice invertido:
    {término: [lista de doc_id que contienen ese término]}
    
    La estructura es straightforward: para cada doc, tokenizamos y 
    registramos en qué documentos aparece cada palabra.
    """
    indice = {}
    
    for doc_id, texto in corpus.items():
        tokens = limpiar_y_tokenizar(texto)
        
        # evitar duplicados con set (si la palabra ya está en el doc, no duplicar)
        tokens_unicos = set(tokens)
        
        for token in tokens_unicos:
            if token not in indice:
                indice[token] = []
            indice[token].append(doc_id)
    
    # ordenar las listas de documentos para consistencia
    for token in indice:
        indice[token].sort()
    
    return indice


def busqueda_booleana_and(indice, termino1, termino2):
    """
    Implementa búsqueda booleana AND.
    Devuelve la intersección de documentos que contienen ambos términos.
    
    Si alguno de los términos no está en el índice, devuelve lista vacía.
    """
    # obtener listas de postings (documentos para cada término)
    postings1 = set(indice.get(termino1.lower(), []))
    postings2 = set(indice.get(termino2.lower(), []))
    
    # intersección = AND booleano
    resultado = postings1 & postings2
    
    return sorted(list(resultado))


def ejecutar_mision1():
    """Ejecuta la misión 1 completa con los datos especificados."""
    
    # corpus de la misión
    corpus_mision1 = {
        "d1": "La red de agentes interceptó tráfico sospechoso en el nodo norte.",
        "d2": "El agente de campo reportó actividad normal en la red interna.",
        "d3": "Manual de procedimientos: la red no debe apagarse sin autorización.",
        "d4": "Mantenimiento programado del agente automático de respaldo.",
    }
    
    print("=" * 70)
    print("MISIÓN 1: LA TELARAÑA DE TOKENS - ÍNDICE INVERTIDO BÁSICO")
    print("=" * 70)
    print()
    
    # paso 1: mostrar corpus
    print("📋 CORPUS ORIGINAL:")
    for doc_id, texto in corpus_mision1.items():
        print(f"  {doc_id}: {texto}")
    print()
    
    # paso 2: construir índice invertido
    print("🔨 CONSTRUYENDO ÍNDICE INVERTIDO...")
    indice = construir_indice_invertido(corpus_mision1)
    print()
    
    # mostrar una muestra del índice (los primeros términos más interesantes)
    print("📑 MUESTRA DEL ÍNDICE INVERTIDO (términos clave):")
    terminos_clave = ["agente", "red", "manual", "tráfico"]
    for term in terminos_clave:
        if term in indice:
            print(f"  '{term}' → {indice[term]}")
    print()
    
    # paso 3: resolver consulta booleana AND
    print("🔍 RESOLVIENDO CONSULTA BOOLEANA:")
    consulta_t1 = "agente"
    consulta_t2 = "red"
    print(f"  Consulta: \"{consulta_t1}\" AND \"{consulta_t2}\"")
    print()
    
    # buscar documentos
    resultado = busqueda_booleana_and(indice, consulta_t1, consulta_t2)
    
    print(f"  Documentos con '{consulta_t1}': {indice.get(consulta_t1.lower(), [])}")
    print(f"  Documentos con '{consulta_t2}': {indice.get(consulta_t2.lower(), [])}")
    print()
    
    # paso 4: mostrar resultado
    print("✅ RESULTADO FINAL (doc_id que contienen ambos términos, ordenados):")
    if resultado:
        print(f"  {resultado}")
        print()
        print("  Documentos coincidentes:")
        for doc_id in resultado:
            print(f"    {doc_id}: {corpus_mision1[doc_id]}")
    else:
        print("  No hay documentos que contengan ambos términos.")
    print()
    
    # paso 5: guardar índice en JSON (útil para análisis posterior)
    print("💾 GUARDANDO ÍNDICE EN JSON...")
    with open("indice_invertido_mision1.json", "w", encoding="utf-8") as f:
        json.dump(indice, f, indent=2, ensure_ascii=False)
    print("  Archivo: indice_invertido_mision1.json")
    print()
    
    print("=" * 70)
    print("FIN DE MISIÓN 1")
    print("=" * 70)
    
    return indice, resultado


if __name__ == "__main__":
    indice, resultado = ejecutar_mision1()
