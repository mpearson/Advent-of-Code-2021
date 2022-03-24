import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

import pandas as pd

df = pd.read_csv("data/problem_2.txt", sep=" ", names=["dir", "value"])

# part 1
dx = df[df["dir"] == "forward"]["value"].sum()
dy = df[df["dir"] == "down"]["value"].sum() - df[df["dir"] == "up"]["value"].sum()
print(f"forward: {dx}, down: {dy}")
print(f"Part 1 solution: {dx * dy}\n")


# part 2
df["delta_aim"] = 0

forward_commands = df["dir"] == "forward"
down_commands = df["dir"] == "down"
up_commands = df["dir"] == "up"

df.loc[down_commands, "delta_aim"] = df.loc[down_commands, "value"]
df.loc[up_commands, "delta_aim"] = -df.loc[up_commands, "value"]

# accumulate aim values at each timestep
df["aim"] = np.cumsum(df["delta_aim"])

dx = df.loc[forward_commands, "value"].sum()
dy = (df.loc[forward_commands, "aim"] *  df.loc[forward_commands, "value"]).sum()

print(f"forward: {dx}, down: {dy}")
print(f"Part 2 solution: {dx * dy}\n")
