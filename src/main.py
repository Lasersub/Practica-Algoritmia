# Importamos las clases de modelos.py
from modelos import Pedido, GrafoUrbano, GestorPedidos

def main():
    print("=== INICIANDO SISTEMA UAH-ROUTE ===")
    
    # ---------------------------------------------------------
    # 1. TEST DEL MÓDULO DE PEDIDOS
    # ---------------------------------------------------------
    print("\n--- 1. Creación de Pedidos ---")
    
    # Pedidos de prueba
    p1 = Pedido(id_pedido="P001", peso=10, beneficio=50)
    p2 = Pedido(id_pedido="P002", peso=5, beneficio=60)
    p3 = Pedido(id_pedido="P003", peso=15, beneficio=45)
    
    gestor = GestorPedidos()
    
    gestor.agregar_pedido(p1)
    gestor.agregar_pedido(p2)
    gestor.agregar_pedido(p3)
    
    # Depuración
    print(f"Estado inicial: {gestor.mostrar_pedidos()}")
    print(f"El ratio (beneficio/peso) del pedido P002 es: {p2.ratio}")

    # ---------------------------------------------------------
    # 2. TEST DEL MÓDULO DE GRAFO URBANO
    # ---------------------------------------------------------
    print("\n--- 2. Construcción de la Ciudad ---")
    
    ciudad = GrafoUrbano()
    
    # Añadimos conexiones y nodos, los nodos se añaden solos ya que las aristas necesitan que los nodos existan para conectarlos
    ciudad.agregar_arista("Alcalá", "Madrid", 30)
    ciudad.agregar_arista("Madrid", "Getafe", 15)
    ciudad.agregar_arista("Alcalá", "Torrejón", 10)
    
    # Comprobamos el __repr__ del grafo
    print(f"Estado del grafo: {ciudad}")
    
    # Comprobamos las distancias y vecinos
    print(f"Distancia de Alcalá a Madrid: {ciudad.obtener_distancia('Alcalá', 'Madrid')} km")
    # Getafe y Alcalá no están conectados directamente, debería dar infinito
    print(f"Distancia de Alcalá a Getafe: {ciudad.obtener_distancia('Alcalá', 'Getafe')} km") 
    print(f"Nodos conectados directamente a Alcalá: {ciudad.obtener_vecinos('Alcalá')}")

# Main ejecutable
if __name__ == "__main__":
    main()