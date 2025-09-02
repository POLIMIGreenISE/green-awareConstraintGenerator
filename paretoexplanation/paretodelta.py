import re
import csv
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

files = ["explanation50.txt", "explanation55.txt", "explanation60.txt", 
         "explanation65.txt", "explanation70.txt", "explanation75.txt", 
         "explanation80.txt", "explanation85.txt", "explanation90.txt"]

def parse_file(file):
    text = Path(file).read_text()
    matches = re.findall(
        r"(\w+\d+) component.*?on the (\w+\d+) node.*?between ([\d\.]+) gCO2eq and ([\d\.]+) gCO2eq",
        text,
        re.DOTALL,
    )
    return pd.DataFrame(matches, columns=["component", "node", "max_gco2", "min_gco2"])

dfs = {file: parse_file(file) for file in files}
plt.figure(figsize=(15, 7))
offset = 85
files = files[::-1]
all_diffs = []
labels_leg = []

for f1, f2 in zip(files, files[1:]):
    df1 = dfs[f1]
    df2 = dfs[f2]
    number = f1.replace("explanation", "").replace(".txt", "")
    number = (int(number) - 5) / 100
    name = rf"$\tau = q_{{{number}}}$"
    labels_leg.append(name)
    diff = pd.merge(df1, df2, how="outer", indicator=True)
    only_in_df1 = diff[diff["_merge"] == "right_only"].drop(columns=["_merge"])
    only_in_df1["max_gco2"] = pd.to_numeric(only_in_df1["max_gco2"], errors="coerce")
    only_in_df1["label"] = name
    only_in_df1["min_gco2"] = pd.to_numeric(only_in_df1["min_gco2"], errors="coerce")
    only_in_df1["diff_gco2"] = only_in_df1["max_gco2"] - only_in_df1["min_gco2"]
    values = only_in_df1["max_gco2"].sort_values(ascending=False).reset_index(drop=True)
    x = range(offset, offset + len(values))  
    #plt.bar(x, only_in_df1["max_gco2"].sort_values(ascending=False).reset_index(drop=True), label=name)
    #offset += len(values)
    all_diffs.append(only_in_df1)

df = dfs["explanation90.txt"]
name = r"$\tau = q_{0.9}$"
df["max_gco2"] = pd.to_numeric(df["max_gco2"], errors="coerce")
df["min_gco2"] = pd.to_numeric(df["min_gco2"], errors="coerce")
df["diff_gco2"] = df["max_gco2"] - df["min_gco2"]
df["label"] = name
values = df["max_gco2"].sort_values(ascending=False).reset_index(drop=True)
x = range(0, 85)
all_diffs.append(df)
labels_leg.append(name)
#plt.bar(x, df["max_gco2"].sort_values(ascending=False).reset_index(drop=True), label=name)

combined_df = pd.concat(all_diffs, ignore_index=True)
combined_df = combined_df.sort_values("max_gco2", ascending=False).reset_index(drop=True)

colors = plt.cm.tab10(np.linspace(0, 1, len(combined_df['label'].unique())))
color_map = dict(zip(combined_df['label'].unique(), colors))

# Plot each point, but only show legend for selected labels
for label in combined_df['label'].unique():
    subset = combined_df[combined_df['label'] == label]
    plt.bar(subset.index, subset['max_gco2'],
                color=color_map[label],
                label=label if label in labels_leg else "_nolegend_")
# unique_labels = combined_df["label"].unique()
# x = combined_df.index
# y = combined_df["max_gco2"]
# plt.bar(x,y)
# plt.xticks(x, combined_df["label"], rotation=45, ha="right")

plt.xlabel("Data points")
plt.ylabel("Max gCO₂ saved")
plt.title("Threshold impact on the constraints")
# handles, labels = plt.gca().get_legend_handles_labels()
# order = [8,0,1,2,3,4,5,6,7]
plt.legend()
plt.grid(True)
plt.show()