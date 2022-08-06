import io
import sys
import heapq
import numpy as np
from dataclasses import dataclass

data_path = "data/problem_15.txt"
data_path = "data/problem_15_test.txt"
# data_path = "data/problem_15_test_2.txt"

with open(data_path, "rb") as f:
    row_length = len(f.readline().strip())

data = np.genfromtxt(data_path, dtype="S").view(dtype=np.uint8).reshape(-1, row_length) - ord("0")
data = data.astype(int)

# print(data)

@dataclass
class GraphNode:
    y: int
    x: int

    # The cost of visiting this specific node
    cost: int

    # The minimum cost to get to the end from this node.This distance is the sum of all node
    # values along the cheapest path to the end.
    distance: int = 0

    # Whether the node has been discovered. Could use distance but it turns out the int comparison
    # of `distance == sys.maxsize` is significantly slower than using this flag. With the flag, the
    # initial distance value doesn't matter.
    discovered: bool = False

    # The closed set is the set of nodes for which we know with certainty the minimum distance to
    # the destination.
    is_closed: bool = False

    neighbors: list = None


    # For a dense graph, edges aren't defined explicitly, but we can easily compute them on demand
    def compute_neighbors(self, grid):
        self.neighbors = []
        # south
        if self.y + 1 < grid.shape[0]:
            self.neighbors.append(grid[self.y + 1, self.x])
        # north
        if self.y > 0:
            self.neighbors.append(grid[self.y - 1, self.x])
        # east
        if self.x + 1 < grid.shape[1]:
            self.neighbors.append(grid[self.y, self.x + 1])
        # west
        if self.x > 0:
            self.neighbors.append(grid[self.y, self.x - 1])

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        return self.distance < other.distance


def create_nodes(cost_grid):

    # Build a 2D array of nodes so we can easily look them up by coordinates
    node_grid = np.empty_like(cost_grid, dtype=object)
    for y in range(cost_grid.shape[0]):
        for x in range(cost_grid.shape[1]):
            node_grid[y, x] = GraphNode(y, x, cost_grid[y, x])

    for node in node_grid.flatten():
        node.compute_neighbors(node_grid)# = list(node.get_neighbors(node_grid))

    return node_grid


def print_dense_grid(array):
    for row in array:
        print("".join([str(x) for x in row]))


def print_grid_distances(node_grid):
    def format_node(node):
        if node.is_closed:
            return f"{node.distance} ".rjust(4)
        elif node.discovered:
            return f"{node.distance}*".rjust(4)
        else:
            return "  ? "

    print("   |" + "".join([str(i).rjust(4) for i in range(node_grid.shape[1])]))
    print("---+-" + ("-" * (5 * node_grid.shape[1])))
    for i, node_row in enumerate(node_grid):
        print(str(i).ljust(3) + "| " + "".join([format_node(node) for node in node_row]))


def print_path(node_grid, path):
    if path is None:
        print("Dangit")
        return

    def format_cost(cost):
        if cost < 0:
            return f"[{str(-cost)}]".rjust(4)
        else:
            return f" {str(cost)} ".rjust(4)

    path_grid = np.zeros_like(node_grid, dtype=np.int32)
    # for node in node_grid.flatten():
    path_grid[...] = np.array([node.cost for node in node_grid.flatten()]).reshape(path_grid.shape)

    for node in path:
        path_grid[node.y, node.x] = -node.cost

    print("   |" + "".join([str(i).rjust(4) for i in range(path_grid.shape[1])]))
    print("---+-" + ("-" * (4 * path_grid.shape[1])))
    for i, cost_row in enumerate(path_grid):
        print(str(i).ljust(3) + "| " + "".join([format_cost(cost) for cost in cost_row]))


