import sys
import json
import collections
from search.util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

def boom(current_state, coord):
    new_state = current_state.copy()
    for team in new_state:
        for member in team:
            if member[1:3] == coord:
                del member
    xmin = coord[1]-1
    xmax = coord[1]+2
    ymin = coord[2]-1
    ymax = coord[2]+2
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            new_state = boom(new_state, [x,y])

    return new_state

def move(current_state, direction, coord):
    new_state = current_state.copy()
    for white_member in new_state["white"]:
        if white_member[1:3] == coord:
            if direction == "left":
                white_member[1] = white_member[1] - 1
            if direction == "right":
                white_member[1] = white_member[1] + 1
            if direction == "up":
                white_member[2] = white_member[2] + 1
            if direction == "down":
                white_member[2] = white_member[2] - 1
    return new_state

def all_moves(queue, coord, state):
    queue.append(move(state, "left", coord))
    queue.append(move(state, "right", coord))
    queue.append(move(state, "up", coord))
    queue.append(move(state, "down", coord))
    queue.append(boom(state, coord))

class Node:
    def __init__(self, state, children):
        self.state = state
        self.children = None

def bfs(start_state, goal_state):
    state_node = Node(start_state)
    queue = collections.deque([start_state])
    while queue:
        state = queue.popleft()
        if state == goal_state:
            return
        for white_member in state["white"]:
            all_moves(queue, white_member[1:3], state)


if __name__ == '__main__':
    main()
