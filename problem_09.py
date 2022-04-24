import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

data_path = "data/problem_09.txt"
# data_path = "data/problem_09_test.txt"

with open(data_path, "rb") as f:
    row_length = len(f.readline().strip())

data = np.genfromtxt(data_path, dtype="S").view(dtype=np.uint8).reshape(-1, row_length) - ord("0")
data = data.astype(int)
# print(data.shape)
# print(data)

# part 1

x_diffs = np.diff(data, axis=1, prepend=1000, append=1000)
y_diffs = np.diff(data, axis=0, prepend=1000, append=1000)

is_x_minima = np.diff(np.sign(x_diffs), axis=1) == 2
is_y_minima = np.diff(np.sign(y_diffs), axis=0) == 2

is_minimum = is_x_minima & is_y_minima

height_at_minima = data[is_minimum]
# print(height_at_minima)
print(f"Part 1 solution: {np.sum(height_at_minima + 1)}")


# part 2
minima_y_coords, minima_x_coords = np.where(is_minimum)
minima_ids = np.arange(len(minima_x_coords))

basin_map = np.full_like(data, -1)
basin_map[minima_y_coords, minima_x_coords] = minima_ids


def get_neighbors(y, x):
    # return a list of neighboring cells that aren't a boundary
    if y + 1 < data.shape[0]:
        yield y + 1, x

    if y > 0:
        yield y - 1, x

    if x + 1 < data.shape[1]:
        yield y, x + 1

    if x > 0:
        yield y, x - 1

# dynamic list of points at the edge of the known basin
open_set = list(zip(minima_y_coords, minima_x_coords))
basin_sizes = np.ones(len(open_set), dtype=int)

while open_set:
    y, x = open_set.pop()
    basin_id = basin_map[y, x]
    for neighbor_y, neighbor_x in get_neighbors(y, x):
        if data[neighbor_y, neighbor_x] == 9:
            continue
        if basin_map[neighbor_y, neighbor_x] == -1:
            basin_map[neighbor_y, neighbor_x] = basin_id
            basin_sizes[basin_id] += 1
            open_set.append((neighbor_y, neighbor_x))

basin_sizes.sort()

print(f"Part 2 solution: {np.product(basin_sizes[-3:])}")

