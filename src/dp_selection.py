"""
Módulo: dp_seleccion.py
Descripción: Implementación de Programación Dinámica (Problema de la Mochila 0/1) 
             para la selección óptima de pedidos basada en beneficio y peso.
"""

from modelos import Pedido

def seleccionar_pedidos_dp(pedidos: list, capacidad_maxima: int) -> tuple:
    """
    Selecciona el subconjunto de pedidos que maximiza el beneficio total 
    sin exceder la capacidad máxima C utilizando tabulación.
    
    Args:
        pedidos (list): Lista de objetos de la clase Pedido.
        capacidad_maxima (int): Capacidad de carga del vehículo (debe ser entero).
        
    Returns:
        tuple: (lista_pedidos_seleccionados, beneficio_total, peso_total)
    """
    
    n = len(pedidos)
    C = int(capacidad_maxima)
    
    # 1. Crear la matriz DP (Tabla de subproblemas)
    # Inicializamos con 0s. Filas: pedidos (0 a n), Columnas: capacidades (0 a C)
    dp = [[0 for _ in range(C + 1)] for _ in range(n + 1)]
    
    # 2. Llenar la matriz mediante la relación de recurrencia
    # Recorremos cada pedido i y cada capacidad w posible
    for i in range(1, n + 1):
        pedido_actual = pedidos[i - 1]
        peso = int(pedido_actual.peso)
        beneficio = pedido_actual.beneficio
        
        for w in range(1, C + 1):
            if peso <= w:
                # Decisión: ¿Es mejor incluir el pedido o dejarlo fuera?
                # max(beneficio_si_no_lo_incluyo, beneficio_pedido + mejor_valor_con_espacio_restante)
                dp[i][w] = max(dp[i - 1][w], beneficio + dp[i - 1][w - peso])
            else:
                # El pedido no cabe en esta capacidad 'w', mantenemos el mejor valor anterior
                dp[i][w] = dp[i - 1][w]
                
    # 3. Reconstrucción de la solución (Backtracking sobre la matriz)
    # Empezamos desde la esquina inferior derecha para ver qué pedidos "activaron" el aumento de beneficio
    seleccionados = []
    w_restante = C
    
    for i in range(n, 0, -1):
        # Si el valor en la celda actual es diferente al de la fila de arriba, 
        # significa que el pedido 'i' fue incluido en la solución óptima.
        if dp[i][w_restante] != dp[i - 1][w_restante]:
            pedido_incluido = pedidos[i - 1]
            seleccionados.append(pedido_incluido)
            w_restante -= int(pedido_incluido.peso)
            
    # Invertimos la lista para mostrar los pedidos en su orden original
    seleccionados.reverse()
    
    # Calculamos los totales finales para el retorno
    beneficio_total = dp[n][C]
    peso_total = sum(p.peso for p in seleccionados)
    
    return seleccionados, beneficio_total, peso_total