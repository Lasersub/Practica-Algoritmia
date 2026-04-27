import random
from src.modelos import GrafoUrbano, GestorPedidos, Pedido

# ---------------------------------------------------------
# 1. GENERADOR RECURSIVO (Mejora Tema 1)
# ---------------------------------------------------------
def generador_recursivo_escenarios(n, id_actual):
    """Genera una lista de diccionarios de pedidos de forma recursiva."""
    # El caso base, cuando no quedan mas pedidos por generar
    if n == 0:
        return []
    
    # El caso general
    # pasamos solo el ID, la clase Pedido ya genera peso y beneficio aleatorios.
    pedido_nuevo = Pedido(f"P{id_actual}")
    
    datos_pedido = {
        "id": pedido_nuevo.id,
        "peso": pedido_nuevo.peso,
        "beneficio": pedido_nuevo.beneficio
    }
    
    # La relacion de recurrencia
    return [datos_pedido] + generador_recursivo_escenarios(n - 1, id_actual + 1)


# ---------------------------------------------------------
# 2. GENERADOR MASIVO GRAFOS
# ---------------------------------------------------------
def GenerarGrafos(num_nodos=50, num_pedidos=50):
    """
    Genera un escenario masivo para pruebas de estrés.
    Devuelve un GrafoUrbano conexo y un GestorPedidos poblado.
    """
    print(f"Generando escenario con {num_nodos} nodos y {num_pedidos} pedidos...")
    
    # A. Generar el Grafo Urbano Conexo
    ciudad = GrafoUrbano()
    nodos_ids = [f"Nodo_{i}" for i in range(1, num_nodos + 1)]
    
    # Camino base para evitar nodos aislados (1->2->3...)
    for i in range(len(nodos_ids) - 1):
        ciudad.agregar_arista(nodos_ids[i], nodos_ids[i+1], random.randint(5, 30))
        
    # Calles aleatorias extra para simular cruces
    for _ in range(num_nodos * 2):
        origen = random.choice(nodos_ids)
        destino = random.choice(nodos_ids)
        if origen != destino: 
            ciudad.agregar_arista(origen, destino, random.randint(5, 50))
            
    # B. Generar los Pedidos 
    lista_diccionarios_pedidos = generador_recursivo_escenarios(num_pedidos, 1)
    
    gestor = GestorPedidos()
    for dict_p in lista_diccionarios_pedidos:
        # Reconstruimos el objeto Pedido
        p = Pedido(dict_p["id"], dict_p["peso"], dict_p["beneficio"])
        gestor.agregar_pedido(p)
        
    return ciudad, gestor
