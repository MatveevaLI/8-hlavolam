import heapq
import os
import time

src_heap = []
dst_heap = []

src_created = []
dst_created = []

src_visited = []
dst_visited = []

number_src = 0
number_dst = 0

created = []


# trieda reprezentuje jeden uzol v strome
# obsahuje aktualny stav, predchodcu, hlbku,
# cislo vytvoreneho uzla, a operaciu pre vznik tohto uzla
class Node:
    def __init__(self, p_state, previous, depth, number, opr):
        self.state = p_state
        self.previous = previous
        self.depth = depth
        self.number = number
        self.opr = opr

    # metoda podla ktorej sa porovnavaju uzly v heap
    def __lt__(self, other):
        return self.number < other.number


# Funcie operatorov pre pohyb vlavo, vpravo, hore, dole

def right(state, x_pos, y_pos):
    temp = state[x_pos][y_pos + 1]
    state[x_pos][y_pos + 1] = state[x_pos][y_pos]
    state[x_pos][y_pos] = temp


def left(state, x_pos, y_pos):
    temp = state[x_pos][y_pos - 1]
    state[x_pos][y_pos - 1] = state[x_pos][y_pos]
    state[x_pos][y_pos] = temp


def up(state, x_pos, y_pos):
    temp = state[x_pos - 1][y_pos]
    state[x_pos - 1][y_pos] = state[x_pos][y_pos]
    state[x_pos][y_pos] = temp


def down(state, x_pos, y_pos):
    temp = state[x_pos + 1][y_pos]
    state[x_pos + 1][y_pos] = state[x_pos][y_pos]
    state[x_pos][y_pos] = temp


# funkcia vrati prazdne polizko
def find_blank(node):
    for x in range(0, row_max):
        for y in range(0, column_max):
            if node[x][y] == 0:
                return x, y


# Zisti ci je dany stav uz existuje
def is_exists(node, list_node):
    if node in list_node:
        return True
    else:
        return False


# Zisti ci sa pretinaju stavy
def is_intersecting(src_node, created_nodes):
    for create_node in range(len(created_nodes)):
        if created_nodes[create_node].state == src_node:
            return create_node
    return -1


# Vypise stav hlavolamu
def print_puzzle(node):
    for x in range(0, row_max):
        for y in range(0, column_max):
            print(node[x][y], end=" ")
        print()


# Algoritmus obojsmerneho hladania
def bidirectional_search(root, direction):
    global number_src
    global number_dst

    if direction == "forward":
        src_visited.append(root)
        x_pos, y_pos = find_blank(root.state)

        # LEFT
        if y_pos - 1 >= 0:
            new = [list(x) for x in root.state]
            left(new, x_pos, y_pos)
            if not is_exists(new, src_created):
                src_created.append(new)
                number_src += 1
                heapq.heappush(src_heap, Node(new, root, root.depth + 1, number_src, "left"))

        # RIGHT
        if y_pos + 1 < column_max:
            new = [list(x) for x in root.state]
            right(new, x_pos, y_pos)
            if not is_exists(new, src_created):
                src_created.append(new)
                number_src += 1
                heapq.heappush(src_heap, Node(new, root, root.depth + 1, number_src, "right"))
        # UP
        if x_pos - 1 >= 0:
            new = [list(x) for x in root.state]
            up(new, x_pos, y_pos)
            if not is_exists(new, src_created):
                src_created.append(new)
                number_src += 1
                heapq.heappush(src_heap, Node(new, root, root.depth + 1, number_src, "up"))

        # DOWN
        if x_pos + 1 < row_max:
            new = [list(x) for x in root.state]
            down(new, x_pos, y_pos)
            if not is_exists(new, src_created):
                src_created.append(new)
                number_src += 1
                heapq.heappush(src_heap, Node(new, root, root.depth + 1, number_src, "down"))

    elif direction == "backward":
        dst_visited.append(root)
        x_pos, y_pos = find_blank(root.state)

        # LEFT
        if y_pos - 1 >= 0:
            new = [list(x) for x in root.state]
            left(new, x_pos, y_pos)
            if not is_exists(new, dst_created):
                dst_created.append(new)
                number_dst += 1
                heapq.heappush(dst_heap, Node(new, root, root.depth + 1, number_dst, "left"))

        # RIGHT
        if y_pos + 1 < column_max:
            new = [list(x) for x in root.state]
            right(new, x_pos, y_pos)
            if not is_exists(new, dst_created):
                dst_created.append(new)
                number_dst += 1
                heapq.heappush(dst_heap, Node(new, root, root.depth + 1, number_dst, "right"))

        # UP
        if x_pos - 1 >= 0:
            new = [list(x) for x in root.state]
            up(new, x_pos, y_pos)
            if not is_exists(new, dst_created):
                dst_created.append(new)
                number_dst += 1
                heapq.heappush(dst_heap, Node(new, root, root.depth + 1, number_dst, "up"))

        # DOWN
        if x_pos + 1 < row_max:
            new = [list(x) for x in root.state]
            down(new, x_pos, y_pos)
            if not is_exists(new, dst_created):
                dst_created.append(new)
                number_dst += 1
                heapq.heappush(dst_heap, Node(new, root, root.depth + 1, number_dst, "down"))


