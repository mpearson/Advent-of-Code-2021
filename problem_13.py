
import numpy as np

data_path = "data/problem_13.txt"
# data_path = "data/problem_13_test.txt"

initial_state = []
folds = []
with open(data_path, "r") as f:
    for line in f:
        line = line.rstrip()
        if line:
            if line[0] == "f":
                direction, value = line.rsplit(" ", 1)[-1].split("=")
                folds.append((int(direction == "x"), int(value)))
            else:
                dot_x, dot_y = line.split(",")
                initial_state.append((int(dot_y), int(dot_x)))

initial_state = np.array(initial_state)
# print(initial_state)
# print(folds)

def print_grid(state):
    dot_grid = np.zeros((state[:, 0].max() + 1, state[:, 1].max() + 1), dtype=int)
    dot_grid[state[:, 0], state[:, 1]] = 1
    for row in dot_grid:
        print("".join([("#" if x == 1 else " ") for x in row]))

def compute_fold(state, axis, crease_value):
    is_reflected = state[:, axis] > crease_value
    new_state = state.copy()
    new_state[is_reflected, axis] = (2 * crease_value) - state[is_reflected, axis]
    return np.unique(new_state, axis=0)

# part 1
current_state = compute_fold(initial_state, *folds[0])
print(f"Part 1 solution: {len(current_state)}")

# part 2
current_state = initial_state
for fold in folds:
    current_state = compute_fold(current_state, *fold)

print("Part 2 solution:")
print_grid(current_state)
