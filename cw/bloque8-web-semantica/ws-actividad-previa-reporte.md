# Reporte: Actividad Previa - Web Semantica

## Misiones 0 a 4

En esta actividad previa exploramos los fundamentos de la Web Semantica
antes de meternos de lleno con RDF y SPARQL. Hicimos 4 misiones:

### Mision 0: HTML a Triples

Extraimos informacion de paginas HTML simples y la convertimos a triples
(sujeto, predicado, objeto). Básicamente aprendimos que detras de cada
pagina web hay datos estructurados que se pueden representar como grafos.
Usamos selectores basicos para sacar la info.

### Mision 1: JSON a Triples

Transformamos datos en JSON a triples RDF. Esto fue mas facil que HTML
porque JSON ya tiene una estructura clave-valor que se mapea naturalmente
a triples. Aprendimos que muchas APIs usan JSON y se puede convertir a
RDF sin tanta complicacion.

### Mision 2: El problema de "Paris"

Aqui nos topamos con un problema clasico: la ambiguedad de identificadores.
"Paris" puede ser la ciudad de Francia o el personaje mitologico. En un
grafo RDF, ambos tendrian el mismo URI si no tenemos cuidado. Esto nos
enseño la importancia de usar identificadores unicos (URIs) y no solo
nombres comunes. La desambiguacion es clave en la Web Semantica.

### Mision 3: Mini-grafo en Python

Implementamos un grafo como lista de diccionarios en Python puro. Cada
triple es un dict con s, p, o. Luego hicimos una funcion consulta_simple
que recibe un patron (con None para variables) y devuelve las
coincidencias. Esto nos dio una idea de como funciona SPARQL por detras.

### Mision 4: Consultas tipo SPARQL

Usando la funcion de la mision 3 hicimos consultas para encontrar autores
de libros y personas con sus nombres. El patron de consulta con None es
similar a como SPARQL usa las variables con ?.

## Que aprendimos

- Los triples son la unidad basica de la Web Semantica
- Extraer datos estructurados de HTML y JSON no es tan trivial
- Los identificadores unicos son fundamentales para evitar ambiguedades
- Un motor de consultas simple se puede implementar con listas y dicts
- La logica de SPARQL no es tan diferente de hacer consultas en Python

## Problemas encontrados

El principal problema fue el de "Paris" (duplicacion de identificadores).
Tambien batallamos un poco con la funcion consulta_simple porque al
principio no manejabamos bien los casos donde el patron tenia todos los
valores fijos. Se soluciono agregando un check de coincidencia antes de
armar la asignacion.
