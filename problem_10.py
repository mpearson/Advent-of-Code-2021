data_path = "data/problem_10.txt"
# data_path = "data/problem_10_test.txt"

with open(data_path, "r") as f:
    data = f.readlines()

# part 1
bracket_pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

error_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

autocomplete_scores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


score = 0
for line in data:
    stack = []
    for char in line.rstrip():
        if not stack or char in bracket_pairs:
            stack.append(char)
        elif char != bracket_pairs[stack[-1]]:
            score += error_scores[char]
            break
        else:
            stack.pop()

print(f"Part 1 solution: {score}")

# part 2
scores = []
for line in data:
    score = 0
    stack = []
    corrupt_line = False
    for char in line.rstrip():
        if not stack or char in bracket_pairs:
            stack.append(char)
        elif char != bracket_pairs[stack[-1]]:
            corrupt_line = True
            break
        else:
            stack.pop()

    if not corrupt_line and stack:
        missing_brackets = (bracket_pairs[char] for char in reversed(stack))
        for char in missing_brackets:
            score = (score * 5) + autocomplete_scores[char]

        scores.append(score)

scores.sort()

print(f"Part 2 solution: {scores[len(scores) // 2]}")

