import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

data = np.genfromtxt("data/problem_1.txt").astype(np.int64)
# part 1
print(f"Part 1 solution: {np.sum(np.diff(data) > 0)}")

# part 2
print(f"Part 2 solution: {np.sum(np.diff(np.sum(sliding_window_view(data, window_shape=3), axis=1)) > 0)}")
