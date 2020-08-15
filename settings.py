

# screen settings
WIDTH, HEIGHT = 800, 600
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER, HEIGHT-TOP_BOTTOM_BUFFER


# colour settings
BLACK = (0, 0, 0)
BLUE = (0, 0, 163)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
GOLD = (124, 123, 7)
GREEN = (33, 208, 33)
YELLOW = (188, 188, 12)
ORANGE = (208, 137, 50)
PLAYER_COLOUR = (190, 194, 15)

# font settings
MENU_TEXT_SIZE = 64
MENU_FONT = 'comicsans'

#level3 settings
class level3:
    ghost_h = -1000
    wall_h = 0
    path_h = -1
    coin_h = 20
    p_sight = 3

    first_is_wall_h = -100
    first_is_path_h = -1

    direct_up = "UP"
    direct_down = "DOWN"
    direct_left = "LEFT"
    direct_right = "RIGHT"
