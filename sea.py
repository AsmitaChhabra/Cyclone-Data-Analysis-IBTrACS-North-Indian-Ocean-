import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_csv("/Users/asmita/Desktop/cyclone data/IBTrACS.NI.v04r01_new.csv", low_memory=False)


# Group the dataset by storm_id (each storm has multiple time steps → we want one row per storm)
storm_summary_clean = df.groupby("storm_id").agg(

    # Take the maximum wind speed observed during the storm
    max_wind_speed=("wind_speed", "max"),

    # Take the minimum central pressure recorded (lower pressure → stronger storm)
    min_pressure=("pressure", "min"),

    # Calculate the average wind speed across all observations of the storm
    avg_wind_speed=("wind_speed", "mean"),

    # Take the first season (year) recorded for the storm
    season=("season", "first"),

    # Take the first subbasin recorded (e.g., Bay of Bengal / Arabian Sea)
    subbasin=("subbasin", "first"),

    # Calculate the average forward movement speed of the storm
    storm_speed=("storm_speed", "mean"),

    # If storm made landfall, at least one row will have landfall=1 → take max
    landfall=("landfall", "max"),

    # Take the last recorded storm grade (e.g., starts as Depression, ends as Severe Cyclone)
    storm_grade=("storm_grade", "last"),

    # Take the first name assigned to the storm (in case it repeats across rows)
    name=("name", "first")

# End of aggregation
).reset_index()  # Reset index so storm_id becomes a regular column again
storm_final = storm_summary_clean.dropna() #Removes storms with missing wind speed, pressure, etc.

# Filter the dataset to include only storms from Bay of Bengal and Arabian Sea
stormy = storm_final[storm_final["subbasin"].isin(["Bay of Bengal", "Arabian Sea"])]
#create a scatter plot with best line of fit for max wind speed vs min pressure separated by subbasin
sns.lmplot(data = stormy,
             x= "min_pressure", y="max_wind_speed", col = "subbasin" , order = 1
#              order=2 → fits a quadratic curve (parabola) order=1 → fits a straight line (simple linear regression).order=3 → fits a cubic curve, and so on.
)
#plt.show()

sns.lmplot(data = stormy,
             x= "min_pressure", y="max_wind_speed", col = "subbasin" , order = 2
#              order=2 → fits a quadratic curve (parabola) order=1 → fits a straight line (simple linear regression).order=3 → fits a cubic curve, and so on.
)
#plt.show()
df1 = df[df["subbasin"].isin(["Bay of Bengal", "Arabian Sea"])]


#distribution of wind speed vs subbasin
sns.catplot (
    data = df1, 
    y= "wind_speed",
    hue = "subbasin", kind = "violin" #or boxplot 

)
#plt.show()

#

df1["storm_grade"] = df1["storm_grade"].dropna().str.strip().str.upper()

sns.catplot (
    data = df1, 
    x= "storm_grade", 
    y= "wind_speed",
    col = "subbasin", kind = "box" 

)
plt.show()

#
sns.catplot (
    data = df1, 
    x= "storm_grade", 
    y= "storm_speed",
    col = "subbasin", kind = "box" 

)
plt.show()


sns.catplot (
    data = df1,  
    y= "pressure",
    col = "storm_grade", hue='subbasin' ,kind = "violin" 

)
plt.show()

