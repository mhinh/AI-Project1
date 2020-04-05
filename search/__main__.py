import sys
import json
import collections
import copy
from search.util import print_move, print_boom, print_board

    # TODO: find and print winning action sequence

def boom(current_state, coord, boomed):
    #print("+++++++START++++++++")
    #print("coord", end=":")
    #print(coord)
    #print("STATE BEFORE BOOM", end=":")
    #print(current_state)
    new_state = {}
    new_state["white"] = [x for x in current_state["white"] if x[1:3] != coord]
    new_state["black"] = [y for y in current_state["black"] if y[1:3] != coord]
    boomed.append(coord)
    #print("STATE AFTER BOOM", end=":")
    #print(new_state)
    #base case: removed all tokens or no tokens around
    xmin = coord[0]-1
    if xmin < 0:
        xmin = 0
    xmax = coord[0]+2
    if xmax > 8:
        xmax = 8
    ymin = coord[1]-1
    if ymin < 0:
        ymin = 0
    ymax = coord[1]+2
    if ymax > 8:
        ymax = 8
    #print(range(xmin, xmax))
    #print(range(ymin, ymax))
    if len(new_state["white"]) == 0 and len(new_state["black"]) == 0:
    #    print("ALL BOOMED")
        return new_state
    #print("START BOOMING NEIGHBORS")
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
    #        print("x y", end=":")
    #        print([x,y])
            if [x,y] not in boomed:
    #            print("already deleted")
                for member in new_state["white"]+new_state["black"]:
    #                print("check member", end=" ")
    #                print(member[1:3], end=" ")
    #                print("against", end=" ")
    #                print([x,y])
                    if member[1:3] == [x,y]:
    #                    print("---------RECURSE----------")
                        new_state = boom(new_state, [x,y], boomed)
                        break;
    #print(".........End Recurse for", end=" ")
    #print(coord)

    return new_state

def move_stack(current_state, coord, direction, distance, number, round):
    new_state = copy.deepcopy(current_state)

    #if moving onto another white then form a stack
    white_list=[[white[1], white[2]] for white in current_state["white"]]
    f_coord = future_coord(coord, direction, distance)
    if f_coord in white_list:
        for white_member in new_state["white"]:
            if white_member[1:3] == coord:
                #if moving all of the stack at once
                if white_member[0] == number:
                    new_state["white"].remove(white_member)
                    break
                #if moving part of the stack
                if white_member[0] > number:
                    white_member[0] -= number


        for white_member in new_state["white"]:
            if white_member[1:3] == f_coord:
                white_member[0] += number
                return new_state

    #if not moving onto any other white
    for white_member in new_state["white"]:
        if white_member[1:3] == coord:
            #if moving all of the stack at once
            if number == white_member[0]:
                #white_member[1:3] = f_coord
                white_member[1] = f_coord[0]
                white_member[2] = f_coord[1]
            #if moving a part of the stack
            if number < white_member[0]:
                white_member[0] -= number
                new_state["white"] += [[number] + f_coord]

    return new_state

def future_coord(current_coord, direction, distance):
    future_coord = copy.deepcopy(current_coord)
    if direction == "left":
        future_coord[0] -= distance
    if direction == "right":
        future_coord[0] += distance
    if direction == "up":
        future_coord[1] += distance
    if direction == "down":
        future_coord[1] -= distance
    return future_coord

def movable_stack(current_state, coord, direction, distance):
    f_coord = []
    f_coord = future_coord(coord, direction, distance)

    #check if not going out of the board
    for i in f_coord:
        if i<0 or i>7:
            return False

    #check if not going to black
    black_list=[[black[1], black[2]] for black in current_state["black"]]
    if f_coord in black_list:
        return False

    return True

def valid_stack(state, round):
    for white_member in state["white"]:
        if white_member[0] > round:
            return False
    return True

def count_members(team):
    count = 0
    for member in team:
        count += member[0]
    return count

def add_stack_moves(queue, path, seen, state, member, round):
    new_state = {}
    directions = ["left", "right", "up", "down"]
    for number in range(1, round):

        for distance in range(1, member[0]+1):
            for direction in directions:
                if movable_stack(state, member[1:3], direction, distance):
                    new_state = move_stack(state, member[1:3], direction, distance, number, round)
                    if new_state not in seen and valid_stack(new_state, round):
                        queue.append(path + [new_state])
                        seen.append(new_state)
    new_state = boom(state, member[1:3], [])
    if not (new_state["white"] == 0 and new_state["black"] > 0):
        if new_state not in seen:
            queue.append(path + [new_state])
            seen.append(new_state)

def first_bfs(start_state, round):
    queue = collections.deque([[start_state]])
    seen = list([start_state])
    while queue:
        path = queue.popleft()
        current_state = path[-1]

        if count_members(current_state["black"]) <= count_members(current_state["white"]):
            return path
        for white_member in current_state["white"]:
            #add_all_moves(queue, path, seen, white_member[1:3], current_state)
            add_stack_moves(queue, path, seen, current_state, white_member, round)

def bfs(start_state, round):
    queue = collections.deque([[start_state]])
    seen = list([start_state])
    while queue:
        path = queue.popleft()
        current_state = path[-1]
        #boom_state = copy.deepcopy(current_state)
        #for white_member in boom_state["white"]:
    #        boom_state = boom(boom_state, white_member[1:3])
        if len(current_state["black"]) == 0:
            return path
        for white_member in current_state["white"]:
            #add_all_moves(queue, path, seen, white_member[1:3], current_state)
            add_stack_moves(queue, path, seen, current_state, white_member, round)

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        #print("FIRST ROUND")
        #path1 = first_bfs(data)
        #for state in path1:
        #    print(state)
        #current_state = path1[-1]
        #print("SECOND ROUND")
        #if len(current_state["black"]) > 0:
        #    path2 = bfs(current_state)
        #    for state in path2:
        #        print(state)
        max_rounds = count_members(data["white"])
        round = 1
        path = None
        while path == None and round <= max_rounds:
            print("round", end=" ")
            print(round)
            path = bfs(data, round)
            round += 1

        #new_state["white"] = [x for x in data["white"] if x[1:3] != [1,4]]
        #new_state["black"] = data["black"]
        #print("NEW STATE", end=":")
        #print(new_state)
        #print("DATA", end=":")
        #print(data)
        #print(boom(data, [1,4], []))
        print(path)
        #queue = collections.deque([[data]])
        #seen = list([data])
        #path = queue.popleft()
        #current_state = path[-1]
        #add_stack_moves(queue, path, seen, current_state, data["white"][0])
        #for path in queue:
        #    print(path)
        #for i in range(len(path)):
        #    table = {}
        #    for key, value in path[i].items():
        #        for j in range(len(value)):
        #            table[(value[j][1], value[j][2])] = key[0] + ',' + str(value[j][0])

        #    print_board(table)
        #for i in range(len(path) - 1):
        #    if path[i + 1]['white'] != []:
        #        if len(path[i]['white']) != len(path[i + 1]['white']):
         #           print_boom(path[i]['white'][0][1], path[i]['white'][0][2])
          #          continue
           #     print_move(1, path[i]['white'][0][1], path[i]['white'][0][2], path[i + 1]['white'][0][1],
           #                path[i + 1]['white'][0][2])
          #  else:
          #      print_boom(path[i]['white'][0][1], path[i]['white'][0][2])



if __name__ == '__main__':
    main()