# Vypise prvu polovicu cesty
def print_path_f(path_f):
    if path_f.previous is None:
        return
    else:
        print_path_f(path_f.previous)
        print(path_f.opr, end="")
        print(" -> ", end="")


# Vypise druhu polovicu cesty
def print_path_s(path_s):
    if path_s.previous is None:
        return
    else:
        if path_s.opr == "up":
            print("down", end="")
        if path_s.opr == "down":
            print("up", end="")
        if path_s.opr == "right":
            print("left", end="")
        if path_s.opr == "left":
            print("right", end="")
        if path_s.depth != 1:
            print(" -> ", end="")
        print_path_s(path_s.previous)


# Funkcia sluzi na volanie obojsmerneho hladania kym sa nepretinaju uzly
def find_path():
    root_src = Node(position_start, None, 0, 1, "")
    root_dst = Node(position_finish, None, 0, 1, "")

    src_created.append(root_src.state)
    dst_created.append(root_dst.state)
    print("Start position:")
    print_puzzle(root_src.state)
    print()

    print("Finish position:")
    print_puzzle(root_dst.state)
    print()
    possible = True
    solvable = 0

    steps_number = 0

    while possible:
        bidirectional_search(root_src, 'forward')
        bidirectional_search(root_dst, 'backward')
        steps_number += 1

        # ak sa pretinaju zo strany startovacieho stavu
        act_node_src = is_intersecting(src_visited[0].state, created)
        if act_node_src >= 0:
            print("Path: ", end="\n")
            f_path = root_src
            print_path_f(f_path)
            print_path_s(created[act_node_src])
            print()
            possible = False
            break
        elif act_node_src == -1:
            created.append(src_visited[0])
            src_visited.pop(0)

        # Ak sa pretinaju zo strany koncoveho stavu
        act_node_dst = is_intersecting(dst_visited[0].state, created)
        if act_node_dst >= 0:
            print("Path: ", end="\n")
            f_path = created[act_node_dst]
            print_path_f(f_path)
            s_path = root_dst
            print_path_s(s_path)
            print()
            possible = False
            break
        elif act_node_dst == -1:
            created.append(dst_visited[0])
            dst_visited.pop(0)

        # nastavit dalsi uzol pre koncovy a pociatocne stavy
        root_src = heapq.heappop(src_heap)
        root_dst = heapq.heappop(dst_heap)
        if (steps_number % 1000 == 0):
            print("Pocet krokov: ", steps_number)

        if steps_number > 1000000:
            print("Dosiahnut maximalny pocet krokov.")
            possible = False
            break

    print("Pocet krokov: ", steps_number)
    print("Pocet vytvorenych uzlov od pociatocneho a koncoveho stavov: ", number_src, number_dst)


# precita subor zo vstupom a nacita hlavolam
def load_puzzle():
    filename = input("Zadajte meno suboru: ")
    while not os.path.exists(filename):
        print("Subor neexistuje. Skuste este raz\n")
        filename = input("Zadajte meno suboru: ")

    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]

    global column_max, row_max
    column_max = int(lines[0])
    row_max = int(lines[1])
    src = 0

    for line in range(len(lines)):
        lines[line] = lines[line].split()

    global position_start, position_finish
    position_start = [[] for i in range(row_max)]
    position_finish = [[] for i in range(row_max)]

    # nacita hlavolam
    for line in range(2, len(lines)):
        if src == 0:
            z = 0
            for x in range(0, row_max):
                for y in range(0, column_max):
                    num = int(lines[line][z])
                    z += 1
                    position_start[x].append(num)
            src = 1
        else:
            z = 0
            for x in range(0, row_max):
                for y in range(0, column_max):
                    num = int(lines[line][z])
                    z += 1
                    position_finish[x].append(num)


load_puzzle()
timer = 0.0
start = time.time()

find_path()

end = time.time()
print("Cas: ", end - start)
