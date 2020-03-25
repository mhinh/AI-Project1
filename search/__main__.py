import sys
import json

from search.util import print_move, print_boom, print_board

class Node:
    def _int_(self,state):
        self.state = state
        self.children =None

def move(direction,current_state):


def main():
    table ={}
    with open(sys.argv[1]) as file:
        data = json.load(file)
        print(data)
        for key,value in data.items():
            for i in range(len(value)):
                table[(value[i][1],value[i][2])] = key[0] + ',' + str(value[i][0])

        print_board(table)


    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()
