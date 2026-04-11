#Archivo donde van a ir las clases

class Pedido:

    #Constructor de la clase
    def __init__(self, id_pedido, peso, beneficio):
        self.id = id_pedido
        self.peso = peso
        self.beneficio = beneficio
        self.ratio = beneficio / peso if peso > 0 else 0
    
    def __repr__(self):
        return f"Pedido(id={self.id}, p={self.peso}, b={self.beneficio})"
    


