# UAH-Route — Sistema de Optimización Logística Urbana

**Práctica 4-5 | Algoritmia y Complejidad | Curso 2025-26**  
Universidad de Alcalá — Grado en Ingeniería Informática

---

## Descripción

UAH-Route es un sistema que resuelve dos problemas clásicos de optimización
aplicados a la logística urbana:

1. **Selección de pedidos** — dado un vehículo con capacidad limitada,
   seleccionar el subconjunto de pedidos que maximice el beneficio sin
   superar la capacidad. Modelado como el **Problema de la Mochila 0/1**
   y resuelto con **Programación Dinámica (Tema 4)**.

2. **Planificación de ruta** — dados los pedidos seleccionados, calcular
   el orden de entrega que minimice la distancia total recorrida. Modelado
   como el **Problema del Viajante de Comercio (TSP)** y resuelto con
   **Backtracking y Ramificación y Poda (Tema 5)**.


## Cómo ejecutar

Desde la carpeta `src/`:

bash: 
python main.py
```

Al iniciar, el sistema pregunta el modo de ejecución:

| Modo | Descripción |
|------|-------------|
| **1 — Demostración** | Datos fijos y reproducibles. Los resultados son siempre los mismos. Ideal para verificar el comportamiento de los algoritmos. |
| **2 — Generación** | Datos aleatorios nuevos en cada ejecución. Demuestra la escalabilidad del sistema. |

A continuación se selecciona uno de los 5 escenarios disponibles.

### Ejecutar los tests

Desde la carpeta raíz del proyecto:

```bash
python -m pytest src/tests/
```

Los 8 tests deben pasar en verde.

---

## Estructura del proyecto
src/
├── main.py                     # Script principal y menú interactivo
├── modelos.py                  # Clases: Pedido, GrafoUrbano, GestorPedidos
├── dp_selection.py             # Fase 2: Mochila 0/1 con Programación Dinámica
├── backtracking_ruta.py        # Fase 3: TSP con Backtracking y poda
├── mejoras/
│   ├── comparador_voraz.py     # Mejora Tema 2: Greedy ratio B/P
│   └── quicksort_personalizado.py  # Mejora Tema 3: Quicksort multicriterio
├── utils/
│   ├── generador_escenarios.py # Mejora Tema 1: Generador recursivo + grafos
│   └── visualizador.py         # (Reservado para trabajo futuro)
├── data/
│   ├── escenarios/             # 5 escenarios en formato JSON
│   └── resultados.txt          # Log de ejecuciones
└── tests/
├── datos_demo.py           # Datos fijos centralizados (fuente única)
├── test_dp.py              # 4 tests unitarios para la DP
└── test_backtracking.py    # 4 tests unitarios para el Backtracking

---

## Escenarios

| # | Nombre | N pedidos | Capacidad | Objetivo |
|---|--------|-----------|-----------|----------|
| 1 | Básico | 5 | 30 kg | Pipeline completo end-to-end |
| 2 | DP vs Voraz | 10 | 15 kg | Contraejemplo: DP supera al Voraz |
| 3 | Ruteo Complejo | 6 | 20 kg | Backtracking en grafo complejo |
| 4 | Poda | 6 | 15 kg | Demostrar reducción de nodos con poda |
| 5 | Libre | 5 | 20 kg | Caso equilibrado propuesto por el grupo |

---

## Algoritmos implementados

### Programación Dinámica — Mochila 0/1

Enfoque bottom-up con tabulación. Estado: `DP[i][w]` = beneficio máximo
con los `i` primeros pedidos y capacidad `w`.  
Complejidad: **O(n · C)** temporal y espacial.

### Backtracking TSP con Ramificación y Poda

Búsqueda en profundidad sobre el árbol de permutaciones de destinos.
Poda por cota: si la distancia parcial supera la mejor ruta conocida,
la rama se descarta.  
Preprocesado Dijkstra para garantizar el funcionamiento en grafos dispersos.  
Complejidad: **O(n!)** peor caso, reducida en la práctica por la poda.

### Mejoras

| Mejora | Tema | Complejidad |
|--------|------|-------------|
| Generador recursivo de escenarios | Tema 1 | O(n) |
| Comparador Voraz (ratio B/P) | Tema 2 | O(n log n) |
| Quicksort multicriterio | Tema 3 | O(n log n) promedio |

---

## Autores

Rayan Bentaleb Zaki: 48160981Q
Jorge Sáez Villate: 71972539L 
Óscar López Rojo: 03492385L 