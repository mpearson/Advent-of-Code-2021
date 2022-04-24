
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
                folds.append((direction == "x", int(value)))
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

def fold_y(state, crease_value):
    is_reflected = state[:, 0] > crease_value
    new_state = state.copy()
    new_state[is_reflected, 0] = (2 * crease_value) - state[is_reflected, 0]
    return np.unique(new_state, axis=0)

def fold_x(state, crease_value):
    is_reflected = state[:, 1] > crease_value
    new_state = state.copy()
    new_state[is_reflected, 1] = (2 * crease_value) - state[is_reflected, 1]
    return np.unique(new_state, axis=0)

# part 1
is_x, crease_value = folds[0]
if is_x:
    current_state = fold_x(initial_state, crease_value)
else:
    current_state = fold_y(initial_state, crease_value)

# print_grid(current_state)
print(f"Part 1 solution: {len(current_state)}")

# part 2
current_state = initial_state
for is_x, crease_value in folds:
    if is_x:
        current_state = fold_x(current_state, crease_value)
    else:
        current_state = fold_y(current_state, crease_value)

print("Part 2 solution:")
print_grid(current_state)
