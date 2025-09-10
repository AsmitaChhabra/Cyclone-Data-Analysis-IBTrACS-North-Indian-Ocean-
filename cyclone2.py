import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("/Users/asmita/Desktop/cyclone data/IBTrACS.NI.v04r01_new.csv")

print(df.info())

# Remove rows where storm_id and name exist but all other cols are empty
df1 = df[~(
    df[['storm_id', 'name']].notna().all(axis=1) &
    df.drop(columns=['storm_id', 'name']).isna().all(axis=1)
)]
print("Before cleaning:", df.shape)
print("After cleaning:", df1.shape)

# ---- Add storm_type (Named vs Unnamed) ----
df1["storm_type"] = np.where(
    df1["name"].notna() & df1["name"].str.strip().ne(""), 
    "Named", "Unnamed"
)

# ---- Aggregate per storm ----
storm_summary_clean = df1.groupby(['storm_id','storm_type']).agg(
    max_wind_speed=("wind_speed","max"),
    min_pressure=("pressure","min"),
    avg_wind_speed=("wind_speed","mean"),
    season=("season","first"),
    subbasin=("subbasin","first")
).reset_index()

storm_final = storm_summary_clean.dropna()
print("Final storm table shape:", storm_final.shape)
print(storm_final[["storm_id","storm_type","max_wind_speed"]].head())

# ---- Counts by subbasin ----
storm_counts_subbasin = storm_final['subbasin'].value_counts()
print(storm_counts_subbasin)

# ---- Storms per year ----
storm_counts_year = storm_final['season'].value_counts().sort_index()
print(storm_counts_year)

pivot_counts = storm_final.pivot_table(
    index="season", 
    columns="subbasin", 
    values="storm_id", 
    aggfunc="count",
    fill_value=0
)

# ---- Plot: Storms per year by subbasin ----
plt.figure()
for subbasin in pivot_counts.columns:
    plt.plot(pivot_counts.index, pivot_counts[subbasin], marker="x", label=subbasin)

plt.title("Number of Storms per Year by Subbasin")
plt.xlabel("Year")
plt.ylabel("Number of Storms")
plt.legend()
plt.grid(True)
plt.show()

# ---- Scatter: Pressure vs Wind Speed ----
plt.figure()
plt.scatter(storm_final['min_pressure'], storm_final['max_wind_speed'])
plt.xlabel("Min Pressure (hPa)")
plt.ylabel("Max Wind Speed (knots)")
plt.title("Pressure vs Wind Speed")
plt.show()

import seaborn as sns

plt.figure(figsize=(6,5))
sns.boxplot(x="storm_type", y="max_wind_speed", data=storm_final, palette=["skyblue","salmon"])
plt.title("Max Wind Speed Distribution: Named vs Unnamed Storms")
plt.xlabel("Storm Type")
plt.ylabel("Max Wind Speed (knots)")
plt.show()
