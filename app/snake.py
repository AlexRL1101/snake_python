import tkinter as tk
import random
from src.tda_cola_lineal import Cola_Lineal

# Configuración
ANCHO, ALTO = 400, 400
TAMANO_SEGMENTO = 20
VELOCIDAD = 200


class SnakeGame:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Snake Game")
        self.canvas = tk.Canvas(self.ventana, width=ANCHO, height=ALTO)
        self.canvas.pack()
        self.ventana.bind("<Key>", self.cambiar_direccion)

        self.snake = [(ANCHO // 2, ALTO // 2)]
        self.comida = self.generar_comida()
        self.direccion = "Right"
        self.puntuacion = 0
        self.cola = Cola_Lineal()
        self.mover()

    def generar_comida(self):
        x = random.randint(0, (ANCHO - TAMANO_SEGMENTO) //
                           TAMANO_SEGMENTO) * TAMANO_SEGMENTO
        y = random.randint(0, (ALTO - TAMANO_SEGMENTO) //
                           TAMANO_SEGMENTO) * TAMANO_SEGMENTO
        return (x, y)

    def cambiar_direccion(self, event):
        key = event.keysym
        if (key == "Up" and self.direccion != "Down") or \
           (key == "Down" and self.direccion != "Up") or \
           (key == "Left" and self.direccion != "Right") or \
           (key == "Right" and self.direccion != "Left"):
            self.direccion = key

    def mover(self):
        x, y = self.calcular_nueva_cabeza()

        if x < 0 or x >= ANCHO or y < 0 or y >= ALTO or self.detectar_colision():
            self.ventana.destroy()
            return

        self.snake.insert(0, (x, y))
        self.cola.insertar((x, y))

        if x == self.comida[0] and y == self.comida[1]:
            self.puntuacion += 1
            self.comida = self.generar_comida()
        else:
            self.snake.pop()
            self.cola.quitar()

        self.dibujar()
        self.ventana.after(VELOCIDAD, self.mover)

    def calcular_nueva_cabeza(self):
        x, y = self.snake[0]
        if self.direccion == "Up":
            return x, y - TAMANO_SEGMENTO
        elif self.direccion == "Down":
            return x, y + TAMANO_SEGMENTO
        elif self.direccion == "Left":
            return x - TAMANO_SEGMENTO, y
        elif self.direccion == "Right":
            return x + TAMANO_SEGMENTO, y

    def detectar_colision(self):
        cabeza = self.snake[0]

        for segmento in self.snake[1:]:
            if segmento == cabeza:
                return True
        return False

    def dibujar(self):
        self.canvas.delete("all")

        for segmento in self.snake:
            x, y = segmento
            self.canvas.create_rectangle(
                x, y, x + TAMANO_SEGMENTO, y + TAMANO_SEGMENTO, fill="green")

        x, y = self.comida
        self.canvas.create_oval(x, y, x + TAMANO_SEGMENTO,
                                y + TAMANO_SEGMENTO, fill="red")

        self.canvas.create_text(
            50, 1, text=f"Puntuación: {self.puntuacion}", anchor="nw")


if __name__ == "__main__":
    juego = SnakeGame()
    juego.ventana.mainloop()
