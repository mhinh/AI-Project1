import sys
import json
import collections

from search.util import print_move, print_boom, print_board


class Node:
    def __init__(self, state):
        self.state = state
        self.children = None


def move(white_order, direction, current_state):
    if direction == 'LEFT' and current_state.state['white'][white_order][1] > 0:
        current_state.state['white'][white_order][1] -= 1
    elif direction == 'RIGHT' and current_state.state['white'][white_order][1] < 7:
        current_state.state['white'][white_order][1] += 1
    elif direction == 'UP' and current_state.state['white'][white_order][2] < 7:
        current_state.state['white'][white_order][2] += 1
    elif direction == 'DOWN' and current_state.state['white'][white_order][2] > 0:
        current_state.state['white'][white_order][2] -= 1


def bfs(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if boom(grid,(x,y)):
            grid[start[0]][start[1]] = "   "
            return path
        for x2, y2 in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= x2 < width and 0 <= y2 < height and (x2, y2) not in seen and grid[x2][y2][0] != 'b':
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))
def copy_grid(grid):
    new_grid=[]
    for i in range(len(grid)):
        temp = []
        for elem in grid[i]:
            temp.append(elem)
        new_grid.append(temp)
    return new_grid

def boom(grid,coord):
    x, y = coord[0], coord[1]
    temp_grid = copy_grid(grid)
    temp_grid[x][y] = "  "
    for x2,y2 in (
    (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)):
        if 0 <= x2 <= 7 and 0 <= y2 <= 7:
            if temp_grid[x2][y2][0] == 'b':
                boom(temp_grid,(x2,y2))
            temp_grid[x2][y2] = "   "
    for i in range(len(temp_grid)):
        for elem in temp_grid[i]:
            if elem[0] == 'b':
                return False
    for i in range(8):
        for j in range(8):
            if grid[i][j] != temp_grid[i][j]:
                grid[i][j] = temp_grid[i][j]
    return True


def main():
    init_table = {}
    with open(sys.argv[1]) as file:
        data = json.load(file)
        print(data)

        for key, value in data.items():
            for i in range(len(value)):
                init_table[(value[i][1], value[i][2])] = key[0] + ',' + str(value[i][0])

        print_board(init_table)

        grid = []
        for x in range(8):
            cells = []
            for y in range(8):
                if (x, y) not in init_table:
                    cells.append("   ")
                else:
                    cells.append(str(init_table[x, y]))
            grid.append(cells)
        white_location = (data['white'][0][1], data['white'][0][2])
        path = bfs(grid, white_location)
        print(path)
        print(grid)
        #for i in range(len(path)-1):
        #    print_move(1,path[i][0],path[i][1],path[i+1][0],path[i+1][1])
        #print_boom(path[-1][0],path[-1][1])

        #print(grid)

        # start_state = Node(data)
        # move(0,'DOWN',start_state)
        # move(0, 'DOWN', start_state)
        # move(0, 'DOWN', start_state)
        # move(0, 'DOWN', start_state

        # print(start_state.state)

        # for key,value in start_state.state.items():
        #    for i in range(len(value)):
        #        table[(value[i][1],value[i][2])] = key[0] + ',' + str(value[i][0])

        # print_board(table)

    # TODO: find and print winning action sequence


if __name__ == '__main__':
    width, height = 7, 7
    main()
