import sys
import json
import collections
from search.util import print_move, print_boom, print_board




    # TODO: find and print winning action sequence

def boom(current_state, coord):
    new_state = current_state.copy()
    for member in new_state["white"]:
        if member[1:3] == coord:
            new_state["white"].remove(member)
            xmin = coord[0]-1
            xmax = coord[0]+2
            ymin = coord[1]-1
            ymax = coord[1]+2
            for x in range(xmin, xmax):
                for y in range(ymin, ymax):
                    new_state = boom(new_state, [x,y])

    return new_state

def move(current_state, direction, coord):
    new_state = current_state.copy()
    for white_member in new_state["white"]:
        if white_member[1:3] == coord:
            if direction == "left":
                white_member[1] -= 1
            if direction == "right":
                white_member[1] += 1
            if direction == "up":
                white_member[2] += 1
            if direction == "down":
                white_member[2] -= 1
    return new_state

def add_all_moves(queue, path, coord, state):
    if coord[0] >= 0:
        queue.append(path + [move(state, "left", coord)])

    if coord[0] <= 7:
        queue.append(path + [move(state, "right", coord)])

    if coord[1] <= 7:
        queue.append(path + [move(state, "up", coord)])

    if coord[1] >= 0:
        queue.append(path + [move(state, "down", coord)])

    queue.append(path + [boom(state, coord)])

class Node:
    def __init__(self, state, children):
        self.state = state
        self.children = None

def bfs(start_state):
    queue = collections.deque([[start_state]])
    while queue:
        path = queue.popleft()
        current_state = path[-1]
        if len(current_state["black"]) == 0:
            return path
        for white_member in current_state["white"]:
            add_all_moves(queue, path, white_member[1:3], current_state)

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        path = bfs(data)
        print(path)
        #queue = collections.deque([[data]])
        #path = queue.popleft()
        #print("PATH")
        #print(path)
        #current_state = path[-1]
        #for white_member in current_state["white"]:
        #    add_all_moves(queue, path, white_member[1:3], current_state)


if __name__ == '__main__':
    main()
