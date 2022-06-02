import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('seaborn-talk')

hydra_table = pd.read_csv("Fields/Hydra.csv")

ra = hydra_table["RA"]
dec = hydra_table["DEC"]
zml = hydra_table["zml"]
g_petro = hydra_table["g_petro"]

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
mask1 = (distances < radius) & (zml > 0.0) & (zml < 0.1) & (g_petro < 18)
mask2 = (zml > 0.0) & (zml < 0.1)

fig, axs = plt.subplots(1, 2, figsize=(10, 10))

axs[0].hist(zml[mask1], bins=25, color='darkorange')
axs[0].set_title("Objects inside 1R200", fontsize=30)
axs[0].set_ylabel("Number of objects", fontsize=30)

axs[1].hist(zml[mask2], bins=25, color='darkorange')
axs[1].set_title("All objects", fontsize=30)

for i in range(2):
    axs[i].set_xlabel("Photo-z", fontsize=30)
    axs[i].yaxis.set_tick_params(labelsize=20, width=3)
    axs[i].xaxis.set_tick_params(labelsize=20, width=3)
    axs[i].grid()

plt.show()
