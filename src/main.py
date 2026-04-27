# Importamos las clases de modelos.py
import json
import os
from modelos import Pedido, GrafoUrbano, GestorPedidos
from utils.generador_escenarios import GenerarGrafos, guardar_pedidos_escenario
from dp_selection import seleccionar_pedidos_dp

def cargar_pedidos_desde_escenario(nombre_archivo):
    #Definimos la ruta donde están tus archivos según tu estructura
    ruta_escenario = os.path.join("data", "escenarios", nombre_archivo)
    
    # Si no existe en la carpeta data, intentamos buscarlo en la raíz por si acaso
    if not os.path.exists(ruta_escenario):
        ruta_escenario = nombre_archivo 

    if not os.path.exists(ruta_escenario):
        print(f"⚠️ No se encontró {nombre_archivo}. Generándolo ahora...")
        # Si no existe en ningún lado, lo creamos
        guardar_pedidos_escenario(ruta_escenario, 1, 50)
    with open(nombre_archivo, "r") as f:
        lista_dicts = json.load(f)
    return [Pedido(p['id'], p['peso'], p['beneficio']) for p in lista_dicts]

def main():
    print("=== INICIANDO SISTEMA UAH-ROUTE ===")
    
    # ---------------------------------------------------------
    # 1. TEST DEL MÓDULO DE PEDIDOS
    # ---------------------------------------------------------
    print("\n--- 1. Creación de Pedidos ---")
    
    pedidos_totales = cargar_pedidos_desde_escenario("data/escenarios/escenario_capacidad.json")

    # ---------------------------------------------------------
    # 2. TEST DEL MÓDULO DE GRAFO URBANO
    # ---------------------------------------------------------
    print("\n--- 2. Construcción de la Ciudad ---")
    
    ciudad, gestor_inicial = GenerarGrafos(num_nodos=50, num_pedidos=50)
    print(f"Grafo construido con {len(ciudad.nodos)} nodos.")

    capacidad_camion = 100
    seleccionados, beneficio, peso = seleccionar_pedidos_dp(pedidos_totales, capacidad_camion)

    # 4. RESULTADOS
    print("\n--- RESULTADO DE LA PROGRAMACIÓN DINÁMICA ---")
    print(f"Beneficio máximo: {beneficio}€")
    print(f"Peso total cargado: {peso}kg")
    print(f"Pedidos seleccionados para el camión: {[p.id for p in seleccionados]}")

# Main ejecutable
if __name__ == "__main__":
    main()