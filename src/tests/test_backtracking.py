import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backtracking_ruta import calcular_ruta_tsp
from modelos import GrafoUrbano


def grafo_completo_3():
    """Triangle: A-B=1, B-C=1, A-C=2"""
    g = GrafoUrbano()
    g.agregar_arista('A', 'B', 1)
    g.agregar_arista('B', 'C', 1)
    g.agregar_arista('A', 'C', 2)
    return g


class TestCalcularRutaTSP(unittest.TestCase):

    def test_ruta_simple(self):
        g = grafo_completo_3()
        ruta, distancia, _ = calcular_ruta_tsp(g, 'A', ['B', 'C'])
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta[0], 'A')
        self.assertEqual(ruta[-1], 'A')
        self.assertIn('B', ruta)
        self.assertIn('C', ruta)
        self.assertLess(distancia, float('inf'))

    def test_sin_ruta_posible(self):
        g = GrafoUrbano()
        g.agregar_arista('A', 'B', 1)
        # C is isolated — no edges
        g.agregar_nodo('C')
        ruta, distancia, _ = calcular_ruta_tsp(g, 'A', ['B', 'C'])
        self.assertIsNone(ruta)
        self.assertEqual(distancia, float('inf'))

    def test_poda_reduce_nodos(self):
        # Ring graph A-B-C-D-E-A (all weight 1), no cross-edges.
        # Optimal tour = 5 (ring order). Off-ring permutations pay dist=2 for
        # any "jump", so their partial sums hit the pruning threshold before the
        # leaf, guaranteeing at least one pruned call regardless of set order.
        g = GrafoUrbano()
        g.agregar_arista('A', 'B', 1)
        g.agregar_arista('B', 'C', 1)
        g.agregar_arista('C', 'D', 1)
        g.agregar_arista('D', 'E', 1)
        g.agregar_arista('E', 'A', 1)

        _, _, explorados_con_poda = calcular_ruta_tsp(g, 'A', ['B', 'C', 'D', 'E'], usar_poda=True)
        _, _, explorados_sin_poda = calcular_ruta_tsp(g, 'A', ['B', 'C', 'D', 'E'], usar_poda=False)
        self.assertLess(explorados_con_poda, explorados_sin_poda)

    def test_grafo_disperso(self):
        """Destinations B and C are not directly connected — requires Dijkstra via intermediate node."""
        g = GrafoUrbano()
        # A -> X -> B -> Y -> C, no direct B-C edge
        g.agregar_arista('A', 'X', 1)
        g.agregar_arista('X', 'B', 1)
        g.agregar_arista('B', 'Y', 1)
        g.agregar_arista('Y', 'C', 1)
        g.agregar_arista('C', 'A', 1)

        ruta, distancia, _ = calcular_ruta_tsp(g, 'A', ['B', 'C'])
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta[0], 'A')
        self.assertEqual(ruta[-1], 'A')
        self.assertIn('B', ruta)
        self.assertIn('C', ruta)
        self.assertLess(distancia, float('inf'))


if __name__ == '__main__':
    unittest.main()
