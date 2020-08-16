import pygame
from settings import *
import random
vec = pygame.math.Vector2
import heapq


class Pac:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = pos
        self.grid_pos = pos
        self.score = 0
        self.path = []
        self.danger_zone = []
        self.seen_coins = []
        # self.unexplored_pos = []
        # self.get_unexplored_pos()
        # self.explored_pos = []


    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR,
                           (int(self.grid_pos[0]*self.app.cell_width + self.app.cell_width//2),
                            int(self.grid_pos[1]*self.app.cell_height + self.app.cell_height//2)),
                           int(self.app.cell_width//3))

    def update1(self):
        self.move1()
        self.check_coins()

    def update2(self):
        self.move2()
        self.check_coins()

    def update3(self):
        # self.explore()
        # self.check_coins()
        pass

    def update4(self):
        self.move4()
        self.check_coins()

    def move1(self):
        if not self.path:
            self.path = self.find_coins1()
        if self.path:
            self.grid_pos = self.path.pop(0)
            self.score -= 1
        else:
            self.app.state = 'finish'

    def move2(self):
        if not self.path:
            self.path = self.find_coins2()
        if self.path:
            self.grid_pos = self.path.pop(0)
            self.score -= 1
        else:
            self.app.state = 'finish'

    def move4(self):
        self.path = self.BFS()
        if self.grid_pos not in self.danger_zone:
            if self.path:
                self.grid_pos = self.path.pop(0)
                self.score -= 1
            elif self.starting_pos in self.app.coins:
                pass
            else:
                self.app.state = 'finish'
        else:
            self.avoid()


    def check_coins(self):
        if self.grid_pos in self.app.coins:
            self.app.coins.remove(self.grid_pos)
            if self.grid_pos in self.seen_coins:
                self.seen_coins.remove(self.grid_pos)
            self.score += 20


    def find_coins2(self):
        if self.app.coins:
            coin_pos = [self.app.coins[0][0], self.app.coins[0][1]]
            queue = [(self.grid_pos, [])] # , coordinate, path
            explored = []

            while queue:
                popped_element = queue.pop(0)
                x = popped_element[0][0]
                y = popped_element[0][1]
                path = popped_element[1]

                if x == coin_pos[0] and y == coin_pos[1]:
                    return path[1:] + [coin_pos]
                elif [x,y] not in explored:
                    explored.append([x,y])

                neighboor = [[x, (y - 1 + self.app.row) % self.app.row], [x, (y + 1 + self.app.row) % self.app.row], [(x - 1 + self.app.col) % self.app.col, y], [(x + 1 + self.app.col) % self.app.col, y]]
                while neighboor:
                    adjacent = neighboor.pop(0)
                    x_ = adjacent[0]
                    y_ = adjacent[1]
                    if vec(x_, y_) not in self.app.walls and vec(x_,y_) not in self.app.g_pos:
                        if not [x_, y_] in explored and [x_, y_] not in queue:
                            coordiante = [x_, y_]
                            queue.append((coordiante, path + [[x, y]]))

            return []

    def find_coins1(self):
        if self.app.coins:
            coin_pos = [self.app.coins[0][0], self.app.coins[0][1]]
            queue = [(self.grid_pos, [])] # , coordinate, path
            explored = []

            while queue:
                popped_element = queue.pop(0)
                x = popped_element[0][0]
                y = popped_element[0][1]
                path = popped_element[1]

                if x == coin_pos[0] and y == coin_pos[1]:
                    return path[1:] + [coin_pos]
                elif [x,y] not in explored:
                    explored.append([x,y])

                neighboor = [[x, (y - 1 + self.app.row) % self.app.row], [x, (y + 1 + self.app.row) % self.app.row], [(x - 1 + self.app.col) % self.app.col, y], [(x + 1 + self.app.col) % self.app.col, y]]
                while neighboor:
                    adjacent = neighboor.pop(0)
                    x_ = adjacent[0]
                    y_ = adjacent[1]
                    if vec(x_, y_) not in self.app.walls:
                        if not [x_, y_] in explored and [x_, y_] not in queue:
                            coordiante = [x_, y_]
                            queue.append((coordiante, path + [[x, y]]))

            return []


    def BFS(self):
        goals = self.app.coins
        self.danger_zone = self.dangerous_zone()
        cur = self.grid_pos
        queue = [[cur]]
        while queue:
            path = queue.pop(0)
            cur = path[-1]
            if cur in goals:
                return path[1:]
            adjacents = self.neighbours(cur)
            for adjacent in adjacents:
                if adjacent not in self.danger_zone and adjacent not in path:
                    queue.append(path + [adjacent])
        return []

    def avoid(self):
        neighbours = self.neighbours(self.grid_pos)
        safety = []
        for neighbour in neighbours:
            if neighbour not in self.danger_zone:
                safety.append(neighbour)
        if self.path:
            if self.path[0] in safety:
                self.grid_pos = self.path.pop(0)
                self.score -= 1
            else:
                self.grid_pos = random.choice(safety)
                self.score -= 1
        else:
            self.app.state = 'finish'

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

    def dangerous_zone(self):
        res = []
        for ghost in self.app.ghosts:
            res += self.neighbours(ghost.grid_pos)
        return res
    # def perceive(self):
    #     for y in range(-1, 2):
    #         for x in range(-1, 2):
    #             perceived_cell = self.grid_pos + vec(x, y)
    #             if perceived_cell in self.app.coins and perceived_cell not in self.seen_coins:
    #                 self.seen_coins.append(perceived_cell)
    #
    # def explore(self):
    #     self.perceive()
    #     if self.grid_pos in self.unexplored_pos:
    #         self.unexplored_pos.remove(self.grid_pos)
    #     if not self.path:
    #         if self.seen_coins:
    #             self.path = self.BFS(self.seen_coins)
    #         else:
    #             self.path = self.BFS(self.unexplored_pos)
    #     self.grid_pos = self.path.pop(0)
    #
    #
    # def get_unexplored_pos(self):
    #     for y in range(self.app.row):
    #         for x in range(self.app.col):
    #             if vec(x, y) not in self.app.walls and vec(x, y) not in self.app.g_pos:
    #                 self.unexplored_pos.append(vec(x, y))

    def move(self, des):
        self.grid_pos = des

    def move_up(self):
        pos = (self.grid_pos[0], (self.grid_pos[1] - 1 + self.app.row) % self.app.row)
        type = self.app.pos_type_lv3(pos)

        if type == level3.wall_h:
            return 0

        self.move(vec(pos))
        return 1

    def move_down(self):
        pos = (self.grid_pos[0], (self.grid_pos[1] + 1 + self.app.row) % self.app.row)
        type = self.app.pos_type_lv3(pos)

        if type == level3.wall_h:
            return 0

        self.move(vec(pos))
        return 1

    def move_left(self):
        pos = ((self.grid_pos[0] - 1 + self.app.col) % self.app.col, self.grid_pos[1])
        type = self.app.pos_type_lv3(pos)

        if type == level3.wall_h:
            return 0

        self.move(vec(pos))
        return 1

    def move_right(self):
        pos = ((self.grid_pos[0] + 1 + self.app.col) % self.app.col, self.grid_pos[1])
        type = self.app.pos_type_lv3(pos)

        if type == level3.wall_h:
            return 0

        self.move(vec(pos))
        return 1

    def move_lv3(self, direction):
        if direction == level3.direct_up:
            return self.move_up()
        elif direction == level3.direct_down:
            return self.move_down()
        elif direction == level3.direct_left:
            return self.move_left()
        elif direction == level3.direct_right:
            return self.move_right()

def Heuristic(node, goal):
    return abs((node[0] - goal[0])) + abs((node[1] - goal[1]))


