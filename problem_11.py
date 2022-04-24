import numpy as np

data_path = "data/problem_11.txt"
# data_path = "data/problem_11_test.txt"

data = []
with open(data_path, "r") as f:
    for line in f:
        data.append([int(char) for char in line.rstrip()])
data = np.array(data)
print("Initial state:")


def get_neighborhood_view(state, y, x):
    # return a view of the 3x3 region around (y, x)
    return state[max(0, y - 1) : y + 2, max(0, x - 1) : x + 2]


def step(state):
    state += 1
    flash_count = 0

    while True:
        triggered_y, triggered_x = np.where(state > 9)
        number_triggered = len(triggered_y)

        # step ends when no further 🐙 are triggered
        if number_triggered == 0:
            break

        flash_count += number_triggered

        # convolve 3x3 box with triggered cells
        for y, x in zip(triggered_y, triggered_x):
            neighbors = get_neighborhood_view(state, y, x)
            neighbors[neighbors > 0] += 1

        state[triggered_y, triggered_x] = 0

    return flash_count


# part 1
data_part_1 = data.copy()
total_flashes = 0
for i in range(100):
    total_flashes += step(data_part_1)
print(f"State at step {i + 1}:")
print(data_part_1)
print(f"Part 1 solution: {total_flashes}")


# part 2
data_part_2 = data.copy()
total_flashes = 0
number_of_octopi = np.product(data_part_2.shape)
for i in range(10000):
    if step(data_part_2) == number_of_octopi:
        print(f"State at step {i + 1}:")
        print(data_part_2)
        print(f"Part 2 solution: {i + 1}")
        break
