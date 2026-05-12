import os
import json
import time
import random

from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp
from backtracking_ruta import calcular_ruta_tsp
from mejoras.comparador_voraz import seleccionar_pedidos_voraz
from mejoras.quicksort_personalizado import quicksort_multicriterio


def menu():

    print("--- SISTEMA LOGÍSTICO UAH-ROUTE ---")

    print("1. Escenario 1: Básico (N=5)")
    print("2. Escenario 2: Capacidad Crítica (N=50)")
    print("3. Escenario 3: Ruteo Complejo (N=20)")
    print("4. Escenario 4: Escenario de Poda (N=15)")
    print("5. Escenario 5: Escenario Libre")
    print("6. Salir")
  
    return input("Elige el escenario que quieres probar: ")

# Función de carga para leer el destino del JSON
def cargar_pedidos_desde_escenario(nombre_archivo):
    ruta_final = f"data/escenarios/{nombre_archivo}"
    if not os.path.exists(ruta_final): return []
    
    with open(ruta_final, "r") as archivo:
        lista_dicts = json.load(archivo)
    # Añadimos p.get('destino') para que no falle si no existe
    return [Pedido(p['id'], p.get('destino', 'Desconocido'), p['peso'], p['beneficio']) for p in lista_dicts]

def ejecutar_sistema(opcion):
    #1. CONFIGURACIÓN
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


    resumen_txt = f"ESCENARIO: {nombre.upper()} | N={n} | Capacidad={capacidad}kg\n"

    nombre_archivo = f"escenario_{nombre}.json"
    guardar_pedidos_escenario(nombre_archivo, 1, n) 
    print(f"Archivo {nombre_archivo} generado y guardado.")
    
    #2. CREACIÓN DE DATOS
    ciudad, _ = GenerarGrafos(num_nodos=n, num_pedidos=0)
    pedidos_totales = cargar_pedidos_desde_escenario(nombre_archivo)
    
    #Asignamos destino a cada pedido
    for i in range(len(pedidos_totales)):
        pedidos_totales[i].destino = f"Nodo_{i+1}"

    #Mejora Quicksort
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

    print("\n--- CATÁLOGO DE PEDIDOS (Ordenado por Prioridad) ---")
    for p in pedidos_totales[:10]:
        print(f"  > [Pedido {p.id}] Beneficio: {p.beneficio}€ | Peso: {p.peso}kg")
    if len(pedidos_totales) > 10:
        print(f"  > ... y {len(pedidos_totales) - 10} pedidos más.")
    print(f"  [Tiempo de ordenación: {t_qs:.6f}s]")

    resumen_txt += f"Ordenación ({criterio}): {t_qs:.6f}s\n"
    
    # 3. SELECCIÓN (Fase 2)
    inicio_dp = time.perf_counter()
    sel_dp, ben_dp, peso_dp = seleccionar_pedidos_dp(pedidos_totales, capacidad)
    tiempo_dp = time.perf_counter() - inicio_dp
    
    inicio_v = time.perf_counter()
    sel_v, ben_v, peso_v = seleccionar_pedidos_voraz(pedidos_totales, capacidad)
    tiempo_v = time.perf_counter() - inicio_v

    print(f"\n[PD] Beneficio: {ben_dp}€ ({tiempo_dp:.6f}s) | [Voraz] Beneficio: {ben_v}€ ({tiempo_v:.6f}s)")
    resumen_txt += f"PD: {ben_dp}€ ({tiempo_dp:.6f}s) | Voraz: {ben_v}€ ({tiempo_v:.6f}s)\n"

    # 4. RUTEO CON BACKTRACKING (Fase 3)
    print("\n--- OPTIMIZACIÓN DE RUTA (Backtracking) ---")
    destinos_a_visitar = [p.destino for p in sel_dp if p.destino != "Nodo_1"]
    resumen_ruteo = ""

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
                resumen_ruteo = f"Ruta: {kms}km | Poda: {explorados} n. | Sin Poda: {exp_sin} n."
            else:
                resumen_ruteo = "No se pudo encontrar una ruta válida."

        elif opcion == "2":
            x = len(destinos_a_visitar)
            resumen_ruteo = f"TSP omitido (N={x} destinos) por complejidad O(n!)."
            print(f"   {resumen_ruteo}")

        else:
            CAP_TSP = 8
            if len(destinos_a_visitar) > CAP_TSP:
                print(f"   Limitando a {CAP_TSP} destinos para la comparativa.")
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
                resumen_ruteo = f"Ruta: {kms}km | Poda: {explorados} n. | Sin Poda: {exp_sin} n."
            else:
                resumen_ruteo = "No se pudo encontrar una ruta válida."
    else:
        resumen_ruteo = "No hay pedidos seleccionados."
        print(f"   {resumen_ruteo}")

    resumen_txt += f"Ruteo: {resumen_ruteo}\n"

    #Guardado final en .txt
    # Obtenemos la ruta absoluta de la carpeta donde está este main.py
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_txt = os.path.join(directorio_actual, "data", "resultados.txt")
    
    # Aseguramos que la carpeta data existe
    os.makedirs(os.path.join(directorio_actual, "data"), exist_ok=True)
    
    print("\nIntentando escribir en: resultados.txt")

    try:
        # Abrimos en modo 'a+' (añadir y leer) para forzar la creación si no existe
        with open(ruta_txt, "a+", encoding="utf-8") as f:
            f.write("\n" + "="*70 + "\n")
            f.write(f"LOG: {time.strftime('%H:%M:%S')} - {time.strftime('%d/%m/%Y')}\n")
            f.write(resumen_txt)
            f.write("="*70 + "\n")
            
            #Aseguramos que los datos pasen del buffer de Python
            # al hardware para evitar pérdida de métricas en caso de cierre inesperado.
            f.flush()
            os.fsync(f.fileno())
            
        print(f"EXITO: Se han escrito los datos de forma correcta en el archivo.")
    except Exception as e:
        print(f"ERROR CRÍTICO al escribir el archivo: {e}")

    print(f"\nProceso finalizado. Revisa el archivo resultados.txt para ver lo obtenido.")
    input("\nPresiona Enter para volver al menú...")

def main():
    random.seed(time.time())
    if not os.path.exists("data/escenarios"): 
        os.makedirs("data/escenarios")
    while True:
        opcion = menu()
        if opcion == "6": 
            break
        elif opcion in "12345": 
            ejecutar_sistema(opcion)

if __name__ == "__main__":
    main()