import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

df= pd.read_csv("/Users/asmita/Desktop/cyclone data/IBTrACS.NI.v04r01_new.csv")

print(df.info()) #basic info about the dataset
print(df.shape) #how many rows and columns in total 

#there data consists of many rows where storm id and name are present but other columns are empty and every storm id has multiple entries. 
# so we create one row per storm 

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

print("Before cleaning:", df.shape)
print("After cleaning:", storm_final.shape)

#To check the distribution of storms :
#storm_counts_subbasin: number of storms in each subbasin (Bay of Bengal, Arabian Sea, etc.).
storm_counts_subbasin = storm_final['subbasin'].value_counts()
print(storm_counts_subbasin) 

#storm_counts_year: number of storms each year (chronological order using sort_index()).
storm_counts_year = storm_final['season'].value_counts().sort_index()
print(storm_counts_year)

#pivot table to summarise the number of storms per year in each subbasin.

