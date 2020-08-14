from pacman import *
from ghost import *

pygame.init()

vec = pygame.math.Vector2


class App:
    def __init__(self):
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
        self.load()
        self.mapping()
        self.pacman = Pac(self, vec(self.p_pos))
        self.make_ghost()

    def run(self):
        while self.running:
            if self.state == 'start':
                self = App()
                self.menu()
            if self.state == 'level1':
                self.draw(1)
                pygame.time.delay(300)
                self.update()
            if self.state == 'level2':
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
        if not self.coins:
            self.state = 'finish'
        self.pacman.update3()
        for ghost in self.ghosts:
            if ghost.grid_pos == self.pacman.grid_pos:
                self.running = 'finish'
            ghost.update3()
            if ghost.grid_pos == self.pacman.grid_pos:
                self.running = 'finish'

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

    def load(self, map_dir="map0.txt"):
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


