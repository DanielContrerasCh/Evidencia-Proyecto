"""
Implementación del clásico juego Pacman usando la biblioteca turtle.

El juego consiste en un laberinto donde Pacman (círculo amarillo) debe comer
los puntos blancos mientras evita a los fantasmas (círculos rojos). Los
fantasmas se mueven de manera aleatoria por el laberinto.

Ejercicios sugeridos:
1. Modificar el tablero
2. Cambiar el número de fantasmas
3. Cambiar la posición inicial de Pacman
4. Ajustar la velocidad de los fantasmas
5. Mejorar la inteligencia de los fantasmas
"""

from random import choice
from turtle import (
    Turtle, bgcolor, clear, done, goto, hideturtle,
    listen, onkey, ontimer, setup, tracer, up, update, dot
)
from freegames import floor, vector

# Puntaje inicializado en 0
state = {'score': 0}

# Crear tortugas invisibles para dibujar y escribir
path = Turtle(visible=False)
writer = Turtle(visible=False)

# Dirección inicial de Pacman
aim = vector(5, 0)

# Posicin inicial de Pacman
pacman = vector(0, 0)

# Matriz con dirección y posición inicial de fantasmas
ghosts = [
    [vector(-180, 160), vector(10, 0)],
    [vector(-180, -160), vector(0, 10)],
    [vector(100, 160), vector(0, -10)],
    [vector(100, -160), vector(-10, 0)],
]

# Matriz que define el tablero de juego
# 0: representa paredes
# 1: representa pasillos con puntos
# 2: representa pasillos sin puntos (puntos ya comidos)
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0,
    0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Dibuja un cuadrado en la posicion especificada.

    Args:
        x (int): Coordenada x del cuadrado
        y (int): Coordenada y del cuadrado
    """
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    # Dibuja un cuadrado repitiendo movimientos hacia adelante y giros
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """
    Calcula el índice en la matriz tiles para un punto dado.
    Args:
        point (vector): Punto para calcular su posición en la matriz
    Returns:
        int: índice correspondiente en la matriz tiles
    """
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """
    Verifica si un punto es una posición válida en el tablero.
    Args:
        point (vector): Punto a verificar
    Returns:
        bool: True si el punto es válido, False en caso contrario
    """
    index = offset(point)

    if tiles[index] == 0:  # Verifica si hay pared
        return False

    index = offset(point + 19)  # Verifica el otro extremo del personaje

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibuja el mundo del juego: paredes, pasillos y puntos."""
    bgcolor('black')
    path.color('blue')

    # Recorre la matriz del tablero y dibuja cada elemento
    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:  # Si no es pared
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:  # Si hay punto para comer
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Maneja el movimiento de Pacman y los fantasmas."""
    # Actualiza el puntaje
    writer.undo()
    writer.write(state['score'])

    clear()

    # Mueve a Pacman si la siguiente posicion es válida
    if valid(pacman + aim):
        pacman.move(aim)

    # Verifica si Pacman come un punto
    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2  # Marca el punto como comido
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    # Dibuja a Pacman
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # Si el fantasma no puede seguir en su direccián actual,
            # elige una nueva direccián aleatoria
            options = [
                vector(10, 0),    # Derecha
                vector(-10, 0),   # Izquierda
                vector(0, 10),    # Arriba
                vector(0, -10),   # Abajo
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    # Verifica si Pacman choca con algun fantasma
    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return  # Termina el juego

    # Programa el siguiente movimiento
    ontimer(move, 100)


def change(x, y):
    """Cambia la dirección de Pacman si el movimiento es válido.

    Args:
        x (int): Componente x del vector dirección
        y (int): Componente y del vector dirección
    """
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Configuración inicial del juego
setup(420, 420, 370, 0)  # Dimensiones de la ventana
hideturtle()
tracer(False)  # Desactiva la animación para mejorar el rendimiento
writer.goto(180, 160)  # Posición del marcador de puntaje
writer.color('white')
writer.write(state['score'])

# Configuración de controles
listen()
onkey(lambda: change(5, 0), 'Right')     # Flecha derecha
onkey(lambda: change(-5, 0), 'Left')     # Flecha izquierda
onkey(lambda: change(0, 5), 'Up')        # Flecha arriba
onkey(lambda: change(0, -5), 'Down')     # Flecha abajo

# Inicia el juego
world()
move()
done()
