🌪️ Cyclone Data Analysis in the North Indian Ocean

**Table of Contents**

Introduction
Data Preparation
Descriptive Statistics
Exploratory Data Analysis (EDA)
Modeling
Summary & Insights
Appendix: Plots
Introduction

This project analyzes cyclone data from the North Indian Ocean, focusing on the Bay of Bengal and Arabian Sea. Using the IBTrACS dataset, the study aims to:

Explore trends in cyclone frequency and intensity over time
Compare characteristics between subbasins
Investigate relationships between meteorological variables
Build a simple model to predict storm intensity


**Data Source: IBTrACS.NI.v04r01_new.csv**

**Steps:**
Loaded dataset with pandas.
Inspected data structure, removed rows with missing wind speed, pressure, or subbasin.
Aggregated data to have one row per storm, summarizing key statistics (max wind, min pressure, average wind, year, subbasin, etc.).

**Descriptive Statistics**

Number of storms per subbasin: Calculated using value counts.
Number of storms per year: Calculated and sorted to identify chronological trends.
Pivot Table: Summarized storm counts for each year and subbasin.


