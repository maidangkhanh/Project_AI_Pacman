import pygame
from settings import *
import random
import heapq

vec = pygame.math.Vector2


class Ghost:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = pos
        self.grid_pos = pos
        self.path = []
        self.move_zone = self.level3_move_zone()

    def draw(self):
        pygame.draw.circle(self.app.screen, RED,
                           (int(self.grid_pos[0]*self.app.cell_width + self.app.cell_width//2),
                            int(self.grid_pos[1]*self.app.cell_height + self.app.cell_height//2)),
                           int(self.app.cell_width//3))

    def update(self):
        return

    def update3(self):
        self.move_random()

    def update4(self):
        self.hunt()

    def move_random(self):
        moveable = [x for x in self.neighbours(self.grid_pos) if x in self.move_zone]
        self.grid_pos = random.choice(moveable)

    def level3_move_zone(self):
        res = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                res.append(self.starting_pos + vec(x, y))
        return res

    def neighbours(self, pos):
        up = pos + vec(-1, 0)
        down = pos + vec(1, 0)
        left = pos + vec(0, -1)
        right = pos + vec(0, 1)
        res = []

        if up not in self.app.walls:
            res.append(up)
        if down not in self.app.walls:
            res.append(down)
        if left not in self.app.walls:
            res.append(left)
        if right not in self.app.walls:
            res.append(right)
        return res

    def Heuristic(self, node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def findPacman(self):
        pac_pos = self.app.pacman.grid_pos
        queue = []
        heapq.heappush(queue, (
            self.Heuristic(self.grid_pos, pac_pos), [self.grid_pos[0], self.grid_pos[1]], [], 0))  # Heuristic + cost, coordinate, path, cost

        while queue:
            popped_element = heapq.heappop(queue)
            x = popped_element[1][0]
            y = popped_element[1][1]
            path = popped_element[2]
            cost = popped_element[3]

            if x == pac_pos[0] and y == pac_pos[1]:
                return path[1:] + [pac_pos]

            neighboor = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
            while neighboor:
                adjacent = neighboor.pop()
                x_ = adjacent[0]
                y_ = adjacent[1]
                if x_ in range(0, self.app.col) and y_ in range(0, self.app.row):
                    if vec(x_, y_) not in self.app.walls:
                        if not [x_, y_] in path:
                            coordiante = [x_, y_]
                            h = self.Heuristic(coordiante, pac_pos)
                            v = vec(x, y)
                            heapq.heappush(queue, (h + cost + 1, coordiante, path + [[v.x, v.y]], cost + 1))
        return []

    def hunt(self):
        self.path = self.findPacman()
        if self.path:
            self.grid_pos = self.path.pop(0)
