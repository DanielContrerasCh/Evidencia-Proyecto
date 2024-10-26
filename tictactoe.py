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
    """Draw 'X' for player X at the given grid cell (x, y) coordinates."""
    turtle.color('red')
    turtle.width(5)
    turtle.up()
    turtle.goto(x - 133, y - 133)
    turtle.down()
    line(x + 10, y + 10, x + 125, y + 125)
    line(x + 10, y + 125, x + 125, y + 10)


def drawo(x, y):
    """Draw 'O' for player O at the given grid cell (x, y) coordinates."""
    turtle.color('blue')
    turtle.width(5)
    turtle.up()
    turtle.goto(x + 67, y + 5)
    turtle.down()
    turtle.circle(62)


def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200


# Dictionary to track the current player (0 for X, 1 for O)
state = {'player': 0}

# List of player drawing functions: drawx for player X, drawo for player O
players = [drawx, drawo]

# Initialize the board to keep track of occupied cells
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None],
]


def tap(x, y):
    """Draw X or O in tapped square if it is not already occupied."""
    # Calculate grid cell coordinates based on tap location
    x = floor(x)
    y = floor(y)

    # Determine the row and column index for the tapped cell
    row = int((y + 200) // 133)
    col = int((x + 200) // 133)

    # Check if the cell is already occupied
    if board[row][col] is not None:
        print("Cell is already taken!")
        return  # Exit the function if the cell is occupied

    # Mark the cell as occupied by the current player
    player = state['player']
    board[row][col] = player

    # Draw the player symbol in the tapped cell
    draw = players[player]
    draw(x, y)
    turtle.update()

    # Toggle to the next player (True becomes False, and vice versa)
    state['player'] = not player


# Set up the turtle window and grid
turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
grid()  # Draw the tic-tac-toe grid
turtle.update()

# Register the tap event to capture mouse clicks
turtle.onscreenclick(tap)

# Enter the main loop to start the game
turtle.done()
