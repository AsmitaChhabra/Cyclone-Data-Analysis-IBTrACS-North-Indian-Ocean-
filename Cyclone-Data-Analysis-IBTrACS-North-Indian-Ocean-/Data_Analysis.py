# ===============================================================
# 🌪️ Cyclone Data Analysis Project
# ===============================================================

# -------------------------------
# 1. Import Libraries
# -------------------------------
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# -------------------------------
# 2. Load Data
# -------------------------------
df = pd.read_csv("/Users/asmita/Desktop/cyclone data/IBTrACS.NI.v04r01_new.csv")

print(df.info()) #basic info about the dataset
print(df.shape) #how many rows and columns in total 

# -------------------------------
# 3. Data Cleaning & Transformation
# -------------------------------

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

# Removes storms with missing wind speed, pressure, etc.
storm_final = storm_summary_clean.dropna()
# Remove rows where subbasin is labeled as "missing"
storm_final = storm_final[storm_final["subbasin"] != "missing"]

print("Before cleaning:", df.shape)
print("After cleaning:", storm_final.shape)


# -------------------------------
# 4. Descriptive Statistics
# -------------------------------

#To check the distribution of storms :

# storm_counts_subbasin: number of storms in each subbasin (Bay of Bengal, Arabian Sea, etc.).
storm_counts_subbasin = storm_final['subbasin'].value_counts()
print(storm_counts_subbasin) 

#storm_counts_year: number of storms each year (chronological order using sort_index()).
storm_counts_year = storm_final['season'].value_counts().sort_index()
print(storm_counts_year)

#pivot table to summarise the number of storms per year in each subbasin.
storm_counts_pivot = pd.pivot_table(
    storm_final[storm_final["subbasin"]!= "missing"], #only include rows where subbasin in not null
    index="season",
    columns="subbasin",
    values="storm_id",
    aggfunc="count",
    fill_value=0 
)
print(f"storm_pivot", storm_counts_pivot.head())


# -------------------------------
# 5. Exploratory Data Analysis (EDA)
# -------------------------------
# -------------------------------
# 📊 Trend over time: number of storms per year
# -------------------------------

plt.figure(figsize=(12,6))
plt.plot(storm_counts_year.index, storm_counts_year.values, marker='o', linestyle='-')

#storm_counts_year = df.groupby("season")["storm_id"].nunique()
# season becomes the index (because you grouped by it).
# nunique() gives the values (number of storms).

plt.title("Trend of Cyclones per Year", fontsize=14)
plt.xlabel("Year (Season)")
plt.ylabel("Number of Storms")
plt.grid(True)
plt.show()

# -------------------------------
# 📊 Trend over time with moving average
# -------------------------------

plt.figure(figsize=(12,6))

# Raw yearly cyclone counts (line with markers)
plt.plot(storm_counts_year.index, storm_counts_year.values, 
         marker='o', color='blue', linestyle='-', linewidth=1, label="Yearly Counts")

# 5-year moving average (smoothed trend line)
storm_counts_year_rolling = storm_counts_year.rolling(window=5).mean() #calculated mean over a window of 5 years
plt.plot(storm_counts_year.index, storm_counts_year_rolling, 
         color='red', linestyle='--', linewidth=2, label="5-Year Moving Avg")

#importance : A rolling average makes the trend smoother (given the big ups and downs and the noisy nature of the data), easier to see long-term changes.

# Add labels, title, grid, legend
plt.title("Trend of Cyclones per Year (with 5-Year Moving Average)", fontsize=14, fontstyle="italic")
plt.xlabel("Year (Season)")
plt.ylabel("Number of Storms")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

# -------------------------------
# 📊 Trend of cyclones per year by subbasin (line chart)
# -------------------------------
plt.figure(figsize=(14,6))
for subbasin in storm_counts_pivot.columns:
    plt.plot(storm_counts_pivot.index, storm_counts_pivot[subbasin], marker='o', linestyle="-",label=subbasin)


storm_counts_pivot_rolling = storm_counts_pivot.rolling(window=5).mean()

for subbasin in storm_counts_pivot_rolling.columns:
    plt.plot(storm_counts_pivot_rolling.index, storm_counts_pivot_rolling[subbasin], linestyle="--", linewidth=2, label= f"{subbasin}(5-yr Moving Average)", color="black")
