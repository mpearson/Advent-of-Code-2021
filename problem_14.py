
import numpy as np

data_path = "data/problem_14.txt"
# data_path = "data/problem_14_test.txt"

insertion_rules = []
with open(data_path, "r") as f:
    initial_state = [ord(x) for x in f.readline().rstrip()]

    for line in f:
        line = line.rstrip()
        if line:
            ab, c = line.split(" -> ")
            insertion_rules.append((ord(ab[0]), ord(ab[1]), ord(c)))

insertion_rules = np.array(insertion_rules)
char_offset = insertion_rules.min()
initial_state = np.array(initial_state, dtype=np.int64) - char_offset
insertion_rules -= char_offset
table_size = insertion_rules.max() + 1
insertion_table = np.full((table_size, table_size), -1, dtype=np.int64)
insertion_table[insertion_rules[:, 0], insertion_rules[:, 1]] = insertion_rules[:, 2]

# print(initial_state)
# print(insertion_table)

# part 1
def compute_part_1():
    current_state = initial_state

    for i in range(10):
        new_state = np.empty(len(current_state) * 2 - 1, dtype=int)
        new_state[0::2] = current_state
        new_state[1::2] = insertion_table[current_state[:-1], current_state[1:]]

        current_state = new_state


    char_counts = np.unique(current_state, return_counts=True)[1]
    char_counts.sort()

    # print("".join([chr(x) for x in (current_state + char_offset)]))
    print(char_counts)

    return char_counts[-1] - char_counts[0]

print(f"Part 1 solution: {compute_part_1()}")

# part 2
def compute_part_2():
    current_state = np.zeros_like(insertion_table)
    next_state = np.zeros_like(current_state)

    # state is now a 2D array of counts of element pairs
    for a, b in zip(initial_state[:-1], initial_state[1:]):
        current_state[a, b] += 1

    # 2xN array of all element index pairs, e.g. if table_size == 4 you get:
    # [[0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
    #  [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]]
    element_indices = np.arange(table_size)
    pair_indices = np.dstack(np.meshgrid(element_indices, element_indices)).reshape(-1, 2).T

    for i in range(40):
        next_state[...] = 0


        existing_pairs = np.vstack(np.where(current_state != 0))
        current_counts = current_state[existing_pairs[0], existing_pairs[1]]
        new_elements = insertion_table[existing_pairs[0], existing_pairs[1]]
        # Unfortunately we can't eliminate these loops because existing_pairs contains duplicate
        # indices, which results in undefined behavior in numpy. Basically we can't modify the same
        # index twice in one operation. 😢🐼
        for (left, right), new_element, count in zip(existing_pairs.T, new_elements, current_counts):
            next_state[left, new_element] += count
            next_state[new_element, right] += count

        current_state[...] = next_state

    # The magical insight here is that each element in each pair only counts for half,
    # since it appears in two pairs. *except* the two elements at the very end, which
    # never change throughout the process and are only in one pair.
    char_counts = (current_state.sum(axis=0) + current_state.sum(axis=1)) // 2
    char_counts[initial_state[0]] += 1
    char_counts[initial_state[-1]] += 1
    char_counts.sort()
    # remove the 0's
    char_counts = char_counts[char_counts != 0]
    print(char_counts)

    return char_counts[-1] - char_counts[0]

print(f"Part 2 solution: {compute_part_2()}")
