from main import df
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Amount of planets per facility
df_FL = df.groupby('Facility')['Planet_Name'].count().sort_values(ascending=False).reset_index()
df_FL.rename(columns={'Planet_Name': 'Planets'}, inplace=True)

# Calculate the amount of planets a facility has discovered to assess it's performance
df_ph = df[df['Potentially_Habitable'] == True]
possibly_habitable = df_ph.groupby('Facility')['Planet_Name'].count().reset_index()
possibly_habitable.rename(columns={'Planet_Name': 'Habitable_Planets'}, inplace=True)

df_FL = df_FL.merge(possibly_habitable, on='Facility')
df_FL['Habitable_Discovery'] = df_FL['Habitable_Planets'] / df_FL['Planets'] * 100
df_FL['Observation_Score'] = df_FL['Habitable_Discovery'] * df_FL['Habitable_Planets'] # Score: Accuracy (%) * Pot. h. planets (Number of.)
df_FL = df_FL[~df_FL['Facility'].isin(['Multiple Observatories', 'Multiple Facilities'])]
df_Best_Facility = df_FL.sort_values(by=['Observation_Score'], ascending=False)
df_Best_Facility = df_Best_Facility[:5]

plt.figure(figsize=[24, 7])
plt.bar(df_Best_Facility['Facility'], df_Best_Facility['Observation_Score'], color='green')
plt.title('(Relative) Score of facilities', fontsize=16)
plt.xlabel('Name of the Facility', fontsize=16)
plt.xticks(fontsize=15)
maxscore = np.round(max(df_Best_Facility['Observation_Score']), 0).astype(int) * 1.2
plt.yticks(ticks := np.arange(0, maxscore, 20), [f"{x}" for x in ticks], fontsize=15)
plt.show()

# Print the name of the facility, the accuracy and the amount of pot. hab. planets
for name, accuracy, amount, percentage in zip(df_Best_Facility['Facility'], df_Best_Facility['Observation_Score'], df_Best_Facility['Habitable_Planets'], df_Best_Facility['Habitable_Discovery']):
    print(f"{name} | Score: {accuracy:.2f}  | {amount} planet(s) | {percentage:.2f}% Accurate (Overall)") # 13.1242604409 times faster then the original iterrows

# Group a facilities' discoveries by year
df['Discovery_Year'] = pd.to_datetime(df['Discovery_Time']).dt.year
facility_year = df.groupby(['Facility', 'Discovery_Year']).agg(
    Total_Planets=('Planet_Name', 'count'),
    Habitable_Planets=('Potentially_Habitable', 'sum'),
).reset_index()

# Remove unintelligible entries (MOA, MFA), format accuracy as percentage, then sort by accuracy.
# (Accuracy must be > 0% & data from at least 2 years must be present)
facility_year = facility_year[~facility_year['Facility'].isin(['Multiple Observatories', 'Multiple Facilities'])]
facility_year['Accuracy'] = np.round((facility_year['Habitable_Planets'] / facility_year['Total_Planets'] * 100), 2)
facility_year = facility_year.sort_values(by='Accuracy', ascending=False)
facility_year = facility_year[facility_year['Accuracy'] > 0]
facility_year = facility_year.groupby('Facility').filter(lambda x: len(x) > 2) # Look into dif. type of visualization for lines (bar plot?)

# Plot each individual facility by year
plt.figure(figsize=[15, 8])
for facility in facility_year['Facility'].unique():
    subset = facility_year[facility_year['Facility'] == facility]
    data = subset.sort_values('Discovery_Year')

    plt.plot(data['Discovery_Year'], data['Accuracy'], label=facility)

    for year, amount in zip(data['Discovery_Year'], data['Habitable_Planets']):
        plt.text(year, amount + 3, amount, ha='center', va='bottom')

# Plot the chart with limits to ensure readability
plt.title('% of correct observations per facility', fontsize=16)
plt.xlabel('Discovery Year')
plt.ylabel('Accuracy (%)')
plt.yticks(ticks := np.arange(0, 21, 5), [f"{x}%" for x in ticks])
plt.grid(True, "both", linestyle='-', linewidth=0.15)
plt.ylim(0, facility_year['Accuracy'].max() + 5)
plt.legend(loc='upper left')
plt.show()