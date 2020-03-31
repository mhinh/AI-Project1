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

    return new_state

def movable(current_state, direction, coord, path):
    if direction == "left":
        if coord[0] <= 0:
            return False
        for black_member in current_state["black"]:
            if black_member[2] == coord[1] and black_member[1] == coord[0]-1:
                return False
    if direction == "right":
        if coord[0] >= 7:
            return False
        for black_member in current_state["black"]:
            if black_member[2] == coord[1] and black_member[1] == coord[0]+1:
                return False
    if direction == "up":
        if coord[1] >= 7:
            return False
        for black_member in current_state["black"]:
            if black_member[1] == coord[0] and black_member[2] == coord[1]+1:
                return False
    if direction == "down":
        if coord[1] <= 0:
            return False
        for black_member in current_state["black"]:
            if black_member[1] == coord[0] and black_member[2] == coord[1]-1:
                return False

    new_state = move(current_state, direction, coord)
    if len(path)>1 and path[-2]==new_state:
        return False

    return True

def add_all_moves(queue, path,seen, coord, state):
    if movable(state, "left", coord, path) and move(state, "left", coord) not in seen:
        queue.append(path + [move(state, "left", coord)])
        seen.append(move(state, "left", coord))
    if movable(state, "right", coord, path) and move(state, "right", coord) not in seen:
        queue.append(path + [move(state, "right", coord)])
        seen.append(move(state, "right", coord))
    if movable(state, "up", coord, path) and move(state, "up", coord) not in seen:
        queue.append(path + [move(state, "up", coord)])
        seen.append(move(state, "up", coord))
    if movable(state, "down", coord, path) and move(state, "down", coord) not in seen:
        queue.append(path + [move(state, "down", coord)])
        seen.append(move(state, "down", coord))

    queue.append(path + [boom(state, coord)])

def bfs(start_state):
    queue = collections.deque([[start_state]])
    seen = list([start_state])
    while queue:
        path = queue.popleft()
    #    print(path)
        current_state = path[-1]
        if len(current_state["black"]) == 0:
            return path
        for white_member in current_state["white"]:
            add_all_moves(queue, path,seen, white_member[1:3], current_state)

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
            #print(path[i])
            for key, value in path[i].items():
                for j in range(len(value)):
                    table[(value[j][1], value[j][2])] = key[0] + ',' + str(value[j][0])

            #print_board(table)
        for i in range(len(path)-1):
            if path[i+1]['white'] != [] :
                if len(path[i]['white']) != len(path[i+1]['white']):
                    print_boom(path[i]['white'][0][1],path[i]['white'][0][2])
                    continue
                print_move(1,path[i]['white'][0][1],path[i]['white'][0][2],path[i+1]['white'][0][1],path[i+1]['white'][0][2])
            else:
                print_boom(path[i]['white'][0][1], path[i]['white'][0][2])

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