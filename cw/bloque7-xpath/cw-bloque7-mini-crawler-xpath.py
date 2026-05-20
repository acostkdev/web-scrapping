"""
Mini Crawler XPath - Navegación entre páginas usando XPath
Bloque 7: XPath con Python

Extrae enlaces de una página, luego los visita y extrae datos.
Todo usando lxml + XPath para navegación y extracción.
"""

from lxml import html
import requests
import time
import json


class MiniCrawlerXPath:
    """
    Crawler simple que navega páginas usando XPath para:
    - Extraer enlaces
    - Extraer datos específicos
    - Controlar profundidad de navegación
    """
    
    def __init__(self, delay=1):
        self.delay = delay
        self.visitados = set()
        self.datos = []
        self.headers = {"User-Agent": "MiniCrawlerXPath/1.0"}
    
    def descargar(self, url):
        """Descarga una URL y devuelve el árbol lxml."""
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.encoding = "utf-8"
            return html.fromstring(resp.content)
        except Exception as e:
            print(f"  Error descargando {url}: {e}")
            return None
    
    def extraer_enlaces(self, arbol, url_base):
        """Extrae enlaces absolutos usando XPath."""
        enlaces = arbol.xpath("//a/@href")
        enlaces_abs = []
        for enlace in enlaces:
            if enlace.startswith("http"):
                enlaces_abs.append(enlace)
            elif enlace.startswith("/"):
                from urllib.parse import urlparse
                parsed = urlparse(url_base)
                enlaces_abs.append(f"{parsed.scheme}://{parsed.netloc}{enlace}")
        return enlaces_abs
    
    def extraer_datos_pagina(self, arbol, url):
        """Extrae datos estructurados de una página usando XPath."""
        titulo = arbol.xpath("//h1/text()")
        descripcion = arbol.xpath("//meta[@name='description']/@content")
        parrafos = arbol.xpath("//p/text()")
        
        return {
            "url": url,
            "titulo": titulo[0].strip() if titulo else "",
            "descripcion": descripcion[0].strip() if descripcion else "",
            "num_parrafos": len(parrafos),
            "primer_parrafo": parrafos[0].strip() if parrafos else "",
        }
    
    def rastrear(self, url_inicio, max_paginas=5, profundidad_max=1):
        """
        Rastrea desde url_inicio.
        - max_paginas: cuántas páginas visitar como máximo
        - profundidad_max: cuántos niveles de enlaces seguir
        """
        cola = [(url_inicio, 0)]
        
        print(f"\n🚀 INICIANDO CRAWLER DESDE: {url_inicio}")
        print(f"   Máx páginas: {max_paginas} | Profundidad: {profundidad_max}")
        print()
        
        while cola and len(self.visitados) < max_paginas:
            url, profundidad = cola.pop(0)
            
            if url in self.visitados:
                continue
            if profundidad > profundidad_max:
                continue
            
            print(f"  ▶ [{profundidad}] Visitando: {url[:70]}...")
            
            arbol = self.descargar(url)
            if arbol is None:
                continue
            
            self.visitados.add(url)
            
            # extraer datos de esta página
            datos = self.extraer_datos_pagina(arbol, url)
            self.datos.append(datos)
            
            # mostrar resumen
            print(f"    Título: {datos['titulo'][:60]}")
            print(f"    Párrafos: {datos['num_parrafos']}")
            
            # si no hemos llegado al límite, seguimos enlaces
            if len(self.visitados) < max_paginas and profundidad < profundidad_max:
                enlaces = self.extraer_enlaces(arbol, url)
                nuevas = 0
                for enlace in enlaces:
                    if enlace not in self.visitados and nuevas < 3:
                        cola.append((enlace, profundidad + 1))
                        nuevas += 1
                print(f"    Enlaces nuevos encolados: {nuevas}")
            
            print()
            time.sleep(self.delay)
        
        print(f"✅ CRAWLER FINALIZADO: {len(self.visitados)} páginas visitadas")
        return self.datos


def demo_mini_crawler():
    """Ejecuta el crawler sobre un sitio de prueba."""
    
    crawler = MiniCrawlerXPath(delay=0.5)
    
    datos = crawler.rastrear(
        url_inicio="https://refactoring.guru/",
        max_paginas=3,
        profundidad_max=1
    )
    
    # guardar resultados
    with open("resultados_crawler_xpath.json", "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Datos guardados en: resultados_crawler_xpath.json")
    print()
    
    # mostrar tabla resumen
    print("📊 RESUMEN DE DATOS EXTRAÍDOS:")
    print("-" * 70)
    for d in datos:
        print(f"  {d['url'][:50]:<52} | {d['titulo'][:30]:<30}")
    print()


def demo_offline():
    """Demo offline usando el archivo HTML local."""
    
    print("=" * 70)
    print("MINI CRAWLER XPATH - DEMO OFFLINE")
    print("=" * 70)
    
    with open("CW/cw-bloque7-demo-libreria.html", "r", encoding="utf-8") as f:
        arbol = html.fromstring(f.read())
    
    print("\n📖 Catálogo de Librería (offline)")
    print("-" * 50)
    
    titulos = arbol.xpath("//div[@class='libro']//h3/text()")
    precios = arbol.xpath("//div[@class='libro']//p[@class='precio']/text()")
    generos = arbol.xpath("//div[@class='libro']/@data-genero")
    autores = arbol.xpath("//div[@class='libro']//p[@class='autor']/text()")
    
    print(f"\n  {'Título':<35} {'Autor':<25} {'Precio':<10} {'Género'}")
    print(f"  {'-'*35} {'-'*25} {'-'*10} {'-'*10}")
    
    for t, a, p, g in zip(titulos, autores, precios, generos):
        print(f"  {t:<35} {a:<25} {p:<10} {g}")
    
    print("\n  Ofertas:")
    ofertas = arbol.xpath("//li[@class='oferta']/text()")
    of = arbol.xpath("//section[@id='ofertas']//li/text()")
    for o in of:
        print(f"    • {o}")
    
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--online":
        demo_mini_crawler()
    else:
        demo_offline()
        print("💡 Para crawlear un sitio real: python3 CW/cw-bloque7-mini-crawler-xpath.py --online")
