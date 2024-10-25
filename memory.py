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

from random import *
from turtle import *

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
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


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
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    # Dibujar número de la ficha sobre el cuadro.
    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))

    # Actualizar cambios.
    update()
    ontimer(draw, 100)


# Configuración inicial del juego
shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
