import numpy as np

data_path = "data/problem_3.txt"
# data_path = "data/problem_3_test.txt"

data = np.loadtxt(data_path, dtype="S")
input_width = len(data[0])
data = data.view(dtype=np.uint8).reshape(-1, input_width) == ord("1")


# part 1
exponents = 2 ** np.arange(data.shape[1])[::-1].reshape(-1, 1)
gamma = (np.sum(data, axis=0) > len(data) * 0.5).astype(np.int32)
power_consumption = ((1 - gamma) @ exponents) * (gamma @ exponents)
print(f"Part 1 solution: {power_consumption[0]}\n")


# part 2
o2_data = data[:]
co2_data = data[:]

o2_candidates = np.arange(len(data))
co2_candidates = np.arange(len(data))

for col_index in range(data.shape[1]):
    o2_gamma = int(np.sum(data[o2_candidates, col_index]) >= len(o2_candidates) * 0.5)
    co2_gamma = int(np.sum(data[co2_candidates, col_index]) < len(co2_candidates) * 0.5)

    o2_candidates = o2_candidates[data[o2_candidates, col_index] == o2_gamma]
    co2_candidates = co2_candidates[data[co2_candidates, col_index] == co2_gamma]

    if len(o2_candidates) == 1:
        o2_value = data[o2_candidates[0]]
    if len(co2_candidates) == 1:
        co2_value = data[co2_candidates[0]]

o2_value = (o2_value @ exponents)[0]
co2_value = (co2_value @ exponents)[0]
print(f"o2_value: {o2_value}")
print(f"co2_value: {co2_value}")
print(f"Part 2 solution: {o2_value * co2_value}\n")
