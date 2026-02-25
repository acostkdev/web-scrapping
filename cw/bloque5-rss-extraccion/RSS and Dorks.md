## 1. RSS
Feed RSS y que aplicacion me permite leer
La **Sindicación Realmente Simple (RSS)** es un formato XML diseñado para la distribución de contenidos en la web. Permite a los investigadores centralizar el flujo de información de múltiples fuentes mediante **Agregadores de Contenido**, eliminando la dependencia de algoritmos de recomendación y optimizando los tiempos de vigilancia tecnológica.

### 1.1 Agregadores Recomendados para Gestión Documental

- **Inoreader:** Destaca por sus capacidades de filtrado avanzado mediante reglas lógicas y monitorización de palabras clave.
    
- **Feedly:** Proporciona una interfaz orientada a la curación de contenidos con capacidades de integración vía API.
    
- **The Old Reader:** Optimizado para la visualización minimalista y el intercambio de fuentes en redes de investigación.

### 1.2 Páginas que usan RSS
A continuación, se presentan ejemplos concretos de instituciones y plataformas que integran feeds RSS en su arquitectura:

#### 1.2.1 Organismos Internacionales y Gubernamentales

Estas entidades utilizan la sindicación para garantizar la transparencia y el acceso público a datos oficiales sin mediación editorial.

- **Naciones Unidas (UN News):** Provee canales específicos para comunicados de prensa y actualizaciones sobre crisis humanitarias.
    
- **NASA:** Gestiona diversos flujos de datos, incluyendo el "Breaking News" y el "IotD" (Image of the Day), fundamentales para la divulgación científica.
    
- **BOE (Boletín Oficial del Estado, España):** Ofrece un servicio de alertas mediante RSS para el seguimiento de leyes, disposiciones y anuncios oficiales publicados diariamente.
    

#### 1.2.2 Prensa y Agencias de Información Técnica

El sector periodístico utiliza el RSS para alimentar terminales de noticias profesionales y sistemas de monitoreo masivo.

- **The New York Times:** Mantiene una de las bibliotecas de feeds más completas, segmentada por secciones como _Business_, _Science_ y _Technology_.
    
- **Reuters:** Esencial para el sector financiero, proporcionando flujos de noticias de última hora que son consumidos por terminales de trading.
    
- **El País (España):** Estructura su oferta digital permitiendo la suscripción a secciones específicas como _Economía_, _Cultura_ o _Opinión_.
    

#### 1.2.3 Repositorios de Conocimiento y Bases de Datos Científicas

En el entorno académico, el RSS es la herramienta estándar para la vigilancia tecnológica y bibliográfica.

- **arXiv.org (Cornell University):** Este repositorio de pre-publicaciones de física, matemáticas y computación permite a los investigadores seguir categorías específicas (ej. $cs.AI$ para Inteligencia Artificial) en tiempo real.
    
- **PubMed:** La base de datos de referencia en ciencias de la salud permite generar feeds personalizados basados en términos de búsqueda MeSH (_Medical Subject Headings_).
    
- **ScienceDirect:** Permite la suscripción a los sumarios de revistas académicas específicas para recibir notificaciones de nuevos _papers_ publicados.
    

#### 1.2.4 Plataformas de Desarrollo y Repositorios de Código

La automatización en el flujo de trabajo de desarrollo de software depende críticamente de estas notificaciones.

- **GitHub:** Cada repositorio público ofrece un feed de _releases_ (lanzamientos), lo que permite a los desarrolladores recibir notificaciones de actualizaciones de librerías mediante la URL: `github.com/usuario/repositorio/releases.atom`.
    
- **Stack Overflow:** Permite suscribirse a etiquetas (_tags_) específicas. Por ejemplo, un desarrollador puede monitorizar exclusivamente nuevas preguntas sobre el lenguaje **Python** o **Rust**.
    

#### 1.2.5 Curación de Contenidos y Agregadores

- **Reddit:** Cada comunidad (_subreddit_) funciona como un feed independiente. Al añadir `.rss` al final de cualquier URL de Reddit, el sistema devuelve la estructura XML del contenido actual.
    
- **Hacker News (Y Combinator):** Utilizado por la comunidad de Silicon Valley para seguir las tendencias en tecnología y startups de manera minimalista.

# 2. Dorking

El uso de operadores avanzados permite segmentar bases de datos de indexación para obtener resultados de alta relevancia.

### 2.1 Google: Operadores de Precisión

1. `site:[dominio]`: Restringe la búsqueda a un dominio o TLD específico.
    
2. `filetype:[extensión]`: Localiza documentos por formato (PDF, XLSX, PPTX).
    
3. `"término exacto"`: Ejecuta una búsqueda literal para evitar sinonimias.
    
4. `-[término]`: Operador NOT para la exclusión de ruido semántico.
    
5. `related:[url]`: Identificación de sitios con similitud arquitectónica o temática.
    
6. `intitle:[término]`: Indexación basada en metadatos del título.
    
7. `inurl:[cadena]`: Búsqueda de parámetros específicos dentro de la cadena URL.
    
8. `AROUND(X)`: Operador de proximidad; localiza términos a una distancia de $X$ palabras.
    
9. `* (comodín)`: Sustitución de variables desconocidas en una cadena de búsqueda.
    
10. `cache:[url]`: Recuperación de versiones de páginas no disponibles en el servidor actual.
    
11. `source:[nombre]`: Filtrado por agencias de noticias específicas.
    
12. `[valor]..[valor]`: Búsqueda dentro de un rango numérico o cronológico definido.
    
13. `define:`: Acceso a glosarios y ontologías terminológicas.
    
14. `stocks:`: Consulta de indicadores macroeconómicos y bursátiles.
    
15. `weather:`: Datos meteorológicos geo-localizados.
    
16. `map:`: Solicitud de visualización cartográfica.
    
17. `movie:`: Acceso a metadatos de producciones cinematográficas.
    
18. `[unidad] in [unidad]`: Conversión de magnitudes y divisas.
    
19. `OR`: Operador booleano de unión para términos alternativos.
    
20. `after:YYYY-MM-DD`: Delimitación temporal para resultados de publicación reciente.
    

### 2.2 Bing: Arquitectura de Indexación Diferencial

1. `imagesize:large`: Filtrado por dimensiones de archivo superiores a 2MP.
    
2. `contains:[tipo]`: Identifica sitios que alojan hipervínculos hacia archivos específicos.
    
3. `ip:[dirección]`: Localiza dominios alojados bajo un mismo servidor.
    
4. `feed:[término]`: Descubrimiento de canales RSS relacionados.
    
5. `hasfeed:[sitio]`: Verificación de protocolos de sindicación activos.
    
6. `?rb=0`: Comando de depuración de interfaz para carga de baja latencia.
    
7. `prefer:[término]`: Ponderación positiva de un concepto en el algoritmo de ordenación.
    
8. `loc:[código]`: Segmentación por geolocalización de resultados.
    
9. `language:[código]`: Restricción idiomática estricta.
    
10. `Copilot Sidebar`: Análisis de resultados mediante Procesamiento de Lenguaje Natural (NLP).
    
11. `Visual Search`: Búsqueda basada en patrones de reconocimiento de imagen.
    
12. `ext:[extensión]`: Sintaxis alternativa para la búsqueda de archivos binarios.
    
13. `site:socialmedia.com "query"`: Rastreo profundo en redes sociales de microblogging.
    
14. `Price History`: Análisis de fluctuación de costes en el mercado digital.
    
15. `linkfromdomain:`: Auditoría de enlaces salientes de un dominio.
    
16. `Microsoft Rewards`: Programa de fidelización por actividad de búsqueda.
    
17. `url:[cadena]`: Validación de presencia de términos en la ruta del archivo.
    
18. `License Filter`: Filtrado por derechos de propiedad intelectual (Creative Commons).
    
19. `near:[loc]`: Optimización de resultados por proximidad geográfica.
    
20. `Deep Search`: Función integrada para consultas complejas que requieren múltiples pasos de inferencia.
    

### 2.3 DuckDuckGo: Privacidad y Metabúsqueda (!Bangs)

1. `!a / !w / !yt`: Redireccionamiento directo a Amazon, Wikipedia o YouTube.
    
2. `!github`: Consulta de repositorios de código fuente.
    
3. `!drae`: Acceso directo al diccionario de la Real Academia Española.
    
4. `password [n]`: Algoritmo de generación de claves criptográficas.
    
5. `qr [url]`: Codificación instantánea de URLs a formato Quick Response.
    
6. `shorten [url]`: Ofuscación y reducción de hipervínculos.
    
