
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def ejecutar_mision3():
    """Filtra documentos por nivel SIGILO, aplica TF-IDF y devuelve el top-1."""
    
    documentos_mision3 = [

        {"doc_id": "x1", "nivel": "PUBLICO", "texto": "Boletín de prensa sobre obras en la avenida central y tráfico lento."},
        {"doc_id": "x2", "nivel": "SIGILO", "texto": "Rumor operativo: el contacto cambió frecuencia; verificar handoff nocturno. ###FIN###"},
        {"doc_id": "x3", "nivel": "PUBLICO", "texto": "Convocatoria a curso de primeros auxilios para voluntarios municipales."},
        {"doc_id": "x4", "nivel": "SIGILO", "texto": "Inventario de papelería y tóner para el almacén B del cuartel general."},
        {"doc_id": "x5", "nivel": "RESERVADO", "texto": "Lista de proveedores homologados para catering y cafetería interna."},
    ]
    
    consulta_mision3 = "contacto frecuencia operativo handoff nocturno"

    
    print("=" * 70)
    print("MISIÓN 3: EL CIFRADO DE COLECCIÓN - FILTRO HÍBRIDO")
    print("=" * 70)
    print()
    
    print("DOCUMENTOS COMPLETOS:")
    for doc in documentos_mision3:
        nivel_tag = f"[{doc['nivel']}]"
        print(f"  {doc['doc_id']:>3} {nivel_tag:>12} → {doc['texto'][:60]}...")
    print()
    
    # paso 1: filtrar por nivel SIGILO
    print("FILTRANDO POR NIVEL \"SIGILO\"...")
    documentos_sigilo = [doc for doc in documentos_mision3 if doc["nivel"] == "SIGILO"]
    print(f"  Documentos SIGILO encontrados: {len(documentos_sigilo)}")
    for doc in documentos_sigilo:
        print(f"    {doc['doc_id']}: {doc['texto'][:70]}...")
    print()
    
    # paso 2: preparar textos para TF-IDF
    doc_ids_sigilo = [doc["doc_id"] for doc in documentos_sigilo]
    textos_sigilo = [doc["texto"] for doc in documentos_sigilo]
    
    print("CONSULTA: \"%s\"" % consulta_mision3)
    print()
    
    # paso 3: vectorizar SOLO los documentos filtrados + consulta
    print("APLICANDO TF-IDF + SIMILITUD COSENO...")
    vectorizador = TfidfVectorizer(lowercase=True)
    textos_con_consulta = textos_sigilo + [consulta_mision3]
    matriz_tfidf = vectorizador.fit_transform(textos_con_consulta)
    
    vector_consulta = matriz_tfidf[-1]
    matriz_docs = matriz_tfidf[:-1]
    
    similitudes = cosine_similarity(vector_consulta, matriz_docs)[0]
    
    # paso 4: rankear
    ranking = []
    for idx, doc_id in enumerate(doc_ids_sigilo):
        ranking.append((doc_id, similitudes[idx], textos_sigilo[idx]))
    
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    print()
    print("RANKING (SIGILO documents only):")
    for doc_id, score, texto in ranking:
        print(f"  {doc_id}: {score:.4f}")
    print()
    
    # paso 5: devolver top-1 con preview de 120 caracteres
    top_doc = ranking[0]
    doc_id_ganador, score_ganador, texto_ganador = top_doc
    
    print("=" * 70)
    print(f"DOCUMENTO GANADOR: {doc_id_ganador} (score: {score_ganador:.4f})")
    print("=" * 70)
    print()
    print(f"  Puntuación de similitud: {score_ganador:.4f}")
    print()
    print(f"  Texto completo:")
    print(f"    \"{texto_ganador}\"")
    print()
    print(f"  Preview (primeros 120 caracteres):")
    preview = texto_ganador[:120]
    print(f"    \"{preview}\"")
    print()
    
    # verificar si contiene el delimitador
    if "###FIN###" in texto_ganador:
        print("  ✅ DELIMITADOR ###FIN### ENCONTRADO")
    else:
        print("  ❌ Delimitador ###FIN### NO encontrado")
    print()
    
    print("=" * 70)
    print("FIN DE MISIÓN 3")
    print("=" * 70)
    
    return top_doc


if __name__ == "__main__":
    top_doc = ejecutar_mision3()
