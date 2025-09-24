# 🌍 Exoplanets

### ✨ Welcome to my first Exploratory Data Analysis (EDA) project!

---

## 📌 Project Overview

This small but focused Exploratory Data Analysis project aims to investigate which known exoplanets might be potentially habitable based on their features. The analysis leverages astrophysical principles and machine learning (KNN Imputation) to handle missing data and calculate criteria such as habitability zones.

The end goal is to propose a shortlist of candidate planets (about a dozen or fewer) that could benefit from further investigation.

---

## 🧪 Setup & Requirements

### 📂 Required Files

- `confirmed_exoplanets.csv` – the dataset used for analysis
- `main.py` – performs core analysis and visualizations
- `def_plots.py` - custom scatter & bar plot functions
- `facilities.py` – evaluates observatory performance
- `super_earth.py` – identifies “super Earth” candidates

### 📦 Required Libraries

Make sure the following Python libraries are installed:

- `pandas >= 2.2.3`
- `matplotlib >= 3.10.3`
- `numpy >= 2.2.6`
- `seaborn >= 0.13.2`
- `scikit-learn >= 1.6.1`

> ⚠️ Older versions **may** work, but compatibility is not guaranteed.

---

## 🧠 Script Breakdown

### `main.py`
This is the core of the analysis:
- Cleans and preprocesses the dataset
- Handles missing values with **KNN imputation**
- Calculates **stellar luminosity** and **habitable zones**
- Flags potentially habitable planets
- Generates key plots

### `def_plots.py`
Clears up space in main.py by defining plots
- Makes these plots reusable to avoid code duplication
- Makes main.py more readable

### `facilities.py`
Assesses the performance of different observatories:
- Measures each facility’s contribution to discovering habitable planets
- Calculates a custom “observation score”
- Tracks discovery trends over time

### `super_earth.py`
Classifies exoplanets into “super Earth” candidates based on:
- Orbital distance
- Stellar temperature
- Planetary mass, size, and density
- Orbital eccentricity

> **Why include this?** Because identifying super Earths could complement the search for habitability — and, honestly, it just seemed like a good idea.

---

## 📊 Sample Outputs

- Count and list of potentially habitable exoplanets
- Visualizations of temperature vs. orbital distance
- Top-performing observatories based on accuracy and discovery rate
- Year-over-year success trends
- List of “super Earth” exoplanets
- A list of final candidates to further examine

---

## 📍 Notes

- All physical thresholds (like what counts as "habitable" or "super Earth") are based on research and real astrophysics sources.
- Missing values in key features are imputed using **KNN**, but flagged for transparency.
- This project focuses more on **exploratory insights** than definitive claims.

---

## 📊 Data source
- NASA's Exoplanet Archive: https://dataherb.github.io/flora/nasa_exoplanet_archive/

---

## 💬 Final Thoughts

This project was created to practice and showcase foundational data science skills, domain research, and effective data storytelling.



