import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_csv("datasets/6591c791-9bfb-4203-9f02-660a666cb53d.csv")

# Drop missing values
df = df.dropna()

# Create a chloropleth map
plt.figure(figsize=(10, 8))
plt.title("Chloropleth Map of WT and QSEC")
plt.xlabel("WT")
plt.ylabel("QSEC")
plt.scatter(df["wt"], df["qsec"])
plt.savefig("chloropleth_map.png")
