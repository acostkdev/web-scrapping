"""
XPath con Python - Ejemplos Prácticos
Bloque 7: XPath con Python

Demostración de selectores XPath básicos y avanzados usando lxml.html.
NOTA: lxml debe estar instalado (python3-lxml en sistema).
"""

from lxml import html
import requests


def cargar_desde_archivo(ruta):
    """Carga un HTML desde archivo y devuelve el árbol lxml."""
    with open(ruta, "r", encoding="utf-8") as f:
        arbol = html.fromstring(f.read())
    return arbol


def imprimir_resultados(descripcion, xpath, elementos):
    """Helper para imprimir resultados de forma consistente."""
    print(f"\n  - {descripcion}")
    print(f"    XPath: {xpath}")
    print(f"    Resultados ({len(elementos)}):")
    for i, elem in enumerate(elementos[:5]):  # máx 5
        texto = elem.strip() if isinstance(elem, str) else elem.text_content().strip()
        print(f"      {i+1}. {texto[:80]}")
    if len(elementos) > 5:
        print(f"      ... y {len(elementos) - 5} más")


def demostracion_xpath(arbol):
    """Demuestra diferentes tipos de selectores XPath."""
    
    print("=" * 70)
    print("XPath CON PYTHON - EJEMPLOS PRÁCTICOS")
    print("=" * 70)
    print()
    
    # 1. XPath BÁSICOS - Navegación simple
    print("1. XPATH BÁSICOS (navegación simple)")
    print("-" * 50)
    
    titulo = arbol.xpath("//h1/text()")
    imprimir_resultados("Título principal del sitio", "//h1/text()", titulo)
    
    todos_titulos = arbol.xpath("//h3[@class='titulo']/text()")
    imprimir_resultados("Todos los títulos de libros", "//h3[@class='titulo']/text()", todos_titulos)
    
    autores = arbol.xpath("//p[@class='autor']/text()")
    imprimir_resultados("Todos los autores", "//p[@class='autor']/text()", autores)
    
    # 2. XPath con PREDICADOS - Filtrado condicional
    print("\n2. XPATH CON PREDICADOS (filtrado)")
    print("-" * 50)
    
    libros_ficcion = arbol.xpath("//div[@class='libro'][@data-genero='ficcion']//h3/text()")
    imprimir_resultados("Libros de ficción", "//div[@class='libro'][@data-genero='ficcion']//h3/text()", libros_ficcion)
    
    libros_caros = arbol.xpath("//div[@class='libro'][number(@data-precio) > 300]//h3/text()")
    imprimir_resultados("Libros caros (>$300)", "//div[@class='libro'][number(@data-precio) > 300]//h3/text()", libros_caros)
    
    primer_libro = arbol.xpath("(//div[@class='libro'])[1]//h3/text()")
    imprimir_resultados("Primer libro del catálogo", "(//div[@class='libro'])[1]//h3/text()", primer_libro)
    
    # 3. XPath con FUNCIONES - contains, starts-with, position
    print("\n3. XPATH CON FUNCIONES (contains, position, etc.)")
    print("-" * 50)
    
    textos_con_scraping = arbol.xpath("//p[contains(text(), 'Scraping')]/text()")
    imprimir_resultados("Textos que contienen 'Scraping'", "//p[contains(text(), 'Scraping')]/text()", textos_con_scraping)
    
    tercer_en_adelante = arbol.xpath("(//div[@class='libro'])[position() >= 3]//h3/text()")
    imprimir_resultados("Libros del 3 en adelante", "(//div[@class='libro'])[position() >= 3]//h3/text()", tercer_en_adelante)
    
    parrafos_no_autor = arbol.xpath("//p[not(@class='autor')]/text()")
    imprimir_resultados("Párrafos que NO son de autor", "//p[not(@class='autor')]/text()", parrafos_no_autor)
    
    # 4. XPath con EJES - navegación relativa
    print("\n4. XPATH CON EJES (navegación relativa)")
    print("-" * 50)
    
    # hermanos siguientes después del primer libro
    hermanos = arbol.xpath("(//div[@class='libro'])[1]/following-sibling::div//h3/text()")
    imprimir_resultados("Siguientes libros después del primero (following-sibling)", 
                       "(//div[@class='libro'])[1]/following-sibling::div//h3/text()", hermanos)
    
    ancestros = arbol.xpath("//h3[contains(text(), 'Web Scraping')]/ancestor::section/@id")
    imprimir_resultados("Section ancestro del libro 'Web Scraping'", 
                       "//h3[contains(text(), 'Web Scraping')]/ancestor::section/@id", ancestros)
    
    # 5. Extracción de ATRIBUTOS
    print("\n5. EXTRACCIÓN DE ATRIBUTOS")
    print("-" * 50)
    
    generos = arbol.xpath("//div[@class='libro']/@data-genero")
    imprimir_resultados("Géneros de libros (atributo)", "//div[@class='libro']/@data-genero", generos)
    
    enlaces = arbol.xpath("//nav/a/@href")
    imprimir_resultados("Enlaces de navegación", "//nav/a/@href", enlaces)
    
    print("\n" + "=" * 70)
    print("FIN DE DEMOSTRACIÓN XPATH")
    print("=" * 70)


def scrapear_url(url, xpath_query):
    """Scrapea una URL usando requests + lxml y extrae con XPath."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "utf-8"
        arbol = html.fromstring(resp.content)
        resultados = arbol.xpath(xpath_query)
        return resultados
    except Exception as e:
        return [f"Error: {e}"]


if __name__ == "__main__":
    # cargar archivo de demo
    arbol = cargar_desde_archivo("CW/cw-bloque7-demo-libreria.html")
    demostracion_xpath(arbol)
    
    # demo extra: scrapear un sitio real
    print("\nSCRAPEO RÁPIDO DESDE REFACTORING.GURU:")
    print("-" * 50)
    resultados = scrapear_url(
        "https://refactoring.guru/",
        "//h1/text()"
    )
    print(f"  H1 desde refactoring.guru: {resultados}")
    print()
