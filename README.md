# Practica-Algoritmia

## Mejoras
## comparador_voraz.py
**Eficiencia Algorítmica:** Tal y como refleja el temario, la mejor implementación de este algoritmo voraz está dominada por la función de ordenación (`sorted()` en Python). Por lo tanto, la complejidad temporal de este script es de $O(n \log n)$, siendo $n$ el número de pedidos. El recorrido posterior del bucle `for` tiene un coste lineal de $O(n)$, que queda absorbido por el coste de la ordenación.
* **Optimalidad vs. Programación Dinámica:** Al ser el problema de la mochila discreto (los pedidos no se pueden fraccionar; o van enteros en el camión o no van), este algoritmo voraz **no siempre** encontrará la solución global óptima. Esa es precisamente su función como "mejora": servirá como un excelente punto de referencia (baseline) muy rápido de ejecutar, para compararlo con el tiempo y el resultado exacto que nos dará el módulo de Programación Dinámica.
**Descripcion Escenarios**
1. Escenario Basico: En este escenario diseñamos un bajo numero de pedidos. De esta forma podemos verificar que la integracion entre la programacion dinamica y el backtracking se ha realizado de forma correcta
2. Escenario de Capacidad Critica: Diseñamos una gran cantidad de pedidos que tienen un tamaño pequeño, para asi evaluar la programacion dinamica mediante su complejidad
3. Escenario de Ruteo Completo: Obtenemos un grafo con gran variedad de caminos similares entre si. Con este escenario probamos el backtraking para tratar de buscar el camino minimo mediante una alta cantidad de permutaciones.
4. Escenario de Poda: El escenario de poda incluye restricciones de ventana de tiempo que tiene cada pedido. Demuestra el poder usar de forma correcta la ramificacion y la poda, viendo cuantos nodos se dejan de observar debido a estas restricciones
5. Escenario Libre: Mediante este escenario podremos observar el comportamiento de los pedidos siguiendo casos mas realistas. Evaluar el sistema con condiciones cotidianas en un entorno practico.
