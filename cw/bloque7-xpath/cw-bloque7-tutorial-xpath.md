# Tutorial XPath con Python
**Bloque 7:** XPath con Python 

## Qué es XPath

XPath es un lenguaje para navegar y extraer datos de documentos XML/HTML. como "CSS selectors pero más poderoso". Con XPath puedes:

- Navegar por la estructura del árbol HTML
- Filtrar elementos por atributos, posición, texto contenido
- Extraer texto o atributos específicos
- Navegar hacia arriba/abajo/lateral en el árbol

La sintaxis básica:

| Expresión | Significa |
|-----------|-----------|
| `/` | Hijo directo (como `>` en CSS) |
| `//` | Cualquier descendiente (como un espacio en CSS) |
| `@` | Atributo |
| `[ ]` | Predicado (condición) |
| `text()` | Texto del nodo |
| `*` | Comodín (cualquier elemento) |

---

## Selectores Básicos

```xpath
//h1              → Todos los <h1>
//h1/text()       → Texto de todos los <h1>
//p[@class='foo'] → Todos los <p> con class="foo"
//div/a           → <a> hijo directo de <div>
//div//a          → <a> a cualquier profundidad dentro de <div>
```

## Predicados (Filtros)

Los predicados son condiciones dentro de `[ ]`:

```xpath
//div[@class='libro']           → div con clase "libro"
//div[position() < 3]           → primeros 2 divs
//div[@data-precio > 300]       → divs con precio mayor a 300
//div[not(@class='autor')]      → divs que NO tienen class="autor"
```

Se pueden combinar:

```xpath
//div[@class='libro'][@data-genero='ficcion'][position() <= 3]
```

## Funciones Útiles

```xpath
contains(@class, 'btn')       → class contiene "btn"
starts-with(@href, '/blog')    → href empieza con "/blog"
text() = 'Hola'               → texto exacto
normalize-space(text())       → texto sin espacios extras
string-length(text())         → longitud del texto
```

## Ejes de Navegación

Esto es lo que hace XPath más poderoso que CSS:

```xpath
//h3/ancestor::section        → section ancestro del h3
//div/following-sibling::div  → hermanos siguientes
//div/preceding-sibling::div  → hermanos anteriores
//div/child::*                → todos los hijos
//div/parent::*               → el padre
```

---

## Cómo lo Usamos en Python

Código básico:

```python
from lxml import html
import requests

resp = requests.get("https://ejemplo.com")
arbol = html.fromstring(resp.content)

titulos = arbol.xpath("//h1/text()")
enlaces = arbol.xpath("//a/@href")
precios = arbol.xpath("//div[@class='producto']//span[@class='precio']/text()")
```

## Demo: Catálogo de Librería

El archivo `cw-bloque7-demo-libreria.html` es un HTML de prueba con libros. Usando XPath podemos extraer:

```python
# Todos los títulos
arbol.xpath("//h3[@class='titulo']/text()")
# → ['Cien Años de Soledad', 'El Aleph', ...]

# Solo libros de ficción
arbol.xpath("//div[@class='libro'][@data-genero='ficcion']//h3/text()")
# → ['Cien Años de Soledad', 'El Aleph', 'La Metamorfosis']

# Libros caros (>$300)
arbol.xpath("//div[@class='libro'][number(@data-precio) > 300]//h3/text()")
# → ['Breve Historia del Tiempo', 'Web Scraping con Python', ...]

# Encontrar la section que contiene un libro específico
arbol.xpath("//h3[contains(text(), 'Web Scraping')]/ancestor::section/@id")
# → ['catalogo']
```

## Mini Crawler

El archivo `cw-bloque7-mini-crawler-xpath.py` implementa un crawler que:

1. Visita una página
2. Extrae datos con XPath (título, meta description, párrafos)
3. Sigue enlaces (también con XPath)
4. Controla profundidad y cantidad de páginas

Modo offline (`python3 CW/cw-bloque7-mini-crawler-xpath.py`) usa el HTML local.
Modo online (`--online`) crawlea un sitio real.

---

## Diferencia con BeautifulSoup

| BeautifulSoup | XPath con lxml |
|---------------|----------------|
| `soup.find('h1')` | `arbol.xpath('//h1')` |
| `soup.find_all('div', class_='libro')` | `arbol.xpath("//div[@class='libro']")` |
| `soup.select('div > a')` | `arbol.xpath('//div/a')` |
| No tiene ejes | `following-sibling`, `ancestor`, etc. |

XPath es más expresivo para navegación compleja. BeautifulSoup es más tolerante con HTML mal formado.

---

## Archivos del Bloque

| Archivo | Descripción |
|---------|-------------|
| `cw-bloque7-ejemplos-xpath.py` | Demostración de 20+ selectores XPath |
| `cw-bloque7-mini-crawler-xpath.py` | Crawler que navega y extrae con XPath |
| `cw-bloque7-demo-libreria.html` | HTML de prueba para los ejemplos |
| `cw-bloque7-tutorial-xpath.md` | Este documento |

## Cómo Ejecutar

```bash
# Ejemplos de XPath
python3 CW/cw-bloque7-ejemplos-xpath.py

# Mini crawler (offline)
python3 CW/cw-bloque7-mini-crawler-xpath.py

# Mini crawler (online - crawlea refactoring.guru)
python3 CW/cw-bloque7-mini-crawler-xpath.py --online
```

> **Nota:** Asegúrate de activar el venv: `source .venv/bin/activate`

---

**Estado:** ✅ Completo
