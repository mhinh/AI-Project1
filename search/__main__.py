import sys
import json

from search.util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence

def boom(current_state, coord):
    new_state = current_state.copy()
    xmin = coord[1]-1
    xmax = coord[1]+2
    ymin = coord[2]-1
    ymax = coord[2]+2
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            new_state = boom(new_state, [x,y])
    for team in new_state:
        for member in team:
            if member[1:3] == coord:
                del member
    return new_state



if __name__ == '__main__':
    main()
