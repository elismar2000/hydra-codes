import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
Data = pd.read_csv('Results/MDN/Galaxies/2022-02-21/13h01m.KFold.4x160_700_8192/Results_DF.csv')

###################################################################################################################
# One plot
fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(projection='polar'))

# Scatterplot of the data on polar coordinates (theta in radians (this is the reason for the *np.pi/180) and r)
ax.scatter(Data['RA']*np.pi/180, Data['z'], s=1, alpha=0.2)

# Setting limits and ticks for the axes (the y-axis is the r-axis)
ax.set_ylim(0, 0.3)
ax.set_yticks(np.arange(0, 0.4, 0.1))
ax.set_theta_offset(45*np.pi/180) # This offset is here to change the position of the slice
ax.set_thetamax(-53)
ax.set_thetamin(60)

# This line is here to add space to the r-axis labels. For some reason the default behaviour is to put the labels too close to the edge of the plot
ax.set_yticklabels(['%.1f      ' %s for s in np.arange(0, 0.4, 0.1)], verticalalignment='center')

# The title of the plot
ax.set_title('Sample with z')

# To add the axis labels. I use the 'text' function because I want the r-axis label to be rotated and I think there is no 'ax.set_thetalabel', so you have to do this to label the theta axis
# The coordinates on the 'text' function are theta (in radians) and r.
ax.text(70*np.pi/180, 0.15, 'Redshift', ha='center', va='center', rotation=105)
ax.text(0, 0.33, 'RA (deg)', ha='center', va='center', rotation=-45)

# To disable the grid
ax.grid(False)

plt.show()

###################################################################################################################
# Two polar plots in one figure. The code is the same as before, but in this case I changed the r-axis label a bit.
fig, ax = plt.subplots(1, 2, figsize=(12,12), subplot_kw=dict(projection='polar'))
plt.subplots_adjust(wspace=0.3)

ax[0].scatter(Data['RA']*np.pi/180, Data['z'], s=1, alpha=0.2)
ax[0].set_ylim(0, 0.3)
ax[0].set_yticks(np.arange(0, 0.4, 0.1))
ax[0].set_theta_offset(45*np.pi/180)
ax[0].set_thetamax(-53)
ax[0].set_thetamin(60)
ax[0].set_yticklabels(['%.1f      ' %s for s in np.arange(0, 0.4, 0.1)], verticalalignment='center')
ax[0].set_title('Sample with z')
ax[0].text(80*np.pi/180, 0.15, 'Redshift', ha='center', va='center', rotation=100)
ax[0].text(0, 0.35, 'RA (deg)', ha='center', va='center', rotation=-45)

ax[1].scatter(Data['RA']*np.pi/180, Data['zml'], s=1, alpha=0.2)
ax[1].set_ylim(0, 0.3)
ax[1].set_yticks(np.arange(0, 0.4, 0.1))
ax[1].set_theta_offset(45*np.pi/180)
ax[1].set_thetamax(-53)
ax[1].set_thetamin(60)
ax[1].set_yticklabels(['%.1f      ' %s for s in np.arange(0, 0.4, 0.1)], verticalalignment='center')
ax[1].set_title('Sample with zml')
ax[1].text(80*np.pi/180, 0.15, 'Redshift', ha='center', va='center', rotation=100)
ax[1].text(0, 0.35, 'RA (deg)', ha='center', va='center', rotation=-45)

ax[0].grid(False)
ax[1].grid(False)

plt.show()