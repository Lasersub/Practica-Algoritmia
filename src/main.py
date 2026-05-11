import os
import json
import time # <--- AÑADIDO: Importar time para mediciones

from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp
from backtracking_ruta import calcular_ruta_tsp # <--- NUEVO: Importar ruteo
from mejoras.comparador_voraz import seleccionar_pedidos_voraz
from mejoras.quicksort_personalizado import quicksort_multicriterio


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
        nombre, n, capacidad = "capacidad", 50, 100
    elif opcion == "3":
        nombre, n, capacidad = "ruteo", 20, 80
    elif opcion == "4":
        nombre, n, capacidad = "poda", 15, 60
    elif opcion == "5":
        nombre, n, capacidad = "libre", 10, 50
    else: return

    print(f"\n--- EJECUTANDO: {nombre.upper()} ---")

    nombre_archivo = f"escenario_{nombre}.json"
    guardar_pedidos_escenario(nombre_archivo, 1, n) 
    print(f"[Sistema] Archivo {nombre_archivo} generado y guardado.")
    # 2. CREACIÓN DE DATOS
    ciudad, gestor = GenerarGrafos(num_nodos=n, num_pedidos=n)
    pedidos_totales = cargar_pedidos_desde_escenario(nombre_archivo)
    
    # NUEVO: Asignar destino a cada pedido antes de nada
    for i in range(len(pedidos_totales)):
        pedidos_totales[i].destino = f"Nodo_{i+1}"

    # ---------------------------------------------------------
    # 2.5 PREPROCESADO (Mejora: Quicksort Multicriterio)
    # ---------------------------------------------------------
    print("\n--- PREPARACIÓN DEL CATÁLOGO (Quicksort) ---")
    print("Seleccione el criterio de prioridad para el catálogo:")
    print(" 1. Mayor Beneficio")
    print(" 2. Menor Peso")
    print(" 3. Mayor Ratio (Beneficio/Peso)")
    op_sort = input("Opción: ")
    
    criterio = "beneficio"
    if op_sort == "2": criterio = "peso"
    elif op_sort == "3": criterio = "ratio"

    inicio_qs = time.perf_counter()
    quicksort_multicriterio(pedidos_totales, criterio=criterio)
    t_qs = time.perf_counter() - inicio_qs

    print(f" > Catálogo ordenado en {t_qs:.6f}s bajo criterio: {criterio}")
    for p in pedidos_totales[:10]: # Muestra los 10 primeros pedidos tras ordenación
        print(f"   [ID: {p.id}] {p.beneficio}€ | {p.peso}kg | Ratio: {p.ratio:.2f}")
    
    # 3. SELECCIÓN (Fase 2)
    # AÑADIDO: Medición de tiempo para DP
    inicio_dp = time.perf_counter()
    sel_dp, ben_dp, peso_dp = seleccionar_pedidos_dp(pedidos_totales, capacidad)
    tiempo_dp = time.perf_counter() - inicio_dp
    
    # AÑADIDO: Medición de tiempo para Voraz
    inicio_v = time.perf_counter()
    sel_v, ben_v, peso_v = seleccionar_pedidos_voraz(pedidos_totales, capacidad)
    tiempo_v = time.perf_counter() - inicio_v

    # Modificado el print para mostrar los tiempos al lado del beneficio
    print(f"\n[DP] Beneficio: {ben_dp}€ (Tiempo: {tiempo_dp:.6f}s) | [Voraz] Beneficio: {ben_v}€ (Tiempo: {tiempo_v:.6f}s)")

    # --------------------------------------
    # 4. RUTEO CON BACKTRACKING (Fase 3)
    # --------------------------------------
    print("\n--- OPTIMIZACIÓN DE RUTA (Backtracking) ---")

    destinos_a_visitar = [p.destino for p in sel_dp if p.destino != "Nodo_1"]

    if len(destinos_a_visitar) > 0:
        if opcion == "1":
            inicio_sin = time.perf_counter()
            _, _, exp_sin = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar, usar_poda=False)
            tiempo_sin = time.perf_counter() - inicio_sin

            inicio_con = time.perf_counter()
            ruta, kms, explorados = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar, usar_poda=True)
            tiempo_con = time.perf_counter() - inicio_con

            if ruta:
                print(f"  > Mejor ruta: {' -> '.join(ruta)}")
                print(f"  > Distancia total: {kms} km")
                print(f"  > Nodos explorados (CON poda): {explorados} en {tiempo_con:.6f}s")
                print(f"  > Nodos explorados (SIN poda): {exp_sin} en {tiempo_sin:.6f}s")
            else:
                print("  [!] No se pudo encontrar una ruta valida.")

        elif opcion == "2":
            x = len(destinos_a_visitar)
            print(f"  [!] Escenario de estres para DP (N=50).")
            print(f"  [!] La DP selecciono {x} pedidos con un beneficio optimo.")
            print(f"  [!] TSP exacto omitido: con {x} destinos la explosion")
            print(f"      combinatoria O(n!) hace inviable el ruteo exacto.")
            print(f"      Consultar analisis de complejidad en el informe.")

        else:
            CAP_TSP = 8
            if len(destinos_a_visitar) > CAP_TSP:
                print(f"  [!] Destinos seleccionados: {len(destinos_a_visitar)}.")
                print(f"  [!] Aplicando cap de {CAP_TSP} destinos a ambas versiones")
                print(f"      para garantizar una comparativa valida con/sin poda.")
                destinos_a_visitar = destinos_a_visitar[:CAP_TSP]

            inicio_sin = time.perf_counter()
            _, _, exp_sin = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar, usar_poda=False)
            tiempo_sin = time.perf_counter() - inicio_sin

            inicio_con = time.perf_counter()
            ruta, kms, explorados = calcular_ruta_tsp(ciudad, "Nodo_1", destinos_a_visitar, usar_poda=True)
            tiempo_con = time.perf_counter() - inicio_con

            if ruta:
                print(f"  > Mejor ruta: {' -> '.join(ruta)}")
                print(f"  > Distancia total: {kms} km")
                print(f"  > Nodos explorados (CON poda): {explorados} en {tiempo_con:.6f}s")
                print(f"  > Nodos explorados (SIN poda): {exp_sin} en {tiempo_sin:.6f}s")
            else:
                print("  [!] No se pudo encontrar una ruta valida.")
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