plt.title("Trend of Cyclones per Year by Subbasin with 5 year moving average", fontsize=14, fontstyle="italic")
plt.xlabel("Year (Season)")
plt.ylabel("Number of Storms")
plt.grid(alpha=0.3)
plt.legend(title="Subbasin")
plt.show()


# 📊 Histogram: distribution of maximum wind speeds
plt.figure(figsize=(10,6))

plt.hist(storm_final["max_wind_speed"].dropna(), bins=30, edgecolor="black", alpha=0.7)
plt.title("Distribution of Maximum Wind Speeds", fontsize=14, fontstyle="italic")
plt.xlabel("Maximum Wind Speed (knots)")
plt.ylabel("Frequency")
plt.grid(alpha=0.3)

plt.show()

plt.figure(figsize=(10,6))
plt.hist (storm_final["min_pressure"].dropna(), bins=50 , color = "blue", alpha = 0.5)
plt.title("Distribustion of Minimum Pressure", fontsize =16, ) 
plt.xlabel("Minimum Pressure")
plt.ylabel("Frequency")
plt.grid(alpha=0.5)
plt.show ()

# 📊 Boxplot: compare Bay of Bengal vs Arabian Sea storm intensities
# (to be implemented)

# 📊 Scatter plot: min pressure vs max wind speed
# (to be implemented)
plt.figure(figsize=(8,6))
plt.scatter(storm_final["min_pressure"], storm_final["max_wind_speed"], alpha=0.5, color="purple")

plt.title("Relationship between Pressure and Wind Speed")
plt.xlabel("Min Pressure (hPa)")
plt.ylabel("Max Wind Speed (knots)")
plt.grid(alpha=0.3)
plt.show()

# same scatter plot using seaborn (so much simpler!)
sns.relplot (data= storm_final, x ="min_pressure" , y = "max_wind_speed", hue = "subbasin" )
plt.show()


# 📊 Heatmap: storm frequency by month and year
# -------------------------------
# 📊 Heatmap: Storm Frequency by Month & Year
# -------------------------------
import calendar #helps us convert month numbers (1–12) to names like Jan, Feb, etc.

# Ensure iso_time is parsed correctly
df['iso_time'] = pd.to_datetime(df['iso_time'], format="%Y-%m-%d %H:%M:%S", errors='coerce') #Parse dates and  errors='coerce' means any dates that don’t match the format will become NaT

# Drop rows where parsing failed
df_clean = df.dropna(subset=['iso_time']).copy()

# Extract year and month
df_clean['year'] = df_clean['iso_time'].dt.year
df_clean['month'] = df_clean['iso_time'].dt.month

# Optional: filter recent years if dataset is huge
# df_clean = df_clean[df_clean['year'] >= 1950]

# Count unique storms per month-year
storm_counts = df_clean.groupby(['year', 'month'])['storm_id'].nunique().reset_index(name='storm_count')

# Pivot table for heatmap
heatmap_data = storm_counts.pivot(index='month', columns='year', values='storm_count')

# Fill missing month-year combos with 0
all_months = range(1,13)
heatmap_data = heatmap_data.reindex(all_months, fill_value=0)

# Ensure month numbers are integers
heatmap_data.index = heatmap_data.index.astype(int)

# Replace month numbers with abbreviated month names
heatmap_data.index = [calendar.month_abbr[m] for m in heatmap_data.index]

# Plot the heatmap
plt.figure(figsize=(16,8))
sns.heatmap(
    heatmap_data, 
    cmap="YlOrRd", 
    linewidths=0.5, 
    annot=True, 
    fmt="g"
)
plt.title("Storm Frequency by Month and Year", fontsize=16)
plt.ylabel("Month")
plt.xlabel("Year")
plt.show()

# Optional: print pivot to verify
print(heatmap_data.head())


# 🌍 Geospatial analysis (if latitude/longitude data is available)
# (to be implemented)

#correation matrix 

# -------------------------------
# 6. Statistical Analysis
# -------------------------------

# Hypothesis testing example:
# Are storms in the Bay of Bengal significantly stronger than in the Arabian Sea?
# (to be implemented)


# -------------------------------
# 7. Modeling (Optional)
# -------------------------------

# Classification: Predict landfall (1/0) from storm features
# (to be implemented)

# Clustering: Group storms by intensity, speed, and duration
# (to be implemented)

# Time series forecasting: Predict number of storms per decade
# (to be implemented)


# -------------------------------
# 8. Conclusions & Insights
# -------------------------------

# Summarize findings, key trends, and potential real-world implications
# (to be written)
