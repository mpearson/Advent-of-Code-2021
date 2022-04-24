import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

# import pandas as pd

data_path = "data/problem_04.txt"
# data_path = "data/problem_04_test.txt"

with open(data_path, "r") as f:
    numbers = np.array([int(n) for n in f.readline().strip().split(",")], dtype=np.uint32)
    boards = np.genfromtxt(f, dtype=np.uint32).reshape(-1, 5, 5)

print("all numbers called:", np.all(np.unique(numbers) == np.unique(boards)))

# on which turn was each cell in each board marked?
marked_on_turn = np.full_like(boards, 999999)
for turn, number in enumerate(numbers):
    marked_on_turn[boards == number] = turn

# on which turn does each row or column in each board get completed?
row_victory_turn_nums = np.max(marked_on_turn, axis=2)
col_victory_turn_nums = np.max(marked_on_turn.transpose([0, 2, 1]), axis=2)


# part 1

# which board and row or col is completed first?
row_victory_board, row_victory_row = np.unravel_index(np.argmin(row_victory_turn_nums), row_victory_turn_nums.shape)
col_victory_board, col_victory_row = np.unravel_index(np.argmin(col_victory_turn_nums), col_victory_turn_nums.shape)

# is a row or col completed first?
if row_victory_turn_nums[row_victory_board, row_victory_row] < col_victory_turn_nums[col_victory_board, col_victory_row]:
    winning_board = row_victory_board
    winning_turn = np.min(row_victory_turn_nums[row_victory_board])
else:
    winning_board = col_victory_board
    winning_turn = np.min(col_victory_turn_nums[col_victory_board])

print(f"board {winning_board} wins on turn {winning_turn}")

victory_board = boards[winning_board]
victory_board[marked_on_turn[winning_board] <= winning_turn] = 0
print("winning board:")
print(victory_board)
print(f"sum: {victory_board.sum()}")
print(f"final number: {numbers[winning_turn]}")
print(f"Part 1 solution: {victory_board.sum() * numbers[winning_turn]}\n")

# part 2

row_victory_turn = np.min(row_victory_turn_nums, axis=1)
col_victory_turn = np.min(col_victory_turn_nums, axis=1)

print("turn at which each board wins by row or col")

board_victory_turn = np.min([row_victory_turn, col_victory_turn], axis=0)
last_board_to_win = np.argmax(board_victory_turn)
last_turn = board_victory_turn[last_board_to_win]

print(f"board {last_board_to_win} finishes last on turn {last_turn}")

last_board = boards[last_board_to_win]
last_board[marked_on_turn[last_board_to_win] <= last_turn] = 0
print("last board to finish:")
print(last_board)
print(f"sum: {last_board.sum()}")
print(f"final number: {numbers[last_turn]}")

print(f"Part 2 solution: {last_board.sum() * numbers[last_turn]}\n")
