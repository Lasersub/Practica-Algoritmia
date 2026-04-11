# Practica-Algoritmia

## Mejoras
## comparador_voraz.py
**Eficiencia Algorítmica:** Tal y como refleja el temario, la mejor implementación de este algoritmo voraz está dominada por la función de ordenación (`sorted()` en Python). Por lo tanto, la complejidad temporal de este script es de $O(n \log n)$, siendo $n$ el número de pedidos. El recorrido posterior del bucle `for` tiene un coste lineal de $O(n)$, que queda absorbido por el coste de la ordenación.
* **Optimalidad vs. Programación Dinámica:** Al ser el problema de la mochila discreto (los pedidos no se pueden fraccionar; o van enteros en el camión o no van), este algoritmo voraz **no siempre** encontrará la solución global óptima. Esa es precisamente su función como "mejora": servirá como un excelente punto de referencia (baseline) muy rápido de ejecutar, para compararlo con el tiempo y el resultado exacto que nos dará el módulo de Programación Dinámica.
