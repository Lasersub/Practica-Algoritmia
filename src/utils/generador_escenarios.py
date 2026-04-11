import random
from src.modelos import Pedido
def generador_recursivo_escenarios(n, id_actual):
    #El caso base, cuando no quedan mas pedidos por generar
    if n==0:
        return []
    #El caso general, creamos un pedido con un peso y beneficio aleatorio. 
    pedido_nuevo = Pedido (id_actual, random.randint(4,10), random.randint(20,70))
    #La relacion de recurrencia, cuando tenemos pedidos los vamos incluyendo todos de 
    #forma consecutiva concatenandolos y pasandolos a diccionario para poder usarlo mejor en los archivos de escenario.
    return [pedido_nuevo.to_dict()] + generador_recursivo_escenarios(n-1, id_actual+1)