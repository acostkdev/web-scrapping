Es un lenguaje para localizar nodos y extraer valores en documentos XML y HTML.

- Navegar por la estructura de un arbol de html xml
- rutas relativas y rutas absolutas

/ hijos directos
// hijos hasta cualquier nivel 

Scrapping vertical es sobre la misma pagina
Scrapping horizontal es sobre las diferentes páginas

## Ejemplos

https://refactoring.guru/

Página 1
![[Pasted image 20260213085925.png]]

Página 2
![[Pasted image 20260213151549.png]]

| Funcion                                                    | Xpath                                                                                   |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1. Extraer el Título Principal                             | //h1/text()                                                                             |
| 2. Capturar el resumen o "Pitch" del sitio                 | //p[@class='big']/b/text()                                                              |
| 3. Listar secciones principales (Refactoring y Patterns)   | //div[contains(@class, 'container-headline')]//h2/text()                                |
| 4. Obtener enlaces a las secciones principales             | //div[contains(@class, 'container-headline')]//a[contains(@class, 'btn-primary')]/@href |
| 5. Extraer URLs de imágenes de vista previa                | //img[@class='index-img']/@src                                                          |
| (Empieza pag 2)                                            | -------------------------------------------------------------------                     |
| 6.Obtener la descripción corta de los Patrones de Diseño   | //p[contains(@class, 'dp1-p')]/b/text()                                                 |
| 7. Extraer el enlace al Catálogo de Patrones               | //a[contains(@href, '/design-patterns/catalog')]/@hre                                   |
| 8. Capturar los títulos de los beneficios de usar patrones | //h3[contains(@class, 'dp2-h')]/text()                                                  |
| 9. Obtener los enlaces a ejemplos de código por lenguaje   | //li[contains(@class, 'menu-code-examples-item')]/a/text()                              |
| 10.Extraer los Beneficios Específicos                      | //p[contains(@class, 'dp2-p')]/span/text() \| //p[contains(@class, 'dp2-p')]/text()     |
