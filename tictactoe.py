"""Tic Tac Toe

Exercises

1. Give the X and O a different color and width.
2. What happens when someone taps a taken spot?
3. How would you detect when someone has won?
4. How could you create a computer player?
"""

import turtle
from freegames import line


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Draw X player at the given grid cell with color red"""
    turtle.color('red')
    turtle.width(5)
    turtle.up()
    turtle.goto(x - 133, y - 133)
    turtle.down()
    line(x+10, y+10, x + 125, y + 125)
    line(x+10, y + 125, x + 125, y+10)



def drawo(x, y):
    """Draw O player at the given grid cell with color blue"""
    turtle.color('blue')
    turtle.width(5)
    turtle.up()
    turtle.goto(x + 67, y + 5)
    turtle.down()
    turtle.circle(62)


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


state = {'player': 0}
players = [drawx, drawo]


def tap(x, y):
    """Draw X or O in tapped square."""
    x = floor(x)
    y = floor(y)
    player = state['player']
    draw = players[player]
    draw(x, y)
    turtle.update()
    state['player'] = not player


turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
grid()
turtle.update()
turtle.onscreenclick(tap)
turtle.done()
