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
    mejor_ruta = None
    mejor_distancia = float('inf')
    nodos_explorados = 0
    
    nodos_objetivo = set(nodos_a_visitar)
    total_objetivos = len(nodos_objetivo)


    def backtrack(nodo_actual, visitados, ruta_actual, distancia_actual):
        # Utilizamos variables del entorno superior
        nonlocal mejor_ruta, mejor_distancia, nodos_explorados
        nodos_explorados += 1
        
        # 1. CONDICIÓN DE PODA (Ramificación y Poda)
        # Si la distancia que llevamos ya es peor que la mejor que hemos encontrado
        # por otra rama, cortamos la exploración aquí mismo.
        if usar_poda and distancia_actual >= mejor_distancia:
            return
            
        # 2. CASO BASE: ¿Hemos entregado todos los pedidos?
        if len(visitados) == total_objetivos:
            # Queda el último paso: Volver al origen
            dist_retorno = grafo.obtener_distancia(nodo_actual, origen)
            distancia_total = distancia_actual + dist_retorno
            
            # Si se puede volver al origen y la ruta total mejora lo conocido
            if dist_retorno != float('inf'):
                if not usar_poda or distancia_total < mejor_distancia:
                    mejor_distancia = distancia_total
                    # Guardamos una copia de la ruta añadiendo el retorno
                    mejor_ruta = ruta_actual + [origen]
            return

        # 3. RECURSIÓN: Explorar los posibles siguientes pasos
        vecinos = grafo.obtener_vecinos(nodo_actual)
        
        for vecino, peso in vecinos:
            # Solo iteramos por destinos que nos interesan y que aún no hemos pisado
            if vecino in nodos_objetivo and vecino not in visitados:
                
                # a) Tomar la decisión (Avanzar)
                visitados.add(vecino)
                ruta_actual.append(vecino)
                
                # b) Llamada recursiva (Profundizar en el árbol)
                backtrack(vecino, visitados, ruta_actual, distancia_actual + peso)
                
                # c) Deshacer la decisión (Backtracking - Volver atrás)
                # Esto es vital para evitar la "corrupción" del entorno explicada en el Tema 5
                ruta_actual.pop()
                visitados.remove(vecino)

    # 4. LLAMADA INICIAL
    # Empezamos en el origen, sin haber visitado destinos, con la ruta inicial y 0 km recorridos.
    backtrack(origen, set(), [origen], 0)
    
    return mejor_ruta, mejor_distancia, nodos_explorados