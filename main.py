import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from def_plots import bplot
from def_plots import splot

# Set so all columns are displayed when printed to avoid confusion.
pd.set_option('display.max_columns', None)

df = pd.read_csv('confirmed_exoplanets.csv').drop_duplicates()
df.rename(columns={'pl_name': 'Planet_Name', 'pl_orbsmax': 'Orbital_Distance', 'st_teff': 'Stellar_Temperature',
                   'pl_radj': 'Planet_Size', 'pl_bmassj': 'Planet_Mass', 'pl_dens': 'Density', 'pl_orbeccen': 'Eccentricity',
                   'rowupdate': 'Discovery_Time', 'pl_facility': 'Facility', 'st_mass': 'Stellar_Mass',
                   'st_rad': 'Stellar_Radius'},
          inplace=True)

# Proper renaming to avoid confusion
df = df[['Planet_Name', 'Facility', 'Discovery_Time', 'Stellar_Temperature', 'Stellar_Mass', 'Stellar_Radius',
         'Orbital_Distance', 'Planet_Size', 'Planet_Mass', 'Density', 'Eccentricity']]

# Predicted values will get a flag to make values (filled in by default) stand out.
df['Uncertain_Values'] = False
temp_na = df['Stellar_Temperature'].isna()
mass_na = df['Stellar_Mass'].isna()

# Predicting values of Star Mass and Temp using KNN
df_knn = df[['Stellar_Mass', 'Stellar_Temperature']].copy()
df_knn = df_knn.dropna(how='all', subset=['Stellar_Mass', 'Stellar_Temperature'])
imputer = KNNImputer(n_neighbors=6)
df_imputed = pd.DataFrame(imputer.fit_transform(df_knn), columns=df_knn.columns)
df[['Stellar_Mass', 'Stellar_Temperature']] = df_imputed[['Stellar_Mass', 'Stellar_Temperature']]

df['Uncertain_Values'] = temp_na | mass_na
df = df.dropna(subset=['Stellar_Mass', 'Stellar_Temperature', 'Stellar_Radius'])

# Calculate Luminosity and habitable zone (HZ) based off of the Stefan-Boltzmann law
df['Stellar_Luminosity'] = (df['Stellar_Radius'] ** 2) * (df['Stellar_Temperature'] / 5778) ** 4
"""
Explanation: 
Stefan-Boltzmann law: Luminosity = 4 * pi * Radius^2 * σ (S.B. constant) * Temperature^4
The luminosity of the compared star is = 4 * pi * R^2 * σ * T^4
The l. of the sun is =                   4 * pi * R^2 * σ * T^4
The radius is 1, as it's the sun, while the temperature is 5778 Kelvin. 4 * pi * σ cancel out.
Thus, the luminosity is = (R/1)^2 * (T/5778)^4
"""
df['Habitable_Zone_START_AU'] = np.sqrt(df['Stellar_Luminosity'] / 1.1)
df['Habitable_Zone_END_AU'] = np.sqrt(df['Stellar_Luminosity'] / 0.53)
# https://worldbuilding.stackexchange.com/questions/79646/what-is-the-habitable-zone-around-my-star

# True / False tag based off of whether the planet is inside the HZ
df['Potentially_Habitable'] = (
    (df['Habitable_Zone_START_AU'] <= df['Orbital_Distance']) &
    (df['Habitable_Zone_END_AU'] >= df['Orbital_Distance']))

print(f"\nNumber of Potentially Habitable planets: {df['Potentially_Habitable'].sum()}", end='\n\n')

# Define the potentially habitable planets in a new DF, EXCLUDING visualizations due to request.
df_HZ= df[(df['Potentially_Habitable'] == True) & (df['Uncertain_Values'] == False)]

# Relation between the temp of the star & the distance between the star and the exoplanet
splot(df_HZ, 'Orbital_Distance', 'Stellar_Temperature', 'Potentially habitable planets',
      None, "Orbital Distance (AU)", "Stellar Temperature (Kelvin)",
      'True, which = "both"')
# Showcasing a clear relation between these two values. (Proves how useful KNN is and how these 2 values are "correct")
splot(df_HZ, 'Stellar_Mass', 'Stellar_Temperature', 'Correlation between Stellar Temperature and Mass',
      'Stellar_Temperature', 'Stellar Mass (Relative to the sun)', 'Stellar Temperature (Kelvin)',
      'True, which = "both"')
# Barplots of stellar mass and temperature
bplot(df_HZ, 'Stellar_Mass', 'gray', '#61b4e4', 1.5, 'Stellar Mass (Relative to the sun)')
bplot(df_HZ, 'Stellar_Temperature', 'orange', '#344361', 1.5, 'Stellar Temperature (Kelvin)')

""" Due to missing values for a lot of planets, it is best if we drop them. 52 -> 6 planets
Let's sort this even further! The first one I would look at is Planet_Mass, which comes from pl_bmassj. 
This is mass in Jupiter. The ratio of jupiter/earth is 317,83. K538b has a planet mass of 0.03335.
Knowing this, the earth mass for the planet is around 10.6. However, according to NASA's own database,
Kepler-538 b's mass is 12.9 earths. At this scale, it's not a huge difference, but it does seem suspicious.
However, since I compared previous data as well with the CSV file, some numbers might be slightly 
incorrect. We have to accept this fact and continue working with it.
The second thing I would look at is density. For density, it's best if we look at three things first.
1. Why density? Because it is available, and is a fundamental part of discovering rocky, earth-like planets.
Since this, it has to be relatively close to Earth's value of 5.51. Also, density might reveal some details 
about a planet's composition (See resource at the bottom). 2. Earth's density: 5.51g/cm^3 3. A range must be calculated where planets 
in-between can continue to the next "step".
Luckily, a reddit user estimated the lower and higher end of these ranges based off of a youtube video (?)
that belongs to a channel which makes a lot of similar content in the topic of space, planets and systems.
(See the second resource below) This results in the following: min. d = 0.266 * earth, max = 3.2 * earth. 
(So 1.46566 and 17.632 respectively.)
"""

df_HZ = df_HZ.dropna()
# Due to the fact that K-539 b, the third planet is 0.97 jupiter mass and is a giant gas planet, it will be excluded.
df_HZ = df_HZ[(df_HZ['Density'] >= 1.46566) & (df_HZ['Density'] <= 17.632) & (df_HZ['Planet_Mass'] < 0.2)]
print('The final list of planets that should be examined further: ', end = '')
print(*df_HZ['Planet_Name'], sep = ', ')

"""
Reddit user's calculations: https://www.reddit.com/r/worldbuilding/comments/qhqwpa/comment/hiexilx/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
Density resource: https://astrobiology.nasa.gov/news/how-to-predict-the-make-up-of-rocky-exoplanets-too-small-and-distant-to-directly-observe/
Data source: https://dataherb.github.io/flora/nasa_exoplanet_archive/
"""