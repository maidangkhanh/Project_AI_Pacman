import heapq
import operator
import math


def Heuristic(node, goal):
    return abs(math.floor(node[0] - goal[0])) + abs(math.floor(node[1] - goal[1]))

def Level1_Pacman(map, size, start, food):

    queue = []
    heapq.heappush(queue, (Heuristic(start, food), start, [], 0))#Heuristic + cost, coordinate, path, cost

    while queue:
        popped_element = heapq.heappop(queue)
        x = popped_element[1][0]
        y = popped_element[1][1]
        path = popped_element[2]
        cost = popped_element[3]

        if x == food[0] and y == food[1]:
            return path + [food]

        neighboor = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        while neighboor:
            adjacent = neighboor.pop()
            x_ = adjacent[0]
            y_ = adjacent[1]
            if x_ in range(0, size[0]) and y_ in range(0, size[1]):
                if map[x_][y_] != 1:
                    if not [x_, y_] in path:
                        coordiante = [x_, y_]
                        heapq.heappush(queue, (Heuristic(coordiante, food) + cost + 1, coordiante, path + [[x, y]],cost + 1))

    return "Fail"


def Level2_Pacman(map, size, start, food):
    queue = []
    heapq.heappush(queue, (Heuristic(start, food), start, [], 0))  # Heuristic + cost, coordinate, path, cost

    while queue:
        popped_element = heapq.heappop(queue)
        x = popped_element[1][0]
        y = popped_element[1][1]
        path = popped_element[2]
        cost = popped_element[3]

        if x == food[0] and y == food[1]:
            return path + [food]

        neighboor = [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]
        while neighboor:
            adjacent = neighboor.pop()
            x_ = adjacent[0]
            y_ = adjacent[1]
            if x_ in range(0, size[0]) and y_ in range(0, size[1]):
                if map[x_][y_] != 1 and map[x_][y_] != 3:
                    if not [x_, y_] in path:
                        coordiante = [x_, y_]
                        heapq.heappush(queue,
                                       (Heuristic(coordiante, food) + cost + 1, coordiante, path + [[x, y]], cost + 1))

    return "Fail"



def ReadMap(Filename):
    fin = open(Filename)
    matrix = []
    for line in fin:
        line = line.split(' ')
        if line == ['\n']:
            cell = []
        else:
            cell = (list(map(int, line)))
        matrix.append(cell)

    size = matrix.pop(0)
    start = matrix.pop()
    return matrix, size, start


if __name__ == '__main__':
    map, size, start = ReadMap("map0.txt")

    food = [4, 4]

    path = Level1_Pacman(map, size, start, food)
    print("Start: ", start)
    print("Food: ", food)
    print("Path: ", path)