def compute_distances(node_grid, start_node, end_node):
    # The distance for the destination is simply the cost of the end node itself.
    end_node.discovered = True
    end_node.distance = end_node.cost

    # The initial open set is simply the starting node.
    open_set = [end_node]
    heapq.heapify(open_set)

    # print(f"Initial state:")
    # print_grid_distances(node_grid)

    for i in range(1000000):
        if len(open_set) == 0:
            print("Ran out of nodes to explore :)")
            break

        current_node = heapq.heappop(open_set)

        for neighbor in current_node.neighbors:
            # if neighbor.is_closed:
            #     continue

            if not neighbor.discovered:
            # if neighbor.distance == sys.maxsize:
                neighbor.discovered = True
                neighbor.distance = neighbor.cost + current_node.distance
                heapq.heappush(open_set, neighbor)
            else:
                distance_via_neighbor = current_node.cost + neighbor.distance
                if distance_via_neighbor < current_node.distance:
                    current_node.distance = distance_via_neighbor

        if current_node is start_node: # and current_node.is_open:
            print(f"Path found! iteration: {i}, distance: {current_node.distance}")
            return

        # we would sort open_set here but the min heap structure magically keeps it sorted somehow
        # open_set.sort(key=lambda node: node.distance)

        # print(f"Iteration {i}, open set size = {len(open_set)}:")
        # print_grid_distances(node_grid)


def find_optimal_path(node_grid, start_node, end_node):
    path = [start_node]
    current_node = start_node

    for i in range(10000):
        # current_node = min(current_node.get_neighbors(node_grid), key=lambda node: node.distance)
        current_node = min(current_node.neighbors, key=lambda node: node.distance)
        path.append(current_node)
        if current_node is end_node:
            return path


    return None

# part 1
node_grid = create_nodes(data)
start_node = node_grid[0, 0]
end_node = node_grid[-1, -1]
compute_distances(node_grid, start_node, end_node)
optimal_path = find_optimal_path(node_grid, start_node, end_node)
print_path(node_grid, optimal_path)
print(f"Part 1 solution: {sum(node.cost for node in optimal_path[1:])}")
# sys.exit()

# part 2
tile_number = 5
data_tiled = np.tile(data, (tile_number, tile_number))

# This magically generates a matrix of dimension (H * tile_number, W * tile_number)
# where each (H, W) sub-matrix is all one value, which increments by 1 as you go right and down.
# e.g. if H = 3, W = 4, and tile_number = 3:

# [[ 0, 0, 0, 0,   1, 1, 1, 1,   2, 2, 2, 2 ],
#  [ 0, 0, 0, 0,   1, 1, 1, 1,   2, 2, 2, 2 ],
#  [ 0, 0, 0, 0,   1, 1, 1, 1,   2, 2, 2, 2 ],

#  [ 1, 1, 1, 1,   2, 2, 2, 2,   3, 3, 3, 3 ],
#  [ 1, 1, 1, 1,   2, 2, 2, 2,   3, 3, 3, 3 ],
#  [ 1, 1, 1, 1,   2, 2, 2, 2,   3, 3, 3, 3 ],

#  [ 2, 2, 2, 2,   3, 3, 3, 3,   4, 4, 4, 4 ],
#  [ 2, 2, 2, 2,   3, 3, 3, 3,   4, 4, 4, 4 ],
#  [ 2, 2, 2, 2,   3, 3, 3, 3,   4, 4, 4, 4 ]]

height_offsets = (
    np.mgrid[:tile_number, :tile_number]
    .sum(axis=0)
    .repeat(data.shape[0], axis=0)
    .repeat(data.shape[1], axis=1)
)

# this handles the weirdo base-9 wrapping, i.e. 7 => 8 => 9 => 1 => 2
data_tiled = (((data_tiled - 1) + height_offsets) % 9) + 1
# print_dense_grid(data_tiled)

node_grid = create_nodes(data_tiled)
start_node = node_grid[0, 0]
end_node = node_grid[-1, -1]
compute_distances(node_grid, start_node, end_node)
optimal_path = find_optimal_path(node_grid, start_node, end_node)
# print_path(node_grid, optimal_path)

print(f"Part 2 solution: {sum(node.cost for node in optimal_path[1:])}")
