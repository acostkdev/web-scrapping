# Web Scraping: Repositorio de Actividades Académicas

Este repositorio centraliza el desarrollo técnico y práctico de la materia de Web Scraping. El objetivo primordial es la implementación de algoritmos para la recolección, procesamiento y almacenamiento de datos provenientes de fuentes digitales no estructuradas.

## 📋 Convenciones de Nomenclatura

Para mantener la integridad estructural del repositorio, se ha definido el siguiente estándar de organización de archivos:

* **cw (Class Work):** Actividades prácticas y ejercicios de laboratorio realizados durante las sesiones lectivas.
* **hw (Homework):** Investigaciones y desarrollos técnicos asignados para el trabajo independiente.
* **project/:** Directorio exclusivo para el proyecto integrador, el cual incluye la arquitectura del scraper, la lógica de parseo y el manejo de persistencia de datos.

## 🚀 Estándar de Commits

Para garantizar un historial de versiones legible y organizado, los mensajes de commit deben seguir la misma taxonomía de las actividades. Cada commit debe referirse exclusivamente a los archivos de una actividad específica o a una fase del proyecto:

**Formato:** `Prefijo: Descripción de la actividad`

* **Ejemplo CW:** `cw (parte): RSS and Dorking`
* **Ejemplo HW:** `hw (parte): Implementacion de selectores CSS`
* **Ejemplo Proyecto:** `project (parte): Configuracion inicial de Selenium`

(La etiqueta *parte* es opcional)

## 🏗️ Estructura del Directorio

* `/cw`: Ejercicios de clase (e.g., cw: Introduccion).
* `/hw`: Tareas académicas (e.g., hw: 01-analisis-dom).
* `/project`: Código fuente y documentación del proyecto final.

## 🛠️ Tecnologías Utilizadas

* **Lenguajes:** Python / Node.js
* **Herramientas de Extracción:** BeautifulSoup, Scrapy, Selenium, Playwright.
* **Protocolos:** HTTP/HTTPS, Sindicación (RSS/Atom).
