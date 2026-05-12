import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dp_selection import seleccionar_pedidos_dp
from modelos import Pedido


class TestSeleccionarPedidosDP(unittest.TestCase):

    def test_seleccion_basica(self):
        #Prueba una selección estándar donde solo caben algunos elementos.
        pedidos = [
            Pedido('P1', peso=2, beneficio=3),
            Pedido('P2', peso=3, beneficio=4),
            Pedido('P3', peso=4, beneficio=5),
        ]
        seleccionados, beneficio, _ = seleccionar_pedidos_dp(pedidos, capacidad_maxima=5)
        self.assertEqual(beneficio, 7)
        ids = {p.id for p in seleccionados}
        self.assertEqual(ids, {'P1', 'P2'})

    def test_capacidad_cero(self):
        #Verifica que el sistema no seleccione nada si la capacidad es nula.
        pedidos = [
            Pedido('P1', peso=2, beneficio=10),
            Pedido('P2', peso=1, beneficio=5),
        ]
        seleccionados, beneficio, peso = seleccionar_pedidos_dp(pedidos, capacidad_maxima=0)
        self.assertEqual(seleccionados, [])
        self.assertEqual(beneficio, 0)
        self.assertEqual(peso, 0)

    def test_todos_caben(self):
        #Caso donde la capacidad sobra y se seleccionan todos los pedidos.
        pedidos = [
            Pedido('P1', peso=1, beneficio=10),
            Pedido('P2', peso=2, beneficio=20),
            Pedido('P3', peso=3, beneficio=30),
        ]
        seleccionados, beneficio, peso = seleccionar_pedidos_dp(pedidos, capacidad_maxima=10)
        self.assertEqual(len(seleccionados), 3)
        self.assertEqual(beneficio, 60)
        self.assertEqual(peso, 6)

    def test_beneficio_optimo_vs_voraz(self):
        #Caso crítico: Se comprueba que la Programación Dinámica encuentra
        #la solución óptima global, superando la solución local del algoritmo voraz.ins.
        pedidos = [
            Pedido('P1', peso=1, beneficio=6),
            Pedido('P2', peso=2, beneficio=10),
            Pedido('P3', peso=3, beneficio=12),
        ]
        seleccionados, beneficio, _ = seleccionar_pedidos_dp(pedidos, capacidad_maxima=4)
        # Lógica de simulación voraz para comparar
        greedy_sorted = sorted(pedidos, key=lambda p: p.ratio, reverse=True)
        cap = 4
        greedy_sel = []
        for p in greedy_sorted:
            if p.peso <= cap:
                greedy_sel.append(p)
                cap -= p.peso
        greedy_benefit = sum(p.beneficio for p in greedy_sel)

        self.assertGreater(beneficio, greedy_benefit)
        self.assertEqual(beneficio, 18)


if __name__ == '__main__':
    unittest.main()
