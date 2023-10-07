# A program that returns an rgb when 
# given the name, for red, cyan, white, black, yello, greeen, blue, magenta, orange, purple, pink, grey, brown, and lime

# Standard RGB colors
RED = (255, 0, 0)
CYAN = (0, 100, 100)    
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
GREY = (128, 128, 128)
BROWN = (165, 42, 42)
LIME = (0, 255, 0)

def get_rgb(color):
    if color == "red":
        return RED
    elif color == "cyan":
        return CYAN
    elif color == "white":
        return WHITE
    elif color == "black":
        return BLACK
    elif color == "yellow":
        return YELLOW
    elif color == "green":
        return GREEN
    elif color == "blue":
        return BLUE
    elif color == "magenta":
        return MAGENTA
    elif color == "orange":
        return ORANGE
    elif color == "purple":
        return PURPLE
    elif color == "pink":
        return PINK
    elif color == "grey":
        return GREY
    elif color == "brown":
        return BROWN
    elif color == "lime":
        return LIME
    else:
        return BLACK