import os
import json
from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp
from backtracking_ruta import calcular_ruta_tsp # <--- NUEVO: Importar ruteo
from mejoras.comparador_voraz import seleccionar_pedidos_voraz

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

# NUEVO: Función de carga actualizada para leer el destino del JSON
def cargar_pedidos_desde_escenario(nombre_archivo):
    ruta_final = f"data/escenarios/{nombre_archivo}"
    if not os.path.exists(ruta_final): return []
    
    with open(ruta_final, "r") as archivo:
        lista_dicts = json.load(archivo)
    # Añadimos p.get('destino') para que no falle si no existe
    return [Pedido(p['id'], p.get('destino', 'Desconocido'), p['peso'], p['beneficio']) for p in lista_dicts]

def ejecutar_sistema(opcion):
    # 1. CONFIGURACIÓN
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

    # 2. CREACIÓN DE DATOS
    ciudad, gestor = GenerarGrafos(num_nodos=n, num_pedidos=n)
    pedidos_totales = gestor.mostrar_pedidos()
    
    # NUEVO: Asignar destino a cada pedido antes de nada
    for i in range(len(pedidos_totales)):
        pedidos_totales[i].destino = f"Nodo_{i+1}"

    # 3. SELECCIÓN (Fase 2)
    sel_dp, ben_dp, peso_dp = seleccionar_pedidos_dp(pedidos_totales, capacidad)
    sel_v, ben_v, peso_v = seleccionar_pedidos_voraz(pedidos_totales, capacidad)

    print(f"\n[DP] Beneficio: {ben_dp}€ | [Voraz] Beneficio: {ben_v}€")

    # ---------------------------------------------------------
    # 4. RUTEO CON BACKTRACKING (Fase 3) - NUEVO
    # ---------------------------------------------------------
    print("\n--- OPTIMIZACIÓN DE RUTA (Backtracking) ---")
    
    # Extraemos solo los nombres de los nodos de los pedidos elegidos
    destinos_a_visitar = [p.destino for p in sel_dp]
    
    if len(destinos_a_visitar) > 0:
        # Llamamos al algoritmo de backtracking
        # Salida desde 'Nodo_1' (Almacén Central)
        ruta, kms, explorados = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar)
        
        if ruta:
            print(f"  > Mejor ruta: {' -> '.join(ruta)}")
            print(f"  > Distancia total: {kms} km")
            print(f"  > Nodos explorados: {explorados}")
        else:
            print("  [!] No se pudo encontrar una ruta válida.")
    else:
        print("  [!] No hay pedidos seleccionados para repartir.")

    input("\nPresiona Enter para continuar...")

def main():
    if not os.path.exists("data/escenarios"): os.makedirs("data/escenarios")
    while True:
        opcion = menu()
        if opcion == "6": break
        elif opcion in "12345": ejecutar_sistema(opcion)

if __name__ == "__main__":
    main()