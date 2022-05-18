from code_there_is_no_spoon_2 import Node, GameEngine
import sys

ge = GameEngine()
ge.width = 5
ge.height = 14

lines = [
    ['2', '2', '2', '2', '1'],
    ['2', '.', '.', '.', '.'],
    ['2', '.', '.', '.', '.'],
    ['2', '.', '.', '.', '.'],
    ['2', '.', '.', '.', '.'],
    ['2', '2', '3', '2', '1'],
    ['.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.'],
    ['2', '2', '3', '2', '1'],
    ['2', '.', '.', '.', '.'],
    ['2', '.', '.', '.', '.'],
    ['2', '.', '1', '3', '1'],
    ['2', '.', '.', '2', '.'],
    ['2', '2', '2', '2', '.']
]

for y in range(ge.height):
    line = lines[y] #list(input())  # width characters, each either a number or a '.'
    print(line,file=sys.stderr,flush=True)
    left_neighbor_index = None
    for x in range(ge.width):
        if line[x] == '.':
            continue
        node = Node(int(line[x]),x,y)
        if left_neighbor_index is not None:
            node.neighbors.add(ge.nodes[left_neighbor_index])
        ge.nodes.append(node)

        n = len(ge.nodes)
        left_neighbor_index = n-1
        if n > 1:
            #left/right logic
            if ge.nodes[-2].y == y:# and not (nodes[-2].power == nodes[i].power == 1):
                ge.nodes[-2].neighbors.add(ge.nodes[n-1])

            for i in range(n-2,-1,-1):
                if ge.nodes[i].x == x:# and not(nodes[n-1].power == nodes[i].power == 1):
                    ge.nodes[i].neighbors.add(ge.nodes[n-1])
                    ge.nodes[-1].neighbors.add(ge.nodes[i])
                    break
    
    #def guessing_time():
        # sort nodes by number of neighbors unsolved and bridges remaining
        # try a bridge and do the logic
        # roll it back if it does not work
        #guessing_nodes = copy.deepcopy(nodes)

for _ in range(8):
    were_bridges_added = True
    bridge_count = sum(len(x) for x in ge.bridges.values())
    while were_bridges_added:
        ge.do_easy_logic()
        ge.hard_logic()
        curr_count = sum(len(x) for x in ge.bridges.values())
        if bridge_count == curr_count:
            were_bridges_added = False
        else:
            bridge_count = curr_count
    print("i guessed",file=sys.stderr,flush=True)
    ge.guess_a_bridge(8)