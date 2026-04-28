# Importamos las clases de modelos.py
import json

from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp

def cargar_pedidos_desde_escenario(nombre_archivo):
    ruta_final = f"data/escenarios/{nombre_archivo}"
    
    with open(ruta_final, "r") as archivo:
        lista_dicts = json.load(archivo)
    return [Pedido(p['id'], p['peso'], p['beneficio']) for p in lista_dicts]

def main():
    print("=== INICIANDO SISTEMA UAH-ROUTE ===")
    
    # ---------------------------------------------------------
    # 1. TEST DEL MÓDULO DE PEDIDOS
    # ---------------------------------------------------------
    print("--- 1. Cargando pedidos desde escenario de capacidad critica ---")
    
    pedidos_totales = cargar_pedidos_desde_escenario("escenario_capacidad.json")

    # ---------------------------------------------------------
    # 2. TEST DEL MÓDULO DE GRAFO URBANO
    # ---------------------------------------------------------
    print("--- 2. Construcción de la Ciudad ---")
    
    ciudad, gestor_inicial = GenerarGrafos(num_nodos=50, num_pedidos=50)
    print(f"Grafo construido con {len(ciudad.nodos)} nodos.")

    capacidad_camion = 100
    seleccionados, beneficio, peso = seleccionar_pedidos_dp(pedidos_totales, capacidad_camion)

    # 3. RESULTADOS
    print("\n--- RESULTADO DE LA PROGRAMACIÓN DINÁMICA ---")
    print(f"Beneficio máximo: {beneficio}€")
    print(f"Peso total cargado: {peso}kg")
    print(f"Pedidos seleccionados para el camión: {[p.id for p in seleccionados]}")

# Main ejecutable
if __name__ == "__main__":
    main()