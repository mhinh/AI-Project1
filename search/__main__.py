import sys
import json
import collections
import copy
from search.util import print_move, print_boom, print_board




    # TODO: find and print winning action sequence

def boom(current_state, coord):
    new_state = copy.deepcopy(current_state)
    for team in new_state.keys():
        for member in new_state[team]:

            #print("TEAM", end=" ")
            #print(team)
            #print("MEMBER", end=" ")
            #print(member)
            if member[1:3] == coord:
                new_state[team].remove(member)
                xmin = coord[0]-1
                xmax = coord[0]+2
                ymin = coord[1]-1
                ymax = coord[1]+2
                for x in range(xmin, xmax):
                    for y in range(ymin, ymax):
                        new_state = boom(new_state, [x,y])

    return new_state

def move(current_state, direction, coord):
    new_state = copy.deepcopy(current_state)
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
    #print("CURRENT STATE")
    #print(current_state)
    #print("NEW STATE")
    #print(new_state)
    return new_state

def add_all_moves(queue, path, coord, state):
    path_len = len(path)
    if coord[0] > 0:
        if (path_len==1) or (path_len>1 and path[-2]!=move(state, "left", coord)):
        #print("ADD LEFT", end=" ")
        #print(move(state, "left", coord))
            queue.append(path + [move(state, "left", coord)])
        #print("STATE AFTER MOVE LEFT")
        #print(state)

    if coord[0] < 7:
        if (path_len==1) or (path_len>1 and path[-2]!=move(state, "right", coord)):
        #print("ADD RIGHT", end=" ")
        #print(move(state, "right", coord))
            queue.append(path + [move(state, "right", coord)])
        #print("STATE AFTER MOVE RIGHT")
        #print(state)

    if coord[1] < 7:
        if (path_len==1) or (path_len>1 and path[-2]!=move(state, "up", coord)):
        #print("ADD UP", end=" ")
        #print(move(state, "up", coord))
            queue.append(path + [move(state, "up", coord)])

    if coord[1] > 0:
        if (path_len==1) or (path_len>1 and path[-2]!=move(state, "down", coord)):
        #print("ADD DOWN", end=" ")
        #print(move(state, "down", coord))
            queue.append(path + [move(state, "down", coord)])

    #print("ADD BOOM", end=" ")
    #print(boom(state, coord))
    queue.append(path + [boom(state, coord)])

class Node:
    def __init__(self, state, children):
        self.state = state
        self.children = None

def bfs(start_state):
    queue = collections.deque([[start_state]])
    while queue:
        path = queue.popleft()
        #print(path)
        current_state = path[-1]
        if len(current_state["black"]) == 0:
            return path
        for white_member in current_state["white"]:
            add_all_moves(queue, path, white_member[1:3], current_state)

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        #print(boom(data, [1,4]))
        #print(move(data, "right", [1,4]))
        #print("STATE AFTER MOVE")
        #print(data)
        path = bfs(data)
        print(path)
        for i in range(len(path)):
            table = {}
            print(path[i])
            for key, value in path[i].items():
                for j in range(len(value)):
                    table[(value[j][1], value[j][2])] = key[0] + ',' + str(value[j][0])

            print_board(table)
        #queue = collections.deque([[data]])
        #path = queue.popleft()
        #print("PATH")
        #print(path)
        #current_state = path[-1]
        #for white_member in current_state["white"]:
        #    add_all_moves(queue, path, white_member[1:3], current_state)
        #print("RESULTING QUEUE")
        #print(queue)


if __name__ == '__main__':
    main()
