import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns; sns.set()

plt.style.use('seaborn-talk')

zspec_table = pd.read_csv("ALL_Spec_Only_V7_Aper6_CCM89.csv")

ra = zspec_table["RA"]
dec = zspec_table["DEC"]
z = zspec_table["z"]

#Defining the center of Hydra (in degress)
ra_0 = 159.17
dec_0 = -27.524

#Defining the radius of 1R200 around the center (in degrees)
#R200 = 1.4Mpc + scale of 0.247 Kpc/" ==> radius = 1.5744º
radius = 1.5744

def dist(ra, dec):
    return np.sqrt((ra - ra_0)**2 + (dec - dec_0)**2)

#Defining a mask for the objects inside 1R200
distances = dist(ra, dec)
mask1 = (distances < radius) & (z > 0.0) & (z < 0.05)
#mask2 = (z > 0.0) & (z < 0.05)

fig, axs = plt.subplots(1, 1, figsize=(10, 10))

hist = axs.hist(z[mask1], bins=30, color='darkorange')
axs.set_title("inside 1R200", fontsize=30)
axs.set_ylabel("Number of objects", fontsize=30)


# axs[1].hist(z[mask2], bins=50, color='darkorange')
# axs[1].set_title("zspecs for all objects")

# for i in range(2):
#     axs[i].set_xlabel("Spectroscopic redshift", fontsize=20)
#     axs[i].yaxis.set_tick_params(labelsize=10, width=3)
#     axs[i].xaxis.set_tick_params(labelsize=10, width=3)
#     axs[i].grid()

axs.set_xlabel("Spectroscopic redshift", fontsize=30)
axs.yaxis.set_tick_params(labelsize=20, width=3)
axs.xaxis.set_tick_params(labelsize=20, width=3)
axs.grid()

plt.show()
