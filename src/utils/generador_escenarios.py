import random
from src.modelos import Pedido
def generador_recursivo_escenarios(n, id_actual):
    #El caso base, cuando no quedan mas pedidos por generar
    if n==0:
        return []
    pedido_nuevo = Pedido (1, random.randint(4,10), random.randint(20,70))
    return [pedido_nuevo.to_dict()] + generador_recursivo_escenarios(n-1, id_actual+1)