7. `expand [url]`: Análisis de destino de URLs acortadas (prevención de phishing).
    
8. `lowercase / uppercase`: Normalización de cadenas de texto.
    
9. `stopwatch`: Herramienta de medición de intervalos temporales.
    
10. `figlet`: Conversión de texto a formato ASCII de gran escala.
    
11. `color picker`: Utilidad para la identificación de códigos hex/RGB.
    
12. `Non-track search`: Ausencia total de perfiles de usuario y "burbujas de filtro".
    
13. `!scholar`: Acceso directo a literatura académica.
    
14. `!wolfram`: Integración con motor de conocimiento computacional.
    
15. `!twitter`: Monitorización de tendencias en tiempo real.
    
16. `!maps`: Integración con servicios cartográficos de Apple.
    
17. `!ebay`: Consulta en plataformas de comercio C2C.
    
18. `!rt`: Consulta de índices de crítica cinematográfica.
    
19. `Privacy Grade`: Evaluación del nivel de rastreo de los sitios web resultantes.
    
20. `Zero-click Info`: Respuestas directas extraídas de la base de datos DuckHack.
    

### 2.4 Ahmia.fi
Es importante precisar que **Ahmia.fi**, al ser un motor de búsqueda diseñado para la red **Tor** (enlaces `.onion`), no posee una sintaxis de operadores tan robusta o extensa como la de Google. Su arquitectura es más simplificada debido a las limitaciones de indexación en redes distribuidas.
### Protocolos de Búsqueda Avanzada en Ahmia

1. **`"frase exacta"`**: Al igual que en buscadores tradicionales, las comillas obligan a Ahmia a buscar la coincidencia literal de términos.
    
2. **`término1 término2`**: El espacio actúa como un operador booleano **AND** implícito para encontrar páginas que contengan ambos conceptos.
    
3. **`término1 OR término2`**: Permite expandir la búsqueda para localizar resultados que contengan cualquiera de las dos palabras clave.
    
4. **`-término`**: Operador de exclusión. Útil para eliminar ruido, como por ejemplo `bitcoin -mixer` para buscar información sobre la criptomoneda sin servicios de mezcla.
    
5. **`site:.onion`**: Aunque Ahmia busca por defecto en la red Tor, este comando asegura que los resultados se restrinjan estrictamente a dominios de la red profunda.
    
6. **`site:.tor`**: Variante para localizar servicios ocultos que utilicen sufijos alternativos en redes experimentales.
    
7. **`intitle:"index of"`**: Un dork clásico para localizar directorios abiertos dentro de servidores `.onion`.
    
8. **`intext:"password"`**: Localiza cadenas de texto específicas dentro del cuerpo de la página (útil para investigación de fugas de datos).
    
9. **`intext:"database"`**: Identifica sitios que mencionan explícitamente bases de datos almacenadas.
    
10. **`intext:"dump"`**: Comando clave para analistas de inteligencia que buscan filtraciones de información (leaks).
    
11. **`"-----BEGIN RSA PRIVATE KEY-----"`**: Búsqueda literal de fragmentos de claves criptográficas expuestas accidentalmente.
    
12. **`"-----BEGIN PGP PUBLIC KEY BLOCK-----"`**: Localización de identidades PGP para verificar la autenticidad de servicios o usuarios.
    
13. **`intext:".gov"`**: Identifica sitios en la red profunda que mencionan o contienen documentos gubernamentales filtrados.
    
14. **`intext:".edu"`**: Localización de credenciales o documentos académicos en repositorios no oficiales.
    
15. **`"onion.link"`**: Localización de espejos (mirrors) o puertas de enlace (proxies) que permiten ver contenido Tor desde la web clara.
    
16. **`intext:"exploit"`**: Búsqueda de foros o repositorios de vulnerabilidades de día cero (0-day).
    
17. **`intext:"@gmail.com"`**: Localización de correos electrónicos específicos asociados a cuentas de usuario en foros ocultos.
    
18. **`"magnet:?xt=urn:btih:"`**: Rastreo de enlaces Magnet de archivos Torrent distribuidos exclusivamente en la red Tor.
    
19. **`intext:"API_KEY"`**: Identificación de claves de interfaz de programación expuestas en scripts o archivos de configuración.
    
20. **`intext:"login" "register"`**: Localización de portales de acceso a comunidades privadas o mercados negros.