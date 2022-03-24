import numpy as np

data_path = "data/problem_7.txt"
# data_path = "data/problem_7_test.txt"

data = np.genfromtxt(data_path, dtype=int, delimiter=",")


# 🦀 🦀 🦀 🦀 🦀
# data = (np.random.random(162) * 100203).astype(np.int64) + 5

# part 1
print(f"Part 1 solution: {np.abs(data - int(np.median(data))).sum()}")


# part 2
# barbaric O(N * M) brute force way
# distances = np.abs(data.reshape(-1, 1) - np.arange(data.min(), data.max() + 1, dtype=np.int64))
# fuel_cost = (distances * (distances + 1) // 2).sum(axis=0)
# centroid = np.argmin(fuel_cost) + data.min()

# print(f"best position: {centroid}")
# print(f"Part 2 solution: {fuel_cost.min()}")

# elegant O(N) calculus way

# find centroid c that minimizes:
#     ε = Σ[(x_i + c)(x_i - c + 1) / 2]
#
# δε/δc = 1/2 Σ[c² - (2x_i + 1)c]
#       = 1/2 Σ[2c - 2x_i - 1]
#       = 0
#   2cN = 2 Σ[x_i] - N
#     c = (2 Σ[x_i] - N) / 2N
centroid = int(np.round(((2 * (data).sum() - len(data)) / (2 * len(data)))))

# Unfortunately the real cost function is not continuously differentiable, and our s(s + 1)
# approximation minimum not at s = 0 but at s = -1/2, the nearest integer centroid value is
# occasionally (when???) too low by 1. Let's just check the next integer up as well.
centroid_candidates = np.array([centroid, centroid + 1])
distances = np.abs(data.reshape(-1, 1) - centroid_candidates)
fuel_cost = (distances * (distances + 1) // 2).sum(axis=0)
centroid = centroid_candidates[np.argmin(fuel_cost)]

print(f"best position: {centroid}")
print(f"Part 2 solution: {fuel_cost.min()}")
