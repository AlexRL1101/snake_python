class nodo_Cola(object):
    dato = None
    siguiente = None


class Cola_Lineal(object):

    def __iter__(self):
        self.actual = self.primero
        return self

    def __next__(self):
        if self.actual is not None:
            dato = self.actual.dato
            self.actual = self.actual.siguiente
            return dato
        else:
            raise StopIteration

    def __init__(self):
        self.primero = None
        self.ultimo = None

    def cola_vacia(self):
        return self.primero == None

    def reiniciar(self):
        self.primero = None
        self.ultimo = None

    def insertar(self, dato):
        nodo = nodo_Cola()
        nodo.dato = dato
        if self.cola_vacia():
            self.primero = nodo
            self.ultimo = nodo
        else:
            self.ultimo.siguiente = nodo
            self.ultimo = nodo

    def primer_dato(self):
        return self.primero.dato

    def quitar(self):
        dato = self.primero.dato
        nodo_eliminar = self.primero
        self.primero = self.primero.siguiente
        nodo_eliminar.siguiente = None
        if self.primero == None:
            self.ultimo = None
        return dato

    def imprimir(self):
        caux = Cola_Lineal()
        cadena = ""
        while not self.cola_vacia():
            dato = self.quitar()
            cadena += str(dato) + "\n"
            caux.insertar(dato)

        while not caux.cola_vacia():
            dato = caux.quitar()
            self.insertar(dato)
        return cadena
