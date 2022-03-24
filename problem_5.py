import io
import numpy as np

# data_path = "data/problem_5.txt"
data_path = "data/problem_5_test.txt"

with open(data_path, "r") as f:
    better_file = io.StringIO(f.read().replace(" -> ", ","))
    lines = np.genfromtxt(better_file, dtype=np.int32, delimiter=",")

max_x = np.max(lines[:, [0, 2]])
max_y = np.max(lines[:, [1, 3]])

def render_lines(diagonals=False):
    accumulator = np.zeros((max_y + 1, max_x + 1), dtype=np.int32)
    for start_x, start_y, end_x, end_y in lines:
        x_dir = 1 if start_x <= end_x else -1
        y_dir = 1 if start_y <= end_y else -1

        if start_x == end_x:
            accumulator[start_y:end_y + y_dir:y_dir, start_x] += 1
        elif start_y == end_y:
            accumulator[start_y, start_x:end_x + x_dir:x_dir] += 1
        elif (end_x - start_x) * x_dir == (end_y - start_y) * y_dir:
            if diagonals is True:
                accumulator[np.arange(start_y, end_y + y_dir, y_dir), np.arange(start_x, end_x + x_dir, x_dir)] += 1
        else:
            raise Exception(f"durrr {start_x, start_y, end_x, end_y}")

    return accumulator

# part 1
print(f"Part 1 solution: {np.sum(render_lines() > 1)}")

# part 2
print(f"Part 2 solution: {np.sum(render_lines(diagonals=True) > 1)}")
