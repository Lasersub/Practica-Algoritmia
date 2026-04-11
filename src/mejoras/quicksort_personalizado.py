"""
Módulo: quicksort_personalizado.py
Descripción: Implementación del algoritmo Divide y Vencerás Quicksort para 
             ordenar pedidos bajo múltiples criterios personalizados.
"""

def es_prioritario(pedido_a, pedido_b):
    """
    Define qué pedido va antes basado en múltiples criterios.
    Queremos orden DESCENDENTE de beneficio, luego DESCENDENTE de urgencia, 
    y luego ASCENDENTE de distancia.
    Devuelve True si pedido_a debe ir ANTES o en la MISMA posición que pedido_b.
    """
    # 1. Criterio: Mayor beneficio
    if pedido_a.beneficio != pedido_b.beneficio:
        return pedido_a.beneficio > pedido_b.beneficio
    
    # 2. Criterio: Mayor urgencia (asumiendo que 10 es más urgente que 1)
    if getattr(pedido_a, 'urgencia', 0) != getattr(pedido_b, 'urgencia', 0):
        return getattr(pedido_a, 'urgencia', 0) > getattr(pedido_b, 'urgencia', 0)
    
    # 3. Criterio: Menor distancia (más cerca es mejor)
    return getattr(pedido_a, 'distancia', float('inf')) < getattr(pedido_b, 'distancia', float('inf'))


def particion(pedidos, inicio, fin):
    """
    Coloca el pivote en su posición definitiva. 
    Los elementos prioritarios van a la izquierda, los demás a la derecha.
    """
    # Escogemos el último elemento como pivote (podría ser el primero como sugiere la teoría)
    pivote = pedidos[fin] 
    i = inicio - 1
    
    for j in range(inicio, fin):
        # Si el elemento actual es prioritario respecto al pivote, lo movemos a la izquierda
        if es_prioritario(pedidos[j], pivote):
            i += 1
            pedidos[i], pedidos[j] = pedidos[j], pedidos[i]
            
    # Colocamos el pivote en su posición final
    pedidos[i + 1], pedidos[fin] = pedidos[fin], pedidos[i + 1]
    return i + 1


def quicksort_multicriterio(pedidos, inicio=0, fin=None):
    """
    Función principal de ordenación recursiva.
    """
    if fin is None:
        fin = len(pedidos) - 1
        
    # Condición base: si el tamaño del vector es suficientemente pequeño (<=1), ya está ordenado
    if inicio < fin:
        # Dividir: obtenemos la posición final del pivote
        indice_pivote = particion(pedidos, inicio, fin)
        
        # Conquistar: llamadas recursivas a ambos lados del pivote
        quicksort_multicriterio(pedidos, inicio, indice_pivote - 1)
        quicksort_multicriterio(pedidos, indice_pivote + 1, fin)

    return pedidos