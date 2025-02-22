class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

# Crear nodos del árbol
raiz = Nodo("A")
raiz.izquierda = Nodo("B")
raiz.derecha = Nodo("C")
raiz.izquierda.izquierda = Nodo("D")
raiz.izquierda.derecha = Nodo("E")
raiz.derecha.izquierda = Nodo("F")
raiz.derecha.derecha = Nodo("G")

# Recorridos básicos del árbol
def preorden(nodo):
    if nodo:
        print(nodo.valor, end=" ")  # 1° Raíz
        preorden(nodo.izquierda)   # 2° Izquierda
        preorden(nodo.derecha)     # 3° Derecha

def inorden(nodo):
    if nodo:
        inorden(nodo.izquierda)   # 1° Izquierda
        print(nodo.valor, end=" ")  # 2° Raíz
        inorden(nodo.derecha)     # 3° Derecha

def posorden(nodo):
    if nodo:
        posorden(nodo.izquierda)   # 1° Izquierda
        posorden(nodo.derecha)     # 2° Derecha
        print(nodo.valor, end=" ")  # 3° Raíz

# Imprimir recorridos
print("Recorrido en preorden:")
preorden(raiz)
print("\nRecorrido en inorden:")
inorden(raiz)
print("\nRecorrido en posorden:")
posorden(raiz)
