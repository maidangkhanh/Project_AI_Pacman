import pygame
from settings import *

vec = pygame.math.Vector2


class Ghost:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.target = None

    def draw(self):
        pygame.draw.circle(self.app.screen, RED,
                           (int(self.grid_pos.x*self.app.cell_width + self.app.cell_width//2),
                            int(self.grid_pos.y*self.app.cell_height + self.app.cell_height//2)),
                           int(self.app.cell_width//3))

    def update(self):
        pass
