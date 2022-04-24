import numpy as np

data_path = "data/problem_06.txt"
# data_path = "data/problem_06_test.txt"

# 🐟🐠🐡
data = np.genfromtxt(data_path, dtype=np.uint64, delimiter=",")

def simulate_fish(starting_ages, days):
    age_bins = np.zeros(9, dtype=np.uint64) # 🐠⏰

    for age, count in zip(*np.unique(starting_ages, return_counts=True)):
        age_bins[age] = count

    for _day in range(days):
        # time to make babby 🐟🥚
        new_fish = age_bins[0]

        # time to get old
        age_bins[0:8] = age_bins[1:9]
        age_bins[6] += new_fish
        age_bins[8] = new_fish

    return age_bins[:9]

# part 1
print(f"Part 1 solution: {simulate_fish(data, 80).sum()}")

# part 2
print(f"Part 2 solution: {simulate_fish(data, 256).sum()}")
