"""Juego de memoria con fichas numéricas en pares.

El objetivo es descubrir pares de fichas que contengan el mismo número.
El tablero está compuesto por 64 fichas inicialmente ocultas.

Ejercicios sugeridos:
1. Contar y mostrar cuántos intentos realiza el jugador.
2. Reducir el número de fichas a una cuadrícula de 4x4.
3. Detectar cuándo todas las fichas han sido descubiertas.
4. Centrar los números de una sola cifra en las fichas.
5. Usar letras en lugar de números en las fichas.
"""

import random
import turtle
from freegames import path

# Cargar imagen para las fichas
car = path('car.gif')

# Crear una lista de números en pares
tiles = list(range(32)) * 2

# Variable que almacena la ficha actualmente seleccionada
state = {'mark': None}

# Lista que indica si las fichas están ocultas o reveladas
hide = [True] * 64


def square(x, y):
    """Dibujar cuadro de las fichas ocultas de la imagen."""
    turtle.up()
    turtle.goto(x, y)
    turtle.down()
    turtle.color('black', 'white')
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(50)
        turtle.left(90)
    turtle.end_fill()


def index(x, y):
    """Identificar la ficha seleccionada por el jugador."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convertir el índice de ficha en coordenadas (x, y)."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Mostrar y esconder fichas según las selecciones del jugador."""
    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    """Dibujar el tablero de juego y mostrar las fichas descubiertas."""
    turtle.clear()
    turtle.goto(0, 0)
    turtle.shape(car)
    turtle.stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    # Dibujar número de la ficha sobre el cuadro.
    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        turtle.up()
        turtle.goto(x + 2, y)
        turtle.color('black')
        turtle.write(tiles[mark], font=('Arial', 30, 'normal'))

    # Actualizar cambios.
    turtle.update()
    turtle.ontimer(draw, 100)


# Configuración inicial del juego
random.shuffle(tiles)
turtle.setup(420, 420, 370, 0)
turtle.addshape(car)
turtle.hideturtle()
turtle.tracer(False)
turtle.onscreenclick(tap)
draw()
turtle.done()
