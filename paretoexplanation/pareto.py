import re
import csv
import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

files = ["explanation50.txt", "explanation55.txt", "explanation60.txt", 
         "explanation65.txt", "explanation70.txt", "explanation75.txt", 
         "explanation80.txt", "explanation85.txt", "explanation90.txt",]

def parse_file(file):
    text = Path(file).read_text()
    matches = re.findall(
        r"(\w+\d+) component.*?on the (\w+\d+) node.*?between ([\d\.]+) gCO2eq and ([\d\.]+) gCO2eq",
        text,
        re.DOTALL,
    )
    return pd.DataFrame(matches, columns=["component", "node", "max_gco2", "min_gco2"])

dfs = {file: parse_file(file) for file in files}
plt.figure(figsize=(10, 7))

for f1, f2 in zip(files, files[1:]):
    df1 = dfs[f1]
    df2 = dfs[f2]
    number = f1.replace("explanation", "").replace(".txt", "")
    name = f"Unique to threshold {number}"
    diff = pd.merge(df1, df2, how="outer", indicator=True)
    only_in_df1 = diff[diff["_merge"] == "left_only"].drop(columns=["_merge"])
    only_in_df1["max_gco2"] = pd.to_numeric(only_in_df1["max_gco2"], errors="coerce")
    only_in_df1["min_gco2"] = pd.to_numeric(only_in_df1["min_gco2"], errors="coerce")
    only_in_df1["diff_gco2"] = only_in_df1["max_gco2"] - only_in_df1["min_gco2"]
    plt.scatter(only_in_df1["min_gco2"], only_in_df1["max_gco2"], s=90, edgecolors="black", linewidths=0.5, label=name)

df = dfs["explanation90.txt"]
name = "Unique to threshold 90"
df["max_gco2"] = pd.to_numeric(df["max_gco2"], errors="coerce")
df["min_gco2"] = pd.to_numeric(df["min_gco2"], errors="coerce")
df["diff_gco2"] = df["max_gco2"] - df["min_gco2"]
plt.scatter(df["min_gco2"], df["max_gco2"], s=90, edgecolors="black", linewidths=0.5, label=name)


plt.xlabel("Min gCO₂ saved")
plt.ylabel("Max gCO₂ saved")
plt.title("Threshold impact on the constraints")
plt.legend()
plt.grid(True)
plt.show()