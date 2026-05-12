import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backtracking_ruta import calcular_ruta_tsp
from modelos import GrafoUrbano


def grafo_completo_3():
    #Genera un grafo triangular: A-B=1, B-C=1, A-C=2
    g = GrafoUrbano()
    g.agregar_arista('A', 'B', 1)
    g.agregar_arista('B', 'C', 1)
    g.agregar_arista('A', 'C', 2)
    return g


class TestCalcularRutaTSP(unittest.TestCase):

    def test_ruta_simple(self):
        #Verifica que se encuentre una ruta válida que empiece y termine en el origen.
        g = grafo_completo_3()
        ruta, distancia, _ = calcular_ruta_tsp(g, 'A', ['B', 'C'])
        self.assertIsNotNone(ruta)
        self.assertEqual(ruta[0], 'A')
        self.assertEqual(ruta[-1], 'A')
        self.assertIn('B', ruta)
        self.assertIn('C', ruta)
        self.assertLess(distancia, float('inf'))

    def test_sin_ruta_posible(self):
        #Comprueba el comportamiento del sistema cuando un nodo de destino es inalcanzable.
        g = GrafoUrbano()
        g.agregar_arista('A', 'B', 1)
        # El nodo C está aislado, no existen aristas que lleguen a él
        g.agregar_nodo('C')
        ruta, distancia, _ = calcular_ruta_tsp(g, 'A', ['B', 'C'])
        self.assertIsNone(ruta)
        self.assertEqual(distancia, float('inf'))

    def test_poda_reduce_nodos(self):
        #Validación de eficiencia: Comprueba que la versión con Poda por Cota
        #explora menos nodos que el Backtracking puro sin afectar al resultado.
        # Grafo en anillo A-B-C-D-E-A
        g = GrafoUrbano()
        g.agregar_arista('A', 'B', 1)
        g.agregar_arista('B', 'C', 1)
        g.agregar_arista('C', 'D', 1)
        g.agregar_arista('D', 'E', 1)
        g.agregar_arista('E', 'A', 1)

        _, _, explorados_con_poda = calcular_ruta_tsp(g, 'A', ['B', 'C', 'D', 'E'], usar_poda=True)
        _, _, explorados_sin_poda = calcular_ruta_tsp(g, 'A', ['B', 'C', 'D', 'E'], usar_poda=False)
        
        # El número de llamadas recursivas debe ser menor gracias a la poda
        self.assertLess(explorados_con_poda, explorados_sin_poda)

    def test_grafo_disperso(self):
        #Prueba de conectividad indirecta: Verifica que el algoritmo pueda encontrar
        #rutas a través de nodos intermedios (usando Dijkstra internamente).
        g = GrafoUrbano()
        # Estructura: A -> X -> B -> Y -> C (sin conexión directa B-C)
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
