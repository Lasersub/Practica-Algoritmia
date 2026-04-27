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

class GestorPedidos:
    def __init__(self):
        self.catalogo = [] # Inicializa la lista vacía

    def agregar_pedido(self, pedido):
        self.catalogo.append(pedido)

    def mostrar_pedidos(self):
        """Devuelve la representación de todos los pedidos."""
        return self.catalogo 

class GrafoUrbano:
    def __init__(self):
        # Estructura: { 'Origen': [('Destino1', distancia), ('Destino2', distancia)] }
        self.nodos = {}

    def agregar_nodo(self, id_nodo):
        if id_nodo not in self.nodos:
            self.nodos[id_nodo] = [] # Ahora inicializamos con una lista vacía

    def agregar_arista(self, origen, destino, distancia):
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        
        # Añadimos la tupla (destino, distancia) a la lista del origen
        # Y viceversa, al ser un grafo no dirigido
        self.nodos[origen].append((destino, distancia))
        self.nodos[destino].append((origen, distancia))

    def obtener_distancia(self, origen, destino):
        """Busca en la lista de tuplas del origen el destino indicado."""
        vecinos = self.nodos.get(origen, [])
        for v_id, dist in vecinos:
            if v_id == destino:
                return dist
        return float('inf')

    def obtener_vecinos(self, nodo):
        """Devuelve la lista de tuplas directamente."""
        return self.nodos.get(nodo, [])

    def __repr__(self):
        return f"GrafoUrbano(nodos={len(self.nodos)})"
