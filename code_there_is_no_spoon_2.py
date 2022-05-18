from collections import defaultdict, deque
import sys
import math
import copy

class Node:
    def __init__(self, power, x, y) -> None:
        self.x = x
        self.y = y
        self.power = power
        self.neighbors = set()
        self.bridges = 0
    
    def __str__(self) -> str:
        return "x:{},y:{},power:{}".format(self.x,self.y,self.power)
    
    def is_solved(self):
        return self.bridges == self.power

    def remaining(self):
        return self.power - self.bridges

class GameEngine:
    def __init__(self) -> None:
        self.nodes = list()
        self.bridges = defaultdict(list)
        self.width = 0
        self.height = 0

    def add_bridge(self, base_node,base_neighbor,bridges_to_add=1):
        x0 = base_node.x
        y0 = base_node.y
        x1 = base_neighbor.x
        y1 = base_neighbor.y
        is_vertical = x0-x1 == 0
        for _ in range(bridges_to_add):
            self.bridges[id(base_node)].append(id(base_neighbor))
            self.bridges[id(base_neighbor)].append(id(base_node))
        for node in self.nodes:
            if node == base_node:
                continue
            for neighbor in [x for x in node.neighbors]:
                if neighbor == base_neighbor:
                    continue
                if is_vertical:
                    t1 = (y0 < node.y < y1) or (y1 < node.y < y0)
                    t2 = (y0 < neighbor.y < y1) or (y1 < neighbor.y < y0)
                    t3 = (node.x > x0 and neighbor.x < x0) or (node.x < x0 and neighbor.x > x0)
                    if t1 and t2 and t3:
                        node.neighbors.remove(neighbor)
                        neighbor.neighbors.remove(node)
                else: # it is horizontal
                    t1 = (x0 < node.x < x1) or (x1 < node.x < x0)
                    t2 = (x0 < neighbor.x < x1) or (x1 < neighbor.x < x0)
                    t3 = (node.y > y0 and neighbor.y < y0) or (node.y < y0 and neighbor.y > y0)
                    if t1 and t2 and t3:
                        node.neighbors.remove(neighbor)
                        neighbor.neighbors.remove(node)

    def do_easy_logic(self):
        self.nodes.sort(key=lambda x:len(x.neighbors))
        work_done = True
        while work_done:
            work_done = False
            for node in self.nodes:
                #print("working node:{}".format(node),file=sys.stderr,flush=True)
                if node.is_solved():
                    continue
                if node.power == 1 and len(self.nodes) > 2:
                    tester = sum(1 for x in node.neighbors if not x.is_solved() and x.power > 1)
                else:
                    tester = sum(1 for x in node.neighbors if not x.is_solved())
                remaining = node.power - node.bridges
                #print("x:{},y:{},remaining:{},available:{}".format(node.x,node.y,remaining,available),file=sys.stderr,flush=True)
                if tester > 1:
                    # if the number of unsolved neighbors equals half of the number of bridges left
                    # you can guarentee each neighbor gets two bridges
                    bridges = None
                    if remaining % 2 == 0 and remaining / 2 == tester:
                        bridges = 2
                    # if the remaining is one less than that you can guarentee
                    # each neighbor gets one bridge
                    elif (remaining + 1) % 2 == 0 and (remaining + 1) / 2 == tester:
                        bridges = 1
                    if bridges:
                        for neighbor in node.neighbors:
                            if neighbor.is_solved():
                                continue
                            work_done = True
                            node.bridges += bridges
                            neighbor.bridges += bridges
                            nx = neighbor.x
                            ny = neighbor.y
                            self.add_bridge(node,neighbor,bridges)
                            print("{} {} {} {} {}".format(node.x,node.y,nx,ny, bridges),flush=True)
                    continue
                for i in range(remaining):
                    for neighbor in node.neighbors:
                        #print("neighbor:{}".format(neighbor),file=sys.stderr,flush=True)
                        if neighbor.is_solved():
                            continue
                        if node.power == 1 and len(self.nodes) > 2 and neighbor.power == 1:
                            continue
                        work_done = True
                        node.bridges += 1
                        neighbor.bridges += 1
                        nx = neighbor.x
                        ny = neighbor.y
                        self.add_bridge(node,neighbor)#.x,node.y,nx,ny)
                        #bridges.append((node.x,node.y,nx,ny))
                        print("{} {} {} {} 1".format(node.x,node.y,nx,ny),flush=True)

    def hard_logic(self):
        for node in self.nodes:
            if node.is_solved():
                continue
            remaining = node.power - node.bridges
            available = 0
            for neighbor in node.neighbors:
                if neighbor.is_solved():
                    continue
                if self.bridges[id(node)].count(id(neighbor)) == 1:
                    available += 1
                elif (neighbor.power - neighbor.bridges) == 1:
                    available += 1
                else:
                    available += 2
            #available = sum(min(2,x.power-x.bridges) - bridges[id(node)].count(id(x)) for x in node.neighbors if not x.is_solved())
            if remaining == available:
                print("x:{},y:{},here".format(node.x,node.y),file=sys.stderr,flush=True)
                for neighbor in node.neighbors:
                    if neighbor.is_solved():
                        continue
                    node.bridges += 1
                    neighbor.bridges += 1
                    nx = neighbor.x
                    ny = neighbor.y    
                    self.add_bridge(node,neighbor)
                    print("{} {} {} {} 1".format(node.x,node.y,nx,ny),flush=True)

    def guess_a_bridge(self,n):
        for node in self.nodes:
            if node.is_solved():
                continue
            remaining = node.power - node.bridges
            
            if remaining > n:
                continue

            available = 0
            unsolved_neighbors = []
            closest_neighbor_dist = 9999999
            closest_neighbor = None
            for neighbor in node.neighbors:
                if neighbor.is_solved():
                    continue
                dist = math.hypot(node.x-neighbor.x, node.y-neighbor.y)
                if dist < closest_neighbor_dist:
                    closest_neighbor_dist = dist
                    closest_neighbor = neighbor
                unsolved_neighbors.append(neighbor)
                if self.bridges[id(node)].count(id(neighbor)) == 1:
                    available += 1
                elif (neighbor.power - neighbor.bridges) == 1:
                    available += 1
                else:
                    available += 2
            
            if available > n+1:
                continue

            node.bridges += 1
            closest_neighbor.bridges += 1
            nx = closest_neighbor.x
            ny = closest_neighbor.y
            self.add_bridge(node,closest_neighbor)
            #unsolved_neighbors[0].bridges += 1
            #nx = unsolved_neighbors[0].x
            #ny = unsolved_neighbors[0].y    
            #self.add_bridge(node,unsolved_neighbors[0])
            print("{} {} {} {} 1".format(node.x,node.y,nx,ny),flush=True)

            break



ge = GameEngine()
ge.width = int(input())  # the number of cells on the X axis
ge.height = int(input())  # the number of cells on the Y axis
#print("w:{},h:{}".format(ge.width,ge.height))
lines = [
    ['3', '.', '4', '.', '6', '.', '2', '.'],
    ['.', '1', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '2', '.', '5', '.', '.', '2'],
    ['1', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '1', '.', '.', '.', '.', '.'],
    ['.', '3', '.', '.', '5', '2', '.', '3'],
    ['.', '2', '.', '1', '7', '.', '.', '4'],
    ['.', '4', '.', '.', '5', '1', '.', '2']
]

# create initial nodes with nearest neighbors in four directions
for y in range(ge.height):
    line = list(input())  # width characters, each either a number or a '.'
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

for _ in range(18):
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


for node in ge.nodes:
    print("x:{},y:{},bridges:{}".format(node.x, node.y, ge.bridges[id(node)]),file=sys.stderr,flush=True)