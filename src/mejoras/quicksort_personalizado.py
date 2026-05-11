
def es_prioritario(pedido_a, pedido_b, criterio="beneficio"):
    """
    Define qué pedido va antes basado en los atributos REALES de la clase Pedido.
    """
    if criterio == "beneficio":
        # 1. Mayor beneficio
        if pedido_a.beneficio != pedido_b.beneficio:
            return pedido_a.beneficio > pedido_b.beneficio
        # 2. Desempate: Menor peso
        if pedido_a.peso != pedido_b.peso:
            return pedido_a.peso < pedido_b.peso
        # 3. Desempate final: Mayor ratio
        return pedido_a.ratio > pedido_b.ratio

    elif criterio == "peso":
        # 1. Menor peso
        if pedido_a.peso != pedido_b.peso:
            return pedido_a.peso < pedido_b.peso
        # 2. Desempate: Mayor beneficio
        return pedido_a.beneficio > pedido_b.beneficio

    elif criterio == "ratio":
        # 1. Mayor ratio (rentabilidad)
        if pedido_a.ratio != pedido_b.ratio:
            return pedido_a.ratio > pedido_b.ratio
        # 2. Desempate: Mayor beneficio absoluto
        return pedido_a.beneficio > pedido_b.beneficio


def particion(pedidos, inicio, fin, criterio):
    pivote = pedidos[fin] 
    i = inicio - 1
    for j in range(inicio, fin):
        # Le pasamos el criterio al comparador
        if es_prioritario(pedidos[j], pivote, criterio):
            i += 1
            pedidos[i], pedidos[j] = pedidos[j], pedidos[i]
    pedidos[i + 1], pedidos[fin] = pedidos[fin], pedidos[i + 1]
    return i + 1


def quicksort_multicriterio(pedidos, inicio=0, fin=None, criterio="beneficio"):
    if fin is None:
        fin = len(pedidos) - 1
        
    if inicio < fin:
        # Pasamos el criterio a la partición
        indice_pivote = particion(pedidos, inicio, fin, criterio)
        quicksort_multicriterio(pedidos, inicio, indice_pivote - 1, criterio)
        quicksort_multicriterio(pedidos, indice_pivote + 1, fin, criterio)

    return pedidos