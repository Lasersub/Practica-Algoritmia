"""
Módulo: comparador_voraz.py
Descripción: Implementación de un algoritmo voraz para el problema de selección 
             de pedidos (Mochila 0/1). Actúa como comparador frente a la solución 
             óptima de Programación Dinámica.
"""

def seleccionar_pedidos_voraz(pedidos: list, capacidad_maxima: float) -> tuple:
    """
    Selecciona pedidos utilizando una estrategia voraz basada en el ratio beneficio/peso.
    
    Args:
        pedidos (list): Lista de tuplas representando pedidos (id, peso, beneficio).
        capacidad_maxima (float): Capacidad máxima de carga del vehículo (C).
        
    Returns:
        tuple: (lista_pedidos_seleccionados, beneficio_total, peso_total)
    """
    # 1. Función de selección: Ordenar pedidos por ratio (beneficio / peso) de mayor a menor
    # Esta es la opción (c) del temario: Objetos de mayor relación valor/volumen
    pedidos_ordenados = sorted(
        pedidos, 
        key=lambda p: p[2] / p[1] if p[1] > 0 else 0, 
        reverse=True
    )
    
    solucion = []
    peso_actual = 0.0
    beneficio_total = 0.0
    
    # 2. Iterar sobre los candidatos ya ordenados
    for pedido in pedidos_ordenados:
        id_pedido, peso, beneficio = pedido
        
        # 3. Función es_completable: Comprobar si el pedido cabe en el camión
        if peso_actual + peso <= capacidad_maxima:
            solucion.append(pedido)
            peso_actual += peso
            beneficio_total += beneficio
            
    # Devolvemos la solución alcanzada y sus métricas para facilitar la comparación
    return solucion, beneficio_total, peso_actual

# --- Código de prueba rápida para verificar el funcionamiento ---
if __name__ == "__main__":
    # Escenario de prueba simple
    pedidos_prueba = [
        ("P1", 1, 100),  # (id, peso, beneficio) - Ratio: 100
        ("P2", 1, 1),    # Ratio: 1
        ("P3", 0.5, 10), # Ratio: 20
        ("P4", 2, 13),   # Ratio: 6.5
        ("P5", 5, 50)    # Ratio: 10
    ]
    capacidad = 8.0
    
    seleccion, ben_total, pes_total = seleccionar_pedidos_voraz(pedidos_prueba, capacidad)
    
    print(f"Capacidad máxima: {capacidad}")
    print(f"Pedidos seleccionados: {[p[0] for p in seleccion]}")
    print(f"Beneficio total: {ben_total}€")
    print(f"Peso total ocupado: {pes_total}")