import sys
import os
import copy

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from modelos import Pedido

ESCENARIOS = {
    "1": {
        "n": 5, "capacidad": 30,
        "pedidos": [
            Pedido('P1', 'Nodo_1', 15, 84),
            Pedido('P2', 'Nodo_2',  9, 73),
            Pedido('P3', 'Nodo_3',  5, 72),
            Pedido('P4', 'Nodo_4',  4, 59),
            Pedido('P5', 'Nodo_5', 15, 61),
        ]
    },
    "2": {
        "n": 10, "capacidad": 15,
        "pedidos": [
            Pedido('P1',  'Nodo_1',  1,  6),
            Pedido('P2',  'Nodo_2',  2, 10),
            Pedido('P3',  'Nodo_3',  3, 12),
            Pedido('P4',  'Nodo_4',  5, 17),
            Pedido('P5',  'Nodo_5',  2,  8),
            Pedido('P6',  'Nodo_6',  4, 14),
            Pedido('P7',  'Nodo_7',  3, 11),
            Pedido('P8',  'Nodo_8',  6, 19),
            Pedido('P9',  'Nodo_9',  2,  9),
            Pedido('P10', 'Nodo_10', 4, 13),
        ]
    },
    "3": {
        "n": 6, "capacidad": 20,
        "pedidos": [
            Pedido('P1', 'Nodo_1', 4, 20),
            Pedido('P2', 'Nodo_2', 3, 15),
            Pedido('P3', 'Nodo_3', 2, 12),
            Pedido('P4', 'Nodo_4', 5, 18),
            Pedido('P5', 'Nodo_5', 3, 14),
            Pedido('P6', 'Nodo_6', 4, 16),
        ]
    },
    "4": {
        "n": 6, "capacidad": 15,
        "pedidos": [
            Pedido('P1', 'Nodo_1', 1,  6),
            Pedido('P2', 'Nodo_2', 2, 10),
            Pedido('P3', 'Nodo_3', 3, 12),
            Pedido('P4', 'Nodo_4', 2,  8),
            Pedido('P5', 'Nodo_5', 4, 14),
            Pedido('P6', 'Nodo_6', 3,  9),
        ]
    },
    "5": {
        "n": 5, "capacidad": 20,
        "pedidos": [
            Pedido('P1', 'Nodo_1', 2, 10),
            Pedido('P2', 'Nodo_2', 3, 14),
            Pedido('P3', 'Nodo_3', 4, 16),
            Pedido('P4', 'Nodo_4', 1,  7),
            Pedido('P5', 'Nodo_5', 5, 18),
        ]
    },
}


def get_escenario(opcion):
    """Devuelve una copia fresca del escenario para evitar
    que el quicksort in-place modifique los datos originales."""
    return copy.deepcopy(ESCENARIOS[opcion])
