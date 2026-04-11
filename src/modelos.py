#Archivo donde van a ir las clases

class Pedido:

    #Constructor de la clase
    def __init__(self, id_pedido, peso, beneficio):
        self.id = id_pedido
        self.peso = peso
        self.beneficio = beneficio
        self.ratio = beneficio / peso if peso > 0 else 0 #Si peso es 0 la division daria error asi que devolvemos 0
    
    #ToString
    def __repr__(self):
        return f"Pedido(id={self.id}, p={self.peso}, b={self.beneficio})"
    
class GrafoUrbano:
    def __init__(self):
        # Usaremos un diccionario de diccionarios.
        # Estructura: { 'Origen': { 'Destino1': distancia, 'Destino2': distancia } }
        self.nodos = {}

    def agregar_nodo(self, id_nodo):
        """Añade un punto de entrega o intersección a la ciudad."""
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = {}

    def agregar_arista(self, origen, destino, distancia):
        """Conecta dos puntos con una distancia (peso)."""
        # Nos aseguramos de que los nodos existan
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        
        # Como es una ciudad, asumimos calles de doble sentido (grafo no dirigido)
        self.nodos[origen][destino] = distancia
        self.nodos[destino][origen] = distancia

    def obtener_distancia(self, origen, destino):
        """Devuelve la distancia entre dos nodos, o infinito si no están conectados."""
        return self.nodos.get(origen, {}).get(destino, float('inf')) #float('inf') devuelve infinito si los nodos no estan conectados

    def obtener_vecinos(self, nodo):
        """Devuelve los nodos adyacentes a un nodo objetivo."""
        return self.nodos.get(nodo, {}) #Devuelve diccionario vacio si no encuentra el nodo

    def __repr__(self):
        return f"GrafoUrbano(nodos={len(self.nodos)})"
