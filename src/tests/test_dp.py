import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dp_selection import seleccionar_pedidos_dp
from modelos import Pedido


class TestSeleccionarPedidosDP(unittest.TestCase):

    def test_seleccion_basica(self):
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
        pedidos = [
            Pedido('P1', peso=2, beneficio=10),
            Pedido('P2', peso=1, beneficio=5),
        ]
        seleccionados, beneficio, peso = seleccionar_pedidos_dp(pedidos, capacidad_maxima=0)
        self.assertEqual(seleccionados, [])
        self.assertEqual(beneficio, 0)
        self.assertEqual(peso, 0)

    def test_todos_caben(self):
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
        # Greedy by ratio picks P1 (ratio=3) then P2 (ratio=2) → total peso=3+2=5, beneficio=9+6=15
        # but P2+P3 gives beneficio=6+10=16 with peso=2+4=6 — wait, let's use a classic case:
        # P1: peso=1, beneficio=6  ratio=6
        # P2: peso=2, beneficio=10 ratio=5
        # P3: peso=3, beneficio=12 ratio=4  capacity=4
        # Greedy: P1(6)+P2(10)=16, peso=3. Fits P3? 1+2+3=6>4, no. So greedy=16.
        # DP: P2+P3=22, peso=5>4, no. P1+P3=18, peso=4. DP=18. DP wins.
        pedidos = [
            Pedido('P1', peso=1, beneficio=6),
            Pedido('P2', peso=2, beneficio=10),
            Pedido('P3', peso=3, beneficio=12),
        ]
        seleccionados, beneficio, _ = seleccionar_pedidos_dp(pedidos, capacidad_maxima=4)

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
