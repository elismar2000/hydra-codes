import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.style.use('seaborn-talk')

zspec_table = pd.read_csv("ALL_Spec_Only_V7_Aper6_CCM89.csv")
hydra_table = pd.read_csv("Fields/Hydra.csv")

ra = hydra_table["RA"]
dec = hydra_table["DEC"]
g_petro = hydra_table["g_petro"]
r_petro = hydra_table["r_petro"]
zml = hydra_table["zml"]

class_ = zspec_table["class_Spec"]


#Defining the center of Hydra (in degress)
ra_0 = 159.17
dec_0 = -27.524

#Defining the radius of 1R200 around the center (in degrees)
#R200 = 1.4Mpc + scale of 0.247 Kpc/" ==> radius = 1.5744º
radius = 1.5744

def dist(ra, dec):
    return np.sqrt((ra - ra_0)**2 + (dec - dec_0)**2)

#Defining a mask for the objects inside 1R200
# distances = dist(ra, dec)
# mask1 = (distances < radius)

mask = (r_petro < 16) & (zml > 0.0) & (zml < 0.03) & (class_ == 'GALAXY')
mask_bright = (r_petro < 8) & (class_ == 'GALAXY')

from mpl_toolkits.axes_grid1 import make_axes_locatable
fig = plt.figure(figsize=(10, 10))
cm = plt.cm.get_cmap('Spectral')

ax0 = fig.add_subplot(111)
sc0 = ax0.scatter(x=ra[mask], y=dec[mask], c=r_petro[mask], cmap=cm, s=(1/r_petro[mask])*300)
sc1 = ax0.scatter(x=ra[mask_bright], y=dec[mask_bright], marker='h', color='red')
ax0.set_ylabel("DEC")
ax0.set_xlabel("R.A.")
ax0.set_title(r"r_petro < 16, $0.0 < photo_z < 0.03$")

divider = make_axes_locatable(ax0)
cax1 = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(sc0, cax=cax1, orientation='vertical', label='r_petro')

FiveR200 = plt.Circle((ra_0, dec_0), 5*radius, linestyle='--', edgecolor='red', facecolor="None", lw=2, label=r'$5 r_{200} = 7.872^{\circ}$')
ax0.add_patch(FiveR200)

OneR200 = plt.Circle((ra_0, dec_0), radius, linestyle='-', edgecolor='red', facecolor="None", lw=2, label=r'$1 r_{200} = 1.5744^{\circ}$')
ax0.add_patch(OneR200)

plt.show()
