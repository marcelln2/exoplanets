from main import df

"""
What makes a planet habitable? (Approximations) (This results are for Super-Earth classifications)
- pl_orbsmax (Orbital Distance) 0.9-1.5 AU
- st_teff (Stellar Temperature) 4800K - 6300K (Sun-like stars)
- Planet size	pl_radj	0.5 – 2.0 Jupiter radii (Earth ≈ 0.089)
- Planet mass	pl_bmassj	0.01 – 0.1 Jupiter mass (Earth ≈ 0.003)
- Density	pl_dens	3 – 8 g/cm³ (Earth ~5.5 g/cm³)
- Eccentricity	pl_orbeccen	< 0.3 (stable orbit)
# Classify super earths, then make a small list of planets that are super earths.
"""

df['Super_Earth'] = (
    (df['Orbital_Distance'].between(0.02, 1.5)) &
    (df['Stellar_Temperature'].between(4800, 6300)) &
    (df['Planet_Size'].between(0.05, 0.2)) &
    (df['Planet_Mass'].between(0.002, 0.05)) &
    (df['Density'].between(3, 7.5)) &
    (df['Eccentricity'] <= 0.3)
) # Replaced apply with this. Should be much faster now.

df_SE = df[df['Super_Earth'] == True]
planet_names = list(df_SE['Planet_Name'])
print('\n"Super Earth" like planets: ', end=' ')
print(*planet_names, sep=', ')