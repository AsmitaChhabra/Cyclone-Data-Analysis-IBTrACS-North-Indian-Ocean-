import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df= pd.read_csv("/Users/asmita/Desktop/cyclone data/IBTrACS.NI.v04r01_new.csv")

print(df.info())
#print(df['storm_id'].value_counts())

df1 = df[~(
    df[['storm_id', 'name']].notna().all(axis=1) &   # storm_id AND storm_name present
    df.drop(columns=['storm_id', 'name']).isna().all(axis=1)  # but all other cols empty
)]

print("Before cleaning:", df.shape)
print("After cleaning:", df1.shape)

#creating 1 row per storm and deleteing all the data that is esentially useless for teh garph 
storm_summary_clean = df.groupby('storm_id').agg(max_wind_speed= ("wind_speed", "max"),
                                                    min_pressure= ("pressure", "min"),
                                                    avg_wind_speed=("wind_speed", "mean"), 
                                                    season = ("season", "first"),
                                                    subbasin = ("subbasin", "first"),). reset_index()

storm_final = storm_summary_clean.dropna()
print("Before cleaning:", df.shape)
print("After cleaning:", storm_final.shape)

storm_counts_subbasin = storm_final['subbasin'].value_counts()
print(storm_counts_subbasin)

# Storms per year
storm_counts_year = storm_final['season'].value_counts().sort_index()
print(storm_counts_year)


pivot_counts = storm_final.pivot_table(
    index="season", 
    columns="subbasin", 
    values="storm_id", 
    aggfunc="count",
    fill_value=0
)


plt.figure()
for subbasin in pivot_counts.columns[:-1]:
    plt.plot(pivot_counts.index, pivot_counts[subbasin], marker = "x", label= subbasin)

plt.title("Number of Storms per Year by Subbasin")
plt.xlabel("year")
plt.ylabel("Number of Storms")
plt.legend()
plt.grid(True)
plt.show()

plt.figure()
plt.scatter(storm_final['min_pressure'],storm_final["max_wind_speed"])
plt.xlabel("Min Pressure (hPa)")
plt.ylabel("Max Wind Speed (knots)")
plt.show()

# Make sure storm_id and name exist
df["storm_type"] = np.where(df["name"].notna() & df["name"].str.strip().ne(""), 
                            "Named", "Unnamed")

# Now aggregate storm-wise
storm_summary_clean = df.groupby(['storm_id','storm_type']).agg(
    max_wind_speed=("wind_speed","max"),
    min_pressure=("pressure","min"),
    avg_wind_speed=("wind_speed","mean"),
    season=("season","first"),
    subbasin=("subbasin","first")
).reset_index()

storm_final = storm_summary_clean.dropna()

print(storm_final[["storm_id","storm_type","max_wind_speed"]].head())
