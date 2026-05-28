# Reporte: Actividades Extra - Web Semantica

## Resumen

Estas actividades extra nos llevaron mas alla de los conceptos basicos
de la Web Semantica. Exploramos desde la serializacion Turtle hasta
consultas SPARQL complejas y hasta comparamos SHACL con razonadores.

## Mision A: RDF basico

Aprendimos la estructura basica de RDF: sujeto, predicado, objeto.
Cada triple es un hecho, y el conjunto de triples forma un grafo.
Usamos rdflib para crear grafos programaticamente en Python.

## Mision B: OWL (Web Ontology Language)

Vimos como OWL permite definir ontologias con restricciones mas
expresivas que RDFS. Cosas como equivalencia de clases, restricciones
de cardinalidad y propiedades transitivas. Esto es util para dominios
donde se necesita mas poder expresivo.

## Mision C: Turtle

Aprendimos el formato Turtle (Terse RDF Triple Language) para escribir
triples de forma mas compacta que RDF/XML. Modelamos un catalogo
universitario con profesores, estudiantes, asignaturas y relaciones
como "enseña". Tambien vimos inferencia basica con rdfs:subClassOf:
si Alicia es Profesor y Profesor es subClassOf Persona, entonces
Alicia tambien es Persona automaticamente.

## Mision D: Consultas SPARQL

Ejecutamos consultas SPARQL sobre nuestro grafo universitario:
- SELECT para obtener nombres de personas (usando rutas de propiedad
  para inferencia transitiva)
- ASK para preguntas booleanas (Bob es subClassOf Persona?)
- FILTER para filtrar por idioma (@es vs @en)

Aprendimos que SPARQL es muy parecido a SQL pero para grafos, y que
las consultas se pueden preparar y reutilizar con prepareQuery.

## Mision E: SPARQL en Wikidata

Conectamos con el endpoint SPARQL de Wikidata usando requests.
Ejecutamos consultas para obtener datos reales como ciudades de Mexico
o canciones de artistas famosos. La sintaxis es la misma pero los
prefijos y URIs son los de Wikidata.

## Mision F: SHACL

SHACL (Shapes Constraint Language) se usa para validar grafos RDF.
Definimos shapes (formas) que describen como deben ser los datos:
que propiedades debe tener una Persona, que tipos de valores, etc.
Esto es util para garantizar calidad de datos.

## Mision G: SHACL vs Reasoner

Comparamos SHACL con razonadores (como los que vienen con rdflib).
- SHACL solo valida, no infiere nuevos triples
- Los razonadores (RDFS, OWL) generan nueva informacion a partir
  de reglas logicas
- SHACL es para control de calidad, razonadores para descubrimiento

## Mision H: Integracion

Como proyecto final integramos todo: creamos un grafo con datos
reales (sacados de una pagina web), lo serializamos a Turtle,
le hicimos consultas SPARQL, validamos con SHACL y aplicamos
inferencia RDFS. Fue un buen ejercicio para ver el flujo completo
de trabajo con Web Semantica.

## Conclusiones

La Web Semantica no es solo un concepto teorico, se puede programar
con librerias como rdflib en Python. Aprendimos que:

- Los grafos RDF son flexibles y faciles de extender
- Turtle es mucho mas legible que RDF/XML
- SPARQL es poderosisimo para consultar grafos
- La inferencia automatica ahorra mucho trabajo manual
- SHACL complementa a los razonadores para asegurar calidad

Algunos errores que tuvimos: confundir prefijos en Turtle (olvidar
declararlos), malentender la sintaxis de rutas de propiedad en SPARQL
(property paths), y que rdflib a veces no instala bien en entornos
virtuales. Pero al final logramos que todo funcionara.
