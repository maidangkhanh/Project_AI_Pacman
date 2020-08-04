from pacman import *
from ghost import *

pygame.init()

vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
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
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self):
        self.pacman.update()
        for ghost in self.ghosts:
            ghost.update()

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
                if y == 0 and x == 0:
                    self.walls.append(vec(x-1, y-1))
                elif y == 0:
                    self.walls.append(vec(x, y-1))
                elif x == 0:
                    self.walls.append(vec(x-1, y))

                if y == self.row - 1 and x == self.col - 1:
                    self.walls.append(vec(x+1, y+1))
                elif y == self.row - 1:
                    self.walls.append(vec(x, y+1))
                elif x == self.col - 1:
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

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_wall()
        self.draw_grid()
        self.draw_coins()
        self.pacman.draw()
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


