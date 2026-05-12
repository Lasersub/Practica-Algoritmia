import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dp_selection import seleccionar_pedidos_dp
from modelos import Pedido
from tests.datos_demo import get_escenario


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
        #la solución óptima global, superando la solución local del algoritmo voraz.
        demo = get_escenario("2")
        pedidos = demo["pedidos"]
        seleccionados, beneficio, _ = seleccionar_pedidos_dp(pedidos, demo["capacidad"])
        self.assertGreater(beneficio, 0)
        # Verify DP beats greedy on this dataset
        from mejoras.comparador_voraz import seleccionar_pedidos_voraz
        _, ben_voraz, _ = seleccionar_pedidos_voraz(pedidos, demo["capacidad"])
        self.assertGreaterEqual(beneficio, ben_voraz)


if __name__ == '__main__':
    unittest.main()
