# Informe del proyecto: puntos de articulación en grafos

**Curso:** Algoritmos y Estructuras de Datos (AED)  
**Integrantes:** Antony Yonel Rosales Esteban, Itta Zhair Saavedra Clavijo y Jeseph Imanol Burgos Ochoa  
**Fecha:** 19 de noviembre de 2026

## Resumen

El proyecto implementa el algoritmo DFS de Tarjan para encontrar puntos de articulación en grafos simples no dirigidos. Un punto de articulación es un vértice cuya eliminación aumenta el número de componentes conexas. La implementación calcula tiempos de descubrimiento (`tin`) y valores `low`, registra los eventos del recorrido y valida la traza antes de usarla en las escenas educativas de Manim.

El ejemplo principal es una red con vértices `A`–`G`. La ejecución identifica `A`, `B`, `D` y `E` como puntos de articulación. La película narra la motivación, explica las ideas de DFS, `tin` y `low`, muestra la ejecución, cubre el tratamiento especial de la raíz y analiza la complejidad.

## Alcance y documento de referencia

El archivo `enunciado.txt` de la raíz estaba vacío al preparar este informe. Para contrastar el trabajo con las instrucciones se usó `aed_project_2.pdf`, también ubicado en la raíz. El informe se entrega en Markdown como se solicitó; si la entrega formal exige un PDF, este archivo deberá exportarse a PDF junto con el enlace al video.

El proyecto se concentra en la detección de puntos de articulación. La carpeta `output/` contiene varias ediciones previas; la salida narrada optimizada disponible en este checkout es `output/final_v3_optimizada/Articulaciones_v3_optimizada.mp4`.

El alcance implementado detecta vértices de articulación; no calcula explícitamente la partición completa del grafo en componentes biconexas. Si el tema que el grupo recibió fue la descomposición en componentes biconexas, esa parte tendría que añadirse; si fue puntos de articulación, el alcance coincide con el proyecto.

## Objetivos

- Explicar por qué ciertos vértices son críticos para la conectividad de una red.
- Implementar una solución lineal basada en búsqueda en profundidad, sin delegar el algoritmo a una biblioteca externa.
- Mostrar una ejecución real de la implementación en una animación y conectar los valores calculados con las decisiones del algoritmo.
- Analizar la complejidad temporal y espacial.

## Conceptos y algoritmo

Tarjan recorre todos los componentes del grafo mediante DFS. A cada vértice `u` le asigna:

- `tin[u]`: el instante en que DFS descubre `u`.
- `low[u]`: el menor tiempo de descubrimiento que puede alcanzar el subárbol DFS de `u` al seguir aristas del árbol y, como máximo, una arista de retorno hacia un ancestro.

Cuando termina de explorar un hijo `v` de un vértice no raíz `u`, si `low[v] >= tin[u]`, el subárbol de `v` no tiene una salida hacia un ancestro anterior a `u`. Al eliminar `u`, ese subárbol queda separado, así que `u` es una articulación. La igualdad importa: volver a `u` no evita que la eliminación de `u` desconecte el subárbol.

La raíz DFS es el caso especial: es articulación si tiene más de un hijo directo en el árbol DFS. Se cuentan hijos DFS, no vecinos del grafo; un vecino puede haber sido descubierto a través de otra ruta.

### Ejemplo principal

El grafo de demostración tiene las aristas `A-B`, `A-G`, `B-C`, `C-D`, `D-B`, `D-E` y `E-F`. El orden lexicográfico de vecinos hace determinista el recorrido. La zona `B-C-D` forma un ciclo con una arista de retorno `D-B`; `E-F` forma una rama sin ruta alternativa. Para este grafo, Tarjan devuelve las articulaciones `A`, `B`, `D` y `E`.

La película también muestra dos casos para la raíz: en un triángulo, `A` tiene dos vecinos pero un hijo DFS y no es articulación; en el grafo `R-S` y `R-T`, `R` tiene dos hijos DFS y sí es articulación.

## Implementación

La solución está dividida en módulos bajo `src/articulations/`:

- `graph.py` define un grafo simple, no dirigido e inmutable, con etiquetas de texto. Ordena vértices y vecinos para obtener trazas reproducibles y rechaza lazos y aristas paralelas.
- `tarjan.py` implementa DFS, calcula `tin`, `low`, padres e hijos DFS, procesa grafos desconectados y devuelve el conjunto ordenado de articulaciones.
- `events.py` y `trace.py` registran los hechos de la ejecución y representan el resultado.
- `validate_trace.py` comprueba secuencias, padres, aristas, valores y decisiones de articulación de la traza.

El punto de entrada del ejemplo es `scripts/run_example.py`. Ejecuta `Graph.from_edges`, llama a `run_tarjan` e imprime las articulaciones y los valores `tin` y `low`.

La implementación algorítmica es recursiva. Su profundidad de pila puede alcanzar `O(V)` en un grafo muy profundo; para grafos que excedan el límite de recursión de Python sería necesario aumentar ese límite o usar una DFS iterativa.

## Animación y narración

La película se construye con Manim y organiza el contenido en siete secuencias:

