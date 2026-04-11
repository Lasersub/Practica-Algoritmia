"""
Módulo: comparador_voraz.py
Descripción: Implementación de un algoritmo voraz para el problema de selección 
             de pedidos (Mochila 0/1) utilizando la clase Pedido.
"""

from modelos import Pedido

def seleccionar_pedidos_voraz(pedidos: list, capacidad_maxima: float) -> tuple:
    """
    Selecciona pedidos usando un enfoque voraz basado en el ratio beneficio/peso.
    """
    # Ordenamos los pedidos por su ratio de mayor a menor
    pedidos_ordenados = sorted(pedidos, key=lambda p: p.ratio, reverse=True)
    
    solucion = []
    peso_actual = 0.0
    beneficio_total = 0.0
    
    # Seleccionamos los candidatos que quepan en la mochila
    for pedido in pedidos_ordenados:
        if peso_actual + pedido.peso <= capacidad_maxima:
            solucion.append(pedido)
            peso_actual += pedido.peso
            beneficio_total += pedido.beneficio
            
    return solucion, beneficio_total, peso_actual