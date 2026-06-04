"""
ac1_scraper_paginado.py
AC-1: Rastreo de un sitio real con paginación

Usa Hacker News como sitio de prueba:
- HTML estático, sin JS
- Paginación clara via ?p=N
- 30 artículos por página
- robots.txt: Crawl-delay 30s, sin restricciones en /
"""

import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "SIMANW-AC1/1.0 (academico; proyecto recuperacion informacion)"
}


class RastreadorPaginado:
    def __init__(self, url_base, selector_articulos, selector_siguiente,
                 delay=3, max_paginas=5):
        self.url_base = url_base
        self.selector_articulos = selector_articulos
        self.selector_siguiente = selector_siguiente
        self.delay = delay
        self.max_paginas = max_paginas
        self.resultados = []

    def extraer_pagina(self, html, url_actual):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.select(self.selector_articulos)
        articulos = []
        for item in items:
            a = item.find('a')
            if not a:
                continue
            titulo = a.get_text(strip=True)
            enlace = a.get('href', '')
            if enlace.startswith('item?'):
                enlace = urljoin(url_actual, enlace)
            articulos.append({
                'titulo': titulo,
                'url': enlace,
                'fuente': 'Hacker News',
            })
        return articulos

    def obtener_siguiente_pagina(self, html, url_actual):
        soup = BeautifulSoup(html, 'html.parser')
        more = soup.find('a', string='More')
        if more and more.get('href'):
            return urljoin(url_actual, more['href'])
        return None

    def rastrear(self):
        url_actual = self.url_base
        paginas_visitadas = 0

        while url_actual and paginas_visitadas < self.max_paginas:
            print(f"  Pagina {paginas_visitadas + 1}: {url_actual}")
            try:
                resp = requests.get(url_actual, headers=HEADERS, timeout=15)
                resp.raise_for_status()
            except requests.RequestException as e:
                print(f"    ERROR: {e}")
                break

            articulos = self.extraer_pagina(resp.text, url_actual)
            self.resultados.extend(articulos)
            print(f"    {len(articulos)} articulos (total: {len(self.resultados)})")

            url_siguiente = self.obtener_siguiente_pagina(resp.text, url_actual)
            paginas_visitadas += 1

            if paginas_visitadas < self.max_paginas and url_siguiente:
                url_actual = url_siguiente
                print(f"    Esperando {self.delay}s...")
                time.sleep(self.delay)
            else:
                break

        return self.resultados

    def guardar_json(self, archivo):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(self.resultados, f, ensure_ascii=False, indent=2)
        return len(self.resultados)


def run(output_path="data/ac1_noticias.json"):
    print("=" * 60)
    print("AC-1: RASTREO CON PAGINACION (Hacker News)")
    print("=" * 60)
    print()
    print("  Sitio: news.ycombinator.com")
    print("  robots.txt: Crawl-delay 30s, Disallow solo login/vote/etc")
    print()

    rastreador = RastreadorPaginado(
        url_base="https://news.ycombinator.com/",
        selector_articulos="span.titleline",
        selector_siguiente="a[href*='?p=']",  # fallback, usamos el string 'More'
        delay=3,
        max_paginas=3,
    )

    resultados = rastreador.rastrear()
    print(f"\n  Total noticias: {len(resultados)}")
    print(f"\n  Primeras 5:")
    for r in resultados[:5]:
        print(f"    - {r['titulo'][:65]}")
    print()

    total = rastreador.guardar_json(output_path)
    print(f"  Guardado: {output_path} ({total} noticias)")
    print()

    return resultados


if __name__ == "__main__":
    run()
