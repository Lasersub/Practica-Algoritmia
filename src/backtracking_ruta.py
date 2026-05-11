"""
Módulo: backtracking_ruta.py
Descripción: Implementación del algoritmo TSP mediante Backtracking 
             con y sin estrategias de Ramificación y Poda.
"""

def calcular_ruta_tsp(grafo, origen, nodos_a_visitar, usar_poda=True):
    """
    Calcula la ruta más corta que visita todos los nodos indicados y vuelve al origen.
    
    Args:
        grafo (GrafoUrbano): La instancia de la ciudad.
        origen (str): ID del nodo de salida (ej. 'Almacen').
        nodos_a_visitar (list): Lista de IDs de los destinos de los pedidos.
        usar_poda (bool): Activa o desactiva la Ramificación y Poda.
        
    Returns:
        tuple: (mejor_ruta (list), mejor_distancia (float), nodos_explorados (int))
    """
    import heapq

    def dijkstra(inicio):
        dist = {nodo: float('inf') for nodo in grafo.nodos}
        dist[inicio] = 0
        heap = [(0, inicio)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for vecino, peso in grafo.obtener_vecinos(u):
                nd = d + peso
                if nd < dist[vecino]:
                    dist[vecino] = nd
                    heapq.heappush(heap, (nd, vecino))
        return dist

    nodos_objetivo = set(nodos_a_visitar)
    total_objetivos = len(nodos_objetivo)
    nodos_relevantes = [origen] + list(nodos_objetivo)

    dist_real = {}
    for nodo in nodos_relevantes:
        dist_real[nodo] = dijkstra(nodo)

    # Verify all required paths exist
    for a in nodos_relevantes:
        for b in nodos_relevantes:
            if a != b and dist_real[a][b] == float('inf'):
                return (None, float('inf'), 0)

    mejor_ruta = None
    mejor_distancia = float('inf')
    nodos_explorados = 0

    def backtrack(nodo_actual, visitados, ruta_actual, distancia_actual):
        nonlocal mejor_ruta, mejor_distancia, nodos_explorados
        nodos_explorados += 1

        # 1. CONDICIÓN DE PODA (Ramificación y Poda)
        if usar_poda and distancia_actual >= mejor_distancia:
            return

        # 2. CASO BASE: ¿Hemos entregado todos los pedidos?
        if len(visitados) == total_objetivos:
            dist_retorno = dist_real[nodo_actual][origen]
            distancia_total = distancia_actual + dist_retorno

            if dist_retorno != float('inf'):
                if not usar_poda or distancia_total < mejor_distancia:
                    mejor_distancia = distancia_total
                    mejor_ruta = list(ruta_actual) if ruta_actual[-1] == origen else ruta_actual + [origen]
            return

        # 3. RECURSIÓN: Explorar todos los destinos no visitados directamente
        for candidato in nodos_objetivo:
            if candidato not in visitados:
                peso = dist_real[nodo_actual][candidato]

                # a) Tomar la decisión (Avanzar)
                visitados.add(candidato)
                ruta_actual.append(candidato)

                # b) Llamada recursiva (Profundizar en el árbol)
                backtrack(candidato, visitados, ruta_actual, distancia_actual + peso)

                # c) Deshacer la decisión (Backtracking - Volver atrás)
                ruta_actual.pop()
                visitados.remove(candidato)

    # 4. LLAMADA INICIAL
    backtrack(origen, set(), [origen], 0)

    return mejor_ruta, mejor_distancia, nodos_explorados