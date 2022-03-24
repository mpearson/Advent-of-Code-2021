from pathlib import Path

for i in range(8, 26):
    with open(f"problem_{i}.py", "w") as f:
        f.write(f"""
data_path = "data/problem_{i}.txt"
# data_path = "data/problem_{i}_test.txt"

data = np.genfromtxt(data_path, dtype=int, delimiter=",")
print(data)

# part 1
print(f"Part 1 solution: {{None}}")

# part 2
print(f"Part 2 solution: {{None}}")

""")

    with open(f"data/problem_{i}.txt", "w") as f:
        pass
    with open(f"data/problem_{i}_test.txt", "w") as f:
        pass