1. Motivación mediante una red de transporte y la falla de una estación.
2. Definición de articulación, comparando un ciclo y un camino.
3. Intuición de DFS, `tin`, `low` y las aristas de retorno.
4. Recorrido real del grafo principal y detección de articulaciones.
5. Regla especial de la raíz DFS.
6. Análisis de complejidad.
7. Resumen del resultado y créditos.

La escena principal llama a `run_tarjan` y `validate_trace`. Las animaciones de descubrimientos, aristas de árbol, retornos, actualizaciones de `low` y detecciones de articulación se derivan de los eventos reales, no de una secuencia de valores escrita a mano. `src/animation/graph_view.py` comparte los componentes visuales de grafos.

El título del proyecto y los nombres de los integrantes aparecen en los créditos finales. La narración se define mediante señales en `narration/cues.json`; los scripts de `scripts/` generan voces, renderizan y mezclan audio.

## Revisión frente a los requisitos del video

| Requisito | Evidencia en el proyecto | Estado |
|---|---|---|
| Motivación inicial | Red de transporte y demostración de desconexión al retirar una estación. | Cubierto |
| Introducción conceptual | Definición de articulación, DFS, `tin`, `low`, aristas de retorno y condición de detección. | Cubierto |
| Demostración animada | La traza real del grafo `A`–`G` guía la escena principal. | Cubierto |
| Implementación propia y real | `run_tarjan` implementa el recorrido; `validate_trace` valida los eventos usados por la animación. | Cubierto |
| Caso borde relevante | La raíz se trata por separado; se comparan uno y varios hijos DFS. | Cubierto |
| Análisis de complejidad | El video presenta tiempo `O(V + E)` y espacio auxiliar `O(V)`. | Cubierto |
| Título e integrantes | Se muestran en los créditos finales. | Cubierto |
| Formato y duración | La edición optimizada está en MP4, Full HD 1080p30, y dura 254.8 segundos (4:14.8), según la documentación del proyecto. | Cumple el máximo de 5 minutos; queda algo por debajo del objetivo cercano a 5 minutos indicado posteriormente por el docente. |

El código incluye además ejemplos para la raíz con un hijo DFS y con dos. Esta es una condición de borde algorítmica porque la regla general `low[hijo] >= tin[u]` se aplica a vértices no raíz; la raíz debe evaluarse por cantidad de hijos DFS. La película no necesita presentar un grafo vacío para satisfacer este caso especial.

## Complejidad

El algoritmo examina cada vértice una vez y cada arista un número constante de veces mediante listas de adyacencia ordenadas. Una ejecución de Tarjan cuesta `O(V + E)` tiempo. Los diccionarios de `tin`, `low`, padres e hijos y la pila recursiva ocupan `O(V)` espacio auxiliar. El grafo ocupa `O(V + E)`; el registro de eventos también puede ocupar `O(V + E)`.

## Pruebas y reproducibilidad

El repositorio contiene pruebas en `tests/test_film_v2.py` y `tests/test_film_v3.py`, además del ejemplo ejecutable `scripts/run_example.py`. Este informe constata que esos archivos existen; no afirma que la suite se haya ejecutado durante la preparación del documento.

Las dependencias principales están listadas en `requirements.txt` (`manim==0.21.0`) y las adicionales para narración en `requirements-film-narration.txt`. La producción requiere también FFmpeg/FFprobe y LaTeX con `dvisvgm`. El `README.md` documenta instalación, ejemplo, render y organización.

## Entregables y enlaces

- **Repositorio y código fuente:** [AED-Articulaciones-Proyecto en GitHub](https://github.com/Pepe17xd/AED-Articulaciones-Proyecto).
- **Video narrado optimizado disponible:** [Articulaciones_v3_optimizada.mp4](https://github.com/Pepe17xd/AED-Articulaciones-Proyecto/blob/main/output/final_v3_optimizada/Articulaciones_v3_optimizada.mp4) (`output/final_v3_optimizada/Articulaciones_v3_optimizada.mp4`).
- **Guion y señales de narración:** `narration/cues.json`.
- **Instrucciones de regeneración:** `narration/REGENERAR.md`.
- **Ejemplo de ejecución:** `scripts/run_example.py`.

El historial actual muestra varios commits de desarrollo, corrección, documentación y entrega; el código no aparece como un único commit final.

### Estado de la edición v4

En este checkout están los archivos fuente `src/animation/film_v4.py` y `narration/cues_v4.json`, con una explicación adicional sobre la propagación de `low`, un rótulo corregido para el ejemplo de camino y el título explícito del caso borde de la raíz. Sin embargo, no se encontró `output/final_v4/Articulaciones_v4.mp4` al preparar el informe. Por ello, el enlace de entrega de arriba apunta a la v3 optimizada; debe sustituirse por el MP4 v4 cuando se haya renderizado y revisado.

## Conclusión

El proyecto combina una implementación propia de Tarjan, una traza validable y una película que explica tanto la regla general como el caso especial de la raíz. La versión optimizada disponible documenta el resultado y satisface los elementos principales del video educativo. Antes de cerrar la entrega, conviene renderizar y revisar la v4, actualizar el enlace del informe si esa será la versión final y exportar este Markdown a PDF si así lo exige la plataforma de entrega.
