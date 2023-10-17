import tkinter as tk  # Importa la biblioteca Tkinter y la renombra como 'tk'.
import random  # Importa la biblioteca 'random' para generar números aleatorios.
from src.tda_cola_lineal import Cola_Lineal  # Importa una clase personalizada llamada 'Cola_Lineal' desde un módulo 'src'.

# Configuración
ANCHO, ALTO = 400, 400  # Establece las dimensiones de la ventana del juego.
TAMANO_SEGMENTO = 20  # Define el tamaño de cada segmento de la serpiente y la comida.
VELOCIDAD = 200  # Establece la velocidad de movimiento de la serpiente (en milisegundos).

# Clase SnakeGame
class SnakeGame:
    def __init__(self):
        self.ventana = tk.Tk()  # Crea una ventana de Tkinter.
        self.ventana.title("Snake Game")  # Establece el título de la ventana.
        self.canvas = tk.Canvas(self.ventana, width=ANCHO, height=ALTO)  # Crea un lienzo (canvas) en la ventana con dimensiones definidas.
        self.canvas.pack()  # Empaqueta el lienzo en la ventana.
        self.ventana.bind("<Key>", self.cambiar_direccion)  # Vincula el evento de presionar una tecla a la función 'cambiar_direccion'.

        self.snake = [(ANCHO // 2, ALTO // 2)]  # Inicializa la serpiente con una posición en el centro de la ventana.
        self.comida = self.generar_comida()  # Genera una posición inicial para la comida.
        self.direccion = "Right"  # Inicializa la dirección de la serpiente como "Derecha".
        self.puntuacion = 0  # Inicializa la puntuación en 0.
        self.cola = Cola_Lineal()  # Crea una cola lineal para seguir el rastro de la serpiente.
        self.mover()  # Llama al método 'mover' para iniciar el juego.

    def generar_comida(self):
        # Genera una posición aleatoria para la comida dentro de la ventana del juego.
        x = random.randint(0, (ANCHO - TAMANO_SEGMENTO) // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
        y = random.randint(0, (ALTO - TAMANO_SEGMENTO) // TAMANO_SEGMENTO) * TAMANO_SEGMENTO
        return (x, y)

    def cambiar_direccion(self, event):
        key = event.keysym  # Obtiene la tecla presionada.
        # Cambia la dirección de la serpiente si la tecla es válida y evita invertir la dirección.
        if (key == "Up" and self.direccion != "Down") or \
           (key == "Down" and self.direccion != "Up") or \
           (key == "Left" and self.direccion != "Right") or \
           (key == "Right" and self.direccion != "Left"):
            self.direccion = key

    def mover(self):
        x, y = self.calcular_nueva_cabeza()  # Calcula la nueva posición de la cabeza de la serpiente.

        # Comprueba colisiones con bordes de la ventana o con la propia serpiente.
        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO or self.detectar_colision():
            self.ventana.destroy()  # Cierra la ventana del juego.
            return

        self.snake.insert(0, (x, y))  # Agrega la nueva cabeza a la serpiente.
        self.cola.insertar((x, y))  # Agrega la nueva cabeza a la cola.

        if x == self.comida[0] and y == self.comida[1]:
            self.puntuacion += 1  # Incrementa la puntuación si la serpiente come la comida.
            self.comida = self.generar_comida()  # Genera una nueva posición para la comida.
        else:
            self.snake.pop()  # Elimina el último segmento de la serpiente.
            self.cola.quitar()  # Elimina el último elemento de la cola.

        self.dibujar()  # Actualiza la representación visual del juego en el lienzo.
        self.ventana.after(VELOCIDAD, self.mover)  # Llama a 'mover' nuevamente después de un tiempo.

    def calcular_nueva_cabeza(self):
        x, y = self.snake[0]  # Obtiene la posición actual de la cabeza de la serpiente.
        if self.direccion == "Up":
            return x, y - TAMANO_SEGMENTO
        elif self.direccion == "Down":
            return x, y + TAMANO_SEGMENTO
        elif self.direccion == "Left":
            return x - TAMANO_SEGMENTO, y
        elif self.direccion == "Right":
            return x + TAMANO_SEGMENTO, y

    def detectar_colision(self):
        cabeza = self.snake[0]  # Obtiene la posición de la cabeza de la serpiente.

        for segmento in self.snake[1:]:
            if segmento == cabeza:
                return True  # Si la cabeza colisiona con algún segmento de la serpiente, devuelve True.
        return False  # Si no hay colisión, devuelve False.

    def dibujar(self):
        self.canvas.delete("all")  # Borra todo el contenido en el lienzo.

        for segmento in self.snake:
            x, y = segmento
            # Dibuja cada segmento de la serpiente.
            self.canvas.create_rectangle(x, y, x + TAMANO_SEGMENTO, y + TAMANO_SEGMENTO, fill="green")

        x, y = self.comida
        # Dibuja la comida como un óvalo rojo.
        self.canvas.create_oval(x, y, x + TAMANO_SEGMENTO, y + TAMANO_SEGMENTO, fill="red")

        self.canvas.create_text(50, 1, text=f"Puntuación: {self.puntuacion}", anchor="nw")
        # Muestra la puntuación en la esquina superior izquierda del lienzo.

if __name__ == "__main__":
    juego = SnakeGame()  # Crea una instancia de la clase SnakeGame.
    juego.ventana.mainloop()  # Inicia el bucle principal del juego, mostrando la ventana del juego.
