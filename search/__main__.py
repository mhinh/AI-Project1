import sys
import json
import collections
import copy
import heapq
from search.util import print_move, print_boom, print_board

    # TODO: find and print winning action sequence

#boom the token and return the game state after booming
def boom(current_state, coord, boomed):
    new_state = {}
    new_state["white"] = [x for x in current_state["white"] if x[1:3] != coord]
    new_state["black"] = [y for y in current_state["black"] if y[1:3] != coord]
    boomed.append(coord)
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
    if len(new_state["white"]) == 0 and len(new_state["black"]) == 0:
        return new_state
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            if [x,y] not in boomed:
                for member in new_state["white"]+new_state["black"]:
                    if member[1:3] == [x,y]:
                        new_state = boom(new_state, [x,y], boomed)
                        break;

    return new_state

#apply the move and return the game state after moving
def move_stack(current_state, coord, direction, distance, number):
    new_state = copy.deepcopy(current_state)

    #if moving onto another white then form a stack
    white_list=[[white[1], white[2]] for white in current_state["white"]]
    f_coord = future_coord(coord, direction, distance)
    if f_coord in white_list:
        for white_member in new_state["white"]:
            if white_member[1:3] == coord:
                #if moving all of the stack at once then remove current stack
                if white_member[0] == number:
                    new_state["white"].remove(white_member)
                    break
                #if moving part of the stack then remove a number from the stack
                if white_member[0] > number:
                    white_member[0] -= number

        #then add the removed items onto existing stack at the destination
        for white_member in new_state["white"]:
            if white_member[1:3] == f_coord:
                white_member[0] += number
                return new_state

    #if not moving onto any other white
    for white_member in new_state["white"]:
        if white_member[1:3] == coord:
            #if moving all of the stack at once then just change the coord
            if number == white_member[0]:
                white_member[1] = f_coord[0]
                white_member[2] = f_coord[1]
            #if moving a part of the stack then add another stack to the detination
            if number < white_member[0]:
                white_member[0] -= number
                new_state["white"] += [[number] + f_coord]

    return new_state

#get the future coord after moving
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

#check if the move is valid
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

#count the number of members left in a team
def count_members(team):
    count = 0
    for member in team:
        count += member[0]
    return count

#add all possible moves to the queue
def add_stack_moves(queue, path, seen, state, member):
    new_state = {}
    directions = ["left", "right", "up", "down"]
    for number in range(1, member[0]+1):

        for distance in range(1, member[0]+1):
            for direction in directions:
                if movable_stack(state, member[1:3], direction, distance):
                    new_state = move_stack(state, member[1:3], direction, distance, number)

                    if new_state not in seen:
                        queue.append([heuristic(new_state), (path + [new_state])])
                        seen.append(new_state)
    new_state = boom(state, member[1:3], [])
    if not (new_state["white"] == 0 and new_state["black"] > 0):
        if new_state not in seen:
            queue.append([heuristic(new_state), (path + [new_state])])
            seen.append(new_state)

#compute the estimated cost to goal by counting number of black tokens left
def heuristic(state):
    result = count_members(state["black"])
    return result

def getmin(queue):
    minvalue = queue[0][0]
    minitem = queue[0]
    for i in queue:
        if i[0] < minvalue:
            minvalue = i[0]
            minitem = i
    result = copy.deepcopy(minitem)
    queue.remove(minitem)
    return result[1]

def bfs(start_state):
    queue = []
    queue.append([heuristic(start_state), [start_state]])
    seen = list([start_state])
    while queue:
        path = getmin(queue)
        current_state = path[-1]
        if len(current_state["black"]) == 0:
            return path
        for white_member in current_state["white"]:
            add_stack_moves(queue, path, seen, current_state, white_member)

def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        path = bfs(data)
        table = {}
        for key, value in data.items():
            for j in range(len(value)):
                table[(value[j][1], value[j][2])] = key[0] + ',' + str(value[j][0])

        for i in range(len(path)-1):
            if path[i + 1]['white'] != []:
                if len(path[i]['black']) == len(path[i + 1]['black']):
                    if len(path[i]['white']) == len(path[i + 1]['white']):
                        for j in range(len(path[i]['white'])):
                            if [path[i]['white'][j][1], path[i]['white'][j][2]] != [path[i + 1]['white'][j][1],path[i + 1]
                            ['white'][j][2]]:
                                print_move(path[i]['white'][j][0],path[i]['white'][j][1], path[i]['white'][j][2], path[i + 1]['white'][j][1],
                                    path[i + 1]['white'][j][2])
                    else:
                        coords_before=[]
                        coords_after=[]
                        for x in path[i]['white']:
                            coords_before.append([x[1],x[2]])
                            for y in path[i+1]['white']:
                                coords_after.append([y[1],y[2]])
                                if [x[1],x[2]] == [y[1],y[2]]:
                                    if x[0] < y[0]:
                                        stack_coord=[x[1],x[2]]
                                        num_move= x[0]
                                    if x[0] > y[0]:
                                        stack_coord = [x[1], x[2]]
                                        num_move=y[0]
                        for coord in coords_before:
                            if coord not in coords_after:
                                print_move(num_move,coord[0],coord[1],stack_coord[0],stack_coord[1])
                        for coord in coords_after:
                            if coord not in coords_before:
                                print_move(num_move, stack_coord[0], stack_coord[1], coord[0], coord[1])
                else:
                    coords_before = []
                    coords_after = []
                    for x in path[i]['white']:
                        coords_before.append([x[1], x[2]])
                    for y in path[i + 1]['white']:
                        coords_after.append([y[1], y[2]])
                    for coord in coords_before:
                        if coord not in coords_after:
                            print_boom(coord[0], coord[1])
            else:
                print_boom(path[i]['white'][0][1], path[i]['white'][0][2])


if __name__ == '__main__':
    main()
