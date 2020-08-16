from pacman import *
from ghost import *
from collections import deque
import time
import random
from settings import level3 as lv3

pygame.init()

vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.music()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.state = 'start'
        self.level = 1
        self.map = []
        self.row = None
        self.col = None
        self.ghosts = []
        self.coins = []
        self.walls = []
        self.p_pos = []
        self.g_pos = []
        self.cell_width = None
        self.cell_height = None
        mapdir = random.choice(["map0.txt", "map1.txt", "map2.txt", "map3.txt", "map4.txt"])
        self.load(mapdir)
        self.mapping()
        self.pacman = Pac(self, vec(self.p_pos))
        self.make_ghost()

    def run(self):
        while self.running:
            if self.state == 'start':
                self = App()
                self.menu()
            if self.state == 'level1':
                if self.coins:
                    self.coins = [random.choice(self.coins)]
                self.draw(1)
                pygame.time.delay(300)
                self.update()
            if self.state == 'level2':
                if self.coins:
                    self.coins = [random.choice(self.coins)]
                self.draw()
                pygame.time.delay(300)
                self.update2()
            if self.state == 'level3':
                self.draw()
                pygame.time.delay(300)
                self.update3()
            if self.state == 'level4':
                self.draw()
                pygame.time.delay(300)
                self.update4()
            if self.state == 'finish':
                self.finish()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self):
        if not self.coins:
            self.state = 'finish'
        self.pacman.update1()

    def update2(self):
        if not self.coins:
            self.state = 'finish'
        self.pacman.update2()
        for ghost in self.ghosts:
            if ghost.grid_pos == self.pacman.grid_pos:
                self.running = 'finish'

    def update3(self):
        self.level3(3)

    def update4(self):
        if not self.coins:
            self.state = 'finish'
        self.pacman.update4()
        for ghost in self.ghosts:
            if ghost.grid_pos == self.pacman.grid_pos:
                self.state = 'finish'
            ghost.update4()
            if ghost.grid_pos == self.pacman.grid_pos:
                self.running = 'finish'

    def load(self, map_dir="map1.txt"):
        with open(map_dir) as file:
            self.row, self.col = [int(i) for i in file.readline().split(" ")]
            for line in file:
                line = line.split(" ")
                row = []
                for c in line:
                    row.append(int(c))
                self.map.append(row)
            self.p_pos = self.map.pop(-1)
            self.cell_height = HEIGHT // self.row
            self.cell_width = WIDTH // self.col

    def mapping(self):
        for y in range(self.row):
            for x in range(self.col):
                if y == 0:
                    self.walls.append(vec(x, y-1))
                if x == 0:
                    self.walls.append(vec(x-1, y))

                if y == self.row - 1:
                    self.walls.append(vec(x, y+1))
                if x == self.col - 1:
                    self.walls.append(vec(x+1, y))

                if self.map[y][x] == 1:
                    self.walls.append(vec(x, y))
                elif self.map[y][x] == 2:
                    self.coins.append(vec(x, y))
                elif self.map[y][x] == 3:
                    self.g_pos.append(vec(x, y))
    def music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1)
    def make_ghost(self):
        for idx, pos in enumerate(self.g_pos):
            self.ghosts.append(Ghost(self, vec(pos)))

    def draw(self, level=None):
        self.screen.fill(BLACK)
        self.draw_wall()
        self.draw_grid()
        self.draw_coins()
        self.pacman.draw()
        if level is not 1:
            for ghost in self.ghosts:
                ghost.draw()
        pygame.display.update()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, GOLD, (int(coin.x*self.cell_width + self.cell_width//2),
                                                   int(coin.y*self.cell_height + self.cell_height//2)),
                               self.cell_width//9)

    def draw_wall(self):
        for wall in self.walls:
            if wall[0] in range(self.col) and wall[1] in range(self.row):
                pygame.draw.rect(self.screen, BLUE, (wall.x*self.cell_width,
                                                     wall.y*self.cell_height,
                                                     self.cell_width,
                                                     self.cell_height))

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.screen, GREY, (x * self.cell_width, 0),
                             (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.screen, GREY, (0, x * self.cell_height),
                             (WIDTH, x * self.cell_height))

    def menu(self):
        level1 = button(GREEN, WIDTH//2 - 150, 275, 300, 60, 'LEVEL 1')
        level1.draw(self.screen)
        level2 = button(YELLOW, WIDTH//2 - 150, 350, 300, 60, 'LEVEL 2')
        level2.draw(self.screen)
        level3 = button(ORANGE, WIDTH//2 - 150, 425, 300, 60, 'LEVEL 3')
        level3.draw(self.screen)
        level4 = button(RED, WIDTH//2 - 150, 500, 300, 60, 'LEVEL 4')
        level4.draw(self.screen)

        self.draw_text('PACMAN', self.screen, [WIDTH//2, 140], MENU_TEXT_SIZE, WHITE, MENU_FONT, True)

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1.isOver(pos):
                    self.state = 'level1'
                if level2.isOver(pos):
                    self.state = 'level2'
                if level3.isOver(pos):
                    self.state = 'level3'
                if level4.isOver(pos):
                    self.state = 'level4'

            if event.type == pygame.QUIT:
                self.running = False

    def finish(self):
        self.screen.fill(BLACK)
        final_score = self.pacman.score
        display_text = 'SCORE: ' + str(final_score)
        self.draw_text(display_text, self.screen, [WIDTH//2, 140], MENU_TEXT_SIZE*2, WHITE, MENU_FONT, True)
        main_menu = button(GREEN, 100, 350, 250, 60, 'MAIN MENU')
        main_menu.draw(self.screen)
        quit_button = button(GREEN, 450, 350, 250, 60, 'QUIT')
        quit_button.draw(self.screen)
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu.isOver(pos):
                    self.state = 'start'
                if quit_button.isOver(pos):
                    self.running = False

            if event.type == pygame.QUIT:
                self.running = False

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0]-text_size[0]//2
            pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)

        # level 3

    def heuristic_lv3(self, pacman_pos, direction, limit):
        # get first step
        if direction == lv3.direct_up:
            first = (pacman_pos[0], ((pacman_pos[1] - 1 + self.row) % self.row))
        if direction == lv3.direct_down:
            first = (pacman_pos[0], ((pacman_pos[1] + 1 + self.row) % self.row))
        if direction == lv3.direct_left:
            first = ((pacman_pos[0] - 1 + self.col) % self.col, pacman_pos[1])
        if direction == lv3.direct_right:
            first = ((pacman_pos[0] + 1 + self.col) % self.col, pacman_pos[1])

        frontier = deque()
        frontier.append((first, 1))

        expanded = [pacman_pos]

        heuristic = 0

        ghost_detect = False
        coin_detect = False
        while frontier:
            pos, cost = frontier.popleft()

            expanded.append(pos)

            type = self.pos_type_lv3(pos)

            if type == lv3.ghost_h and cost <= 2:
                ghost_detect = True
                heuristic += lv3.ghost_h
                continue

            if type == lv3.wall_h:
                continue

            if type == lv3.coin_h:
                coin_detect = True
                heuristic += lv3.coin_h * (limit - cost + 1)

            if type == lv3.path_h:
                heuristic += lv3.path_h

            if cost < limit:
                up = (pos[0], ((pos[1] - 1 + self.row) % self.row))
                down = (pos[0], ((pos[1] + 1 + self.row) % self.row))
                left = ((pos[0] - 1 + self.col) % self.col, pos[1])
                right = ((pos[0] + 1 + self.col) % self.col, pos[1])

                adjacency_list = [up, down, left, right]
                for node in adjacency_list:
                    f_exist = False
                    for f_node in frontier:
                        if f_node[0] == node:
                            f_exist = True
                            break

                    if node not in expanded and not f_exist:
                        frontier.append((node, cost + 1))

        if not ghost_detect and not coin_detect:
            type = self.pos_type_lv3(first)
            if type == lv3.wall_h:
                return lv3.first_is_wall_h
            if type == lv3.path_h:
                return lv3.first_is_path_h

        return heuristic

    def pos_type_lv3(self, pos):
        for ghost in self.ghosts:
            if pos == ghost.grid_pos:
                return lv3.ghost_h

        for coin in self.coins:
            if pos == coin:
                return lv3.coin_h

        for wall in self.walls:
            if pos == wall:
                return lv3.wall_h

        return lv3.path_h

    def level3(self, speed=1000):
        points = 0

        lastDirection_reverse_heuristic = 0
        lastDirection_reverse = None
        last_pos = self.pacman.grid_pos

        ghostOrginalPos = list()
        for ghost in self.ghosts:
            ghostOrginalPos.append(ghost.grid_pos)

        ghostLastPos = list()
        for ghost in self.ghosts:
            ghostLastPos.append(ghost.grid_pos)

        count = 0  # use for ghost moves
        while True:
            last_pos = self.pacman.grid_pos

            # stop conditions
            i = 0
            end = False
            for ghost in self.ghosts:
                if ghost.grid_pos == last_pos and self.pacman.grid_pos == ghostLastPos[i]:
                    points += -1000
                    end = True
                if ghost.grid_pos == self.pacman.grid_pos:
                    points += -1000
                    end = True
                i += 1
            if end:
                self.running = 'finish'
                break

            type = self.pos_type_lv3(self.pacman.grid_pos)
            if type == lv3.coin_h:
                points += lv3.coin_h
                self.coins.remove(self.pacman.grid_pos)

            if len(self.coins) == 0:
                self.state = 'finish'
                break

            # calculate heuristics
            heuristics = {lv3.direct_up: 0, lv3.direct_down: 0, lv3.direct_left: 0, lv3.direct_right: 0}
            for direction in heuristics:
                if direction != lastDirection_reverse:
                    heuristics[direction] = self.heuristic_lv3(self.pacman.grid_pos, direction, lv3.p_sight)
                else:
                    if lastDirection_reverse_heuristic > 0: #there are coins but no ghosts
                        heuristics[direction] = self.heuristic_lv3(self.pacman.grid_pos, direction, lv3.p_sight)
                    else:
                        heuristics[direction] = lv3.first_is_path_h - 1
            # choose pacman direction
            max_h = heuristics[max(heuristics, key=heuristics.get)]

            max_directions = list()
            for direction, value in heuristics.items():
                if value == max_h:
                    max_directions.append(direction)
            next_direction = random.choice(max_directions)
            lastDirection_reverse = self.reverse_direction(next_direction)
            lastDirection_reverse_heuristic = self.heuristic_lv3(self.pacman.grid_pos, lastDirection_reverse, lv3.p_sight)

            # ghosts move
            for ghost in self.ghosts:
                ghostLastPos.append(ghost.grid_pos)

            ghost_directions = [lv3.direct_up, lv3.direct_down, lv3.direct_left, lv3.direct_right]

            if count % 2 == 0:
                for ghost in self.ghosts:
                    next_ghost_direction = random.choice(ghost_directions)
                    ghost.move_lv3(next_ghost_direction)
            else:
                i = 0
                for ghost in self.ghosts:
                    ghost.move(ghostOrginalPos[i])
                    i += 1

            # pacman move
            last_pos = self.pacman.grid_pos
            points += - self.pacman.move_lv3(next_direction)

            self.draw()

            count += 1

            # exit buttons
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

            time.sleep(1 / speed)

        self.pacman.score = points

    def reverse_direction(self, direction):
        if direction == lv3.direct_up:
            return lv3.direct_down
        if direction == lv3.direct_down:
            return lv3.direct_up
        if direction == lv3.direct_left:
            return lv3.direct_right
        if direction == lv3.direct_right:
            return lv3.direct_left
        else:
            return None


# credit to Tech With Tim
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                            self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False



