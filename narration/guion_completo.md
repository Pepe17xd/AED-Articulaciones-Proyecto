# Guion completo de narración

## 01_red

Imagina una red de transporte en la que las estaciones están conectadas por rutas.

## 02_falla

¿Qué pasaría si una estación importante dejara de funcionar? Al retirar Centro y sus conexiones, algunas estaciones quedan separadas. Identificar estos puntos críticos nos ayuda a anticipar fallas.

## 03_definicion

Un punto de articulación es un vértice cuya eliminación aumenta el número de componentes conexas del grafo.

## 04_ciclo

En este ciclo existe una ruta alternativa: al retirar B, A y C siguen conectados.

## 05_camino

En cambio, al retirar Q del camino, P y R quedan separados.

## 06_dfs

La búsqueda en profundidad, o DFS, avanza por una ruta hasta que ya no puede continuar y luego retrocede. Al descubrir cada vértice registramos su tiempo de entrada, llamado tin. Low resume el tiempo de entrada más antiguo que puede alcanzar su subárbol DFS, bajando por aristas del árbol y usando, como máximo, una arista de retorno hacia un ancestro.

## 07_retorno

Aquí D encuentra una arista de retorno hacia B.

## 08_low

Esa ruta alternativa permite que low de D baje hasta el tiempo de entrada de B. Al retroceder, la información se propaga hacia sus antecesores.

## 09_igualdad

Para un vértice que no es raíz, al terminar de explorar un hijo DFS comparamos el low del hijo con el tin del vértice. Si el low del hijo es mayor o igual, ese vértice es una articulación. La igualdad también cuenta: volver al propio vértice no evita que su eliminación separe el subárbol.

## 10_recorrido

Observemos la ejecución real. DFS descubrirá los vértices en orden alfabético entre vecinos disponibles. Sigamos las aristas del árbol y los cambios de los valores mientras avanza la búsqueda.

## 10a_descubre

Comenzamos en A. Al descubrir un vértice, tin y low empiezan con el mismo valor.

## 10b_retorno

Desde D encontramos una arista de retorno hacia B. Esta ruta permite reducir el valor low.

## 10c_articulacion

Al regresar desde F, E cumple la condición de articulación: el subárbol de F no alcanza un ancestro anterior de E.

## 10d_raiz

Finalmente A es la raíz y tiene dos hijos directos en el árbol DFS: B y G.

## 11_resultado

En esta ejecución, las articulaciones son A, B, D y E.

## 12_raiz_uno

La raíz se trata de forma distinta. Con un solo hijo en el árbol DFS, no es articulación.

## 13_raiz_dos

Si tiene al menos dos hijos directos en el árbol DFS, sí es articulación. Contamos hijos del árbol de búsqueda, no simplemente vecinos del grafo: un vecino puede haber sido descubierto por otro camino.

## 14_complejidad

Con listas de adyacencia, DFS descubre cada vértice una vez y examina cada arista desde sus extremos. Por eso el tiempo es proporcional a la suma de vértices y aristas: O de V más E. El espacio auxiliar es lineal en el número de vértices, además del espacio del grafo.

## 15_conclusion

DFS, junto con tin y low, permite detectar eficientemente los puntos cuya falla puede dividir una red. En nuestro ejemplo, las articulaciones son A, B, D y E.
