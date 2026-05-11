import os
import json
from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp
from mejoras.comparador_voraz import seleccionar_pedidos_voraz
from backtracking_ruta import calcular_ruta_tsp

def menu():
    print("\n" + "="*50)
    print("      SISTEMA LOGÍSTICO UAH-ROUTE (2025-26)")
    print("="*50)
    print("1. Escenario 1: Básico (N=5)")
    print("2. Escenario 2: Capacidad Crítica (N=50)")
    print("3. Escenario 3: Ruteo Complejo (N=20)")
    print("4. Escenario 4: Escenario de Poda (N=15)")
    print("5. Escenario 5: Escenario Libre")
    print("6. Salir")
    print("="*50)
    return input("Elige el escenario que quieres probar: ")

def ejecutar_sistema(opcion):
    if opcion == "1":
        nombre, n, capacidad = "basico", 5, 30
    elif opcion == "2":
        nombre, n, capacidad = "critico", 50, 100
    elif opcion == "3":
        nombre, n, capacidad = "ruteo", 20, 80
    elif opcion == "4":
        nombre, n, capacidad = "poda", 15, 60
    elif opcion == "5":
        nombre, n, capacidad = "libre", 10, 50
    else: return

    print(f"\n--- EJECUTANDO: {nombre.upper()} ---")

    # 1. CREACIÓN DE CIUDAD Y PEDIDOS (Sincronizados por nodo)
    ciudad, gestor = GenerarGrafos(num_nodos=n, num_pedidos=n)
    
    # Asignamos cada pedido a un nodo específico (P1 -> Nodo_1, etc.)
    pedidos_totales = gestor.mostrar_pedidos()
    for i in range(len(pedidos_totales)):
        pedidos_totales[i].destino = f"Nodo_{i+1}"

    # 2. GUARDADO Y MOSTRAR DISTRIBUCIÓN
    guardar_pedidos_escenario(fichero := f"escenario_{nombre}.json", 1, n)
    print("\n[*] Ubicación de los pedidos en la ciudad:")
    for p in pedidos_totales:
        print(f"  - El {p.id} debe entregarse en el {p.destino}")

    # 3. SELECCIÓN (DP vs VORAZ)
    print("\n" + "-"*45 + "\n--- ANÁLISIS DE SELECCIÓN ---\n" + "-"*45)
    sel_dp, ben_dp, peso_dp = seleccionar_pedidos_dp(pedidos_totales, capacidad)
    sel_v, ben_v, peso_v = seleccionar_pedidos_voraz(pedidos_totales, capacidad)

    print(f"{'ALGORITMO':<15} | {'BENEFICIO':<10} | {'PESO':<10} | {'PEDIDOS'}")
    print(f"{'P. Dinámica':<15} | {ben_dp:<10} | {peso_dp:<10} | {len(sel_dp)}")
    print(f"{'Voraz':<15} | {ben_v:<10} | {peso_v:<10} | {len(sel_v)}")

    # 4. RUTEO (Backtracking)
    print("\n" + "-"*45 + "\n--- OPTIMIZACIÓN DE RUTA (Backtracking) ---\n" + "-"*45)
    
    # Extraemos los nombres de los nodos donde hay que entregar
    destinos_a_visitar = [p.destino for p in sel_dp]
    
    # Llamamos a tu compañero (Backtracking)
    ruta, kms, explorados = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar)

    if ruta:
        print(f"[✓] Mejor ruta encontrada: {' -> '.join(ruta)}")
        print(f"[✓] Distancia total: {kms} km")
        print(f"[i] Nodos explorados por el algoritmo: {explorados}")
    else:
        print("[!] No se encontró una ruta válida que conecte todos los puntos.")

    input("\nPresiona Enter para continuar...")

def main():
    if not os.path.exists("data/escenarios"): os.makedirs("data/escenarios")
    while True:
        opc = menu()
        if opc == "6": break
        elif opc in "12345": ejecutar_sistema(opc)

if __name__ == "__main__":
    main()