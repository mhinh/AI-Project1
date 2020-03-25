import sys
import json

from search.util import print_move, print_boom, print_board

class Node:
  def __init__(self, state):
    self.state = state
    self.children = None





def move(white_order,direction,current_state):
    if direction == 'LEFT'and current_state.state['white'][white_order][1] > 0:
        current_state.state['white'][white_order][1] -=1
    elif direction == 'RIGHT'and current_state.state['white'][white_order][1] < 7:
        current_state.state['white'][white_order][1] +=1
    elif direction == 'UP' and current_state.state['white'][white_order][2] < 7:
        current_state.state['white'][white_order][2] +=1
    elif direction =='DOWN' and current_state.state['white'][white_order][2] > 0:
        current_state.state['white'][white_order][2] -=1

def main():
    table ={}
    init_table={}
    with open(sys.argv[1]) as file:
        data = json.load(file)
        print(data)

        for key,value in data.items():
            for i in range(len(value)):
                init_table[(value[i][1],value[i][2])] = key[0] + ',' + str(value[i][0])

        print_board(init_table)

        start_state = Node(data)
        move(0,'DOWN',start_state)
        move(0, 'DOWN', start_state)
        move(0, 'DOWN', start_state)
        move(0, 'DOWN', start_state)

        print(start_state.state)

        for key,value in start_state.state.items():
            for i in range(len(value)):
                table[(value[i][1],value[i][2])] = key[0] + ',' + str(value[i][0])

        print_board(table)



    # TODO: find and print winning action sequence



if __name__ == '__main__':
    main()
