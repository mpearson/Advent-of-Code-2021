import sys
import numpy as np
# from collections import namedtuple
from dataclasses import dataclass
import io

data_path = "data/problem_15.txt"
data_path = "data/problem_15_test.txt"

with open(data_path, "rb") as f:
    row_length = len(f.readline().strip())

txt = """
1199999999
9199111119
9199199919
9199199919
9111199919
9199199919
9199199919
9199199919
9111199919
9999999911
"""

# data = np.genfromtxt(data_path, dtype="S").view(dtype=np.uint8).reshape(-1, row_length) - ord("0")
data = np.genfromtxt(io.StringIO(txt), dtype="S").view(dtype=np.uint8).reshape(-1, row_length) - ord("0")
data = data.astype(int)


print(data)

# data[...] = 1


@dataclass
class Node:
    y: int
    x: int

    # The cost of visiting this specific node
    cost: int

    # The minimum cost to get to the end from this node.This distance is the sum of all node
    # values along the cheapest path to the end.
    distance: int = 999 #sys.maxsize

    # The open set is the set of nodes which have been discovered via adjacency to the closed set,
    # but for which we don't yet know the minimum distance.
    is_open: bool = False

    # The closed set is the set of nodes for which we know with certainty the minimum distance to
    # the destination.
    is_closed: bool = False


    # For a dense graph, edges aren't defined explicitly, but we can easily compute them on demand
    def get_neighbors(self, grid):
        # south
        if self.y + 1 < grid.shape[0]:
            yield grid[self.y + 1, self.x]
        # north
        if self.y > 0:
            yield grid[self.y - 1, self.x]
        # east
        if self.x + 1 < grid.shape[1]:
            yield grid[self.y, self.x + 1]
        # west
        if self.x > 0:
            yield grid[self.y, self.x - 1]


# Build a 2D array of nodes so we can easily look them up by coordinates
node_grid = np.empty_like(data, dtype=object)
for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        node_grid[y, x] = Node(y, x, data[y, x])


print(node_grid[5, 3])

# sys.exit()


def print_grid_distances(node_grid):
    def format_node(node):
        # dist = str(self.distance).rjust(2)
        if node.is_closed:
            return f"{node.distance} ".rjust(5)
        elif node.is_open:
            return f"{node.distance}*".rjust(5)
        else:
            return "   ? "

    print("   |" + " ".join([str(i).rjust(5) for i in range(node_grid.shape[1])]))
    print("---+-" + ("-" * (6 * node_grid.shape[1])))
    for i, node_row in enumerate(node_grid):
        print(str(i).ljust(3) + "| " + " ".join([format_node(node) for node in node_row]))


def print_path(node_grid, path):
    def format_cost(cost):
        if cost < 0:
            return f"[{str(-cost)}]".rjust(5)
        else:
            return f" {str(cost)} ".rjust(5)

    path_grid = np.zeros_like(node_grid, dtype=np.int32)
    # for node in node_grid.flatten():
    path_grid[...] = np.array([node.cost for node in node_grid.flatten()]).reshape(path_grid.shape)

    for node in path:
        path_grid[node.y, node.x] = -node.cost

    print("   |" + " ".join([str(i).rjust(5) for i in range(path_grid.shape[1])]))
    print("---+-" + ("-" * (6 * path_grid.shape[1])))
    for i, cost_row in enumerate(path_grid):
        print(str(i).ljust(3) + "| " + " ".join([format_cost(cost) for cost in cost_row]))


def compute_distances(node_grid, start_node, end_node):
    # We know the minimum distance for the destination is simply the cost of the end node itself.
    end_node.distance = end_node.cost
    # We know the minimum cost for the destination so it's closed.
    end_node.is_closed = True

    # The initial open set is simply the immediate neighborhood of the end node.
    open_set = list(end_node.get_neighbors(node_grid))
    for node in open_set:
        node.is_open = True
        node.distance = end_node.cost + node.cost


    for i in range(1000):
        if len(open_set) == 0:
            print("Ran out of nodes to explore :)")
            break

        new_open_nodes = []

        for node in open_set:
            # if node is start_node and node.is_open:
            #     print(f"Shortest distance: {node.distance}")
            #     break
            distance_changed = False
            for neighbor in node.get_neighbors(node_grid):
                if neighbor.is_closed or neighbor.is_open:
                    new_cost = node.cost + neighbor.distance
                    if new_cost < node.distance:
                        distance_changed = True
                        node.distance = new_cost
                elif not neighbor.is_open:
                    new_open_nodes.append(neighbor)
                    neighbor.is_open = True
                    # neighbor.distance = neighbor.cost + node.distance

            if not distance_changed:
                node.is_open = False
                node.is_closed = True

        open_set = [node for node in open_set if not node.is_closed] + new_open_nodes


        print(f"Iteration {i}, open set size = {len(open_set)}:")
        print_grid_distances(node_grid)


def find_optimal_path(node_grid, start_node, end_node):
    path = [start_node]
    current_node = start_node

    for i in range(1000):
        current_node = min(current_node.get_neighbors(node_grid), key=lambda node: node.distance)
        path.append(current_node)
        if current_node is end_node:
            return path

    return None



print(f"Initial state:")
print_grid_distances(node_grid)

start_node = node_grid[0, 0]
end_node = node_grid[-1, -1]

compute_distances(node_grid, start_node, end_node)

optimal_path = find_optimal_path(node_grid, start_node, end_node)

print_path(node_grid, optimal_path)


# print(f"node at (0, 0): {node_grid[0, 0]}")
# print(f"node at (8, 8): {node_grid[8, 8]}")
# print("neighbors of (8, 8):")
# for n in get_neighbors(node_grid[8, 8]):
#     print(n)
# print(f"node at (7, 8): {node_grid[7, 8]}")

# part 1
print(f"Part 1 solution: {None}")

# part 2
print(f"Part 2 solution: {None}")

