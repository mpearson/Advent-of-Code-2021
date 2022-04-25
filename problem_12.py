
import numpy as np

data_path = "data/problem_12.txt"
# data_path = "data/problem_12_test.txt"

class Node:
    def __init__(self, name):
        self.name = name
        self.big = ord(self.name[0]) < ord("a")
        self.visited = False
        self.neighbors = []

node_dict = {}

with open(data_path, "r") as f:
    for line in f:
        name_a, name_b = line.rstrip().split("-")

        node_a = node_dict.get(name_a)
        if node_a is None:
            node_a = node_dict[name_a] = Node(name_a)

        node_b = node_dict.get(name_b)
        if node_b is None:
            node_b = node_dict[name_b] = Node(name_b)

        node_a.neighbors.append(node_b)
        node_b.neighbors.append(node_a)

start_node = node_dict["start"]
end_node = node_dict["end"]

# for node in node_dict.values():
#     node_type = "big" if node.big else "small"
#     print(f"{node.name} ({node_type}) -> {[n.name for n in node.neighbors]}")

# part 1
def explore(current_node, prior_path):
    current_path = [*prior_path, current_node]
    if current_node is end_node:
        yield current_path
        return

    for neighbor in current_node.neighbors:
        if neighbor is start_node or (not neighbor.big and neighbor in prior_path):
            continue
        else:
            yield from explore(neighbor, current_path)

paths = list(explore(start_node, []))
# for path in paths:
#     print([n.name for n in path])

print(f"Part 1 solution: {len(paths)}")

# part 2
def explore_with_one_cheat(current_node, prior_path, cheat_used):
    current_path = [*prior_path, current_node]
    if current_node is end_node:
        yield current_path
        return

    for neighbor in current_node.neighbors:
        if neighbor is start_node:
            continue
        if not neighbor.big and neighbor in prior_path:
            if cheat_used:
                continue
            else:
                yield from explore_with_one_cheat(neighbor, current_path, True)
        else:
            yield from explore_with_one_cheat(neighbor, current_path, cheat_used)

paths = list(explore_with_one_cheat(start_node, [], False))
print(f"Part 2 solution: {len(paths)}")

