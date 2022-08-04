import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load data
Data = pd.read_csv('dr_groups[63]_zml.csv')

###################################################################################################################
# One plot
fig, ax = plt.subplots(figsize=(10,10), subplot_kw=dict(projection='polar'))

# Scale factor
sf = 20

# Scatterplot of the data on polar coordinates (theta in radians (this is the reason for the *np.pi/180) and r)
ax.scatter(sf*Data['RA']*np.pi/180, Data['zml'], s=10**(-0.4*Data['r_petro'])*1e6, alpha=0.8)

# Setting limits and ticks for the axes (the y-axis is the r-axis)
ax.set_ylim(0.0050, 0.015)
ax.set_yticks(np.arange(0.0050, 0.016, 0.005))
ax.set_xticks(sf*np.arange(154,  158.5, 1)*np.pi/180,np.arange(154,  158.5, 1))
ax.set_theta_offset(150*np.pi/180) # This offset is here to change the position of the slice
ax.set_thetamax(sf*158.5)
ax.set_thetamin(sf*154.5)

# The title of the plot
ax.set_title('',fontsize=17)

# To add the axis labels. I use the 'text' function because I want the r-axis label to be rotated and I think there is no 'ax.set_thetalabel', so you have to do this to label the theta axis
# The coordinates on the 'text' function are theta (in radians) and r.
ax.text(sf*159*np.pi/180, 0.01, 'Redshift', ha='center', va='center', rotation=80,fontsize=15)
ax.text(sf*156.5*np.pi/180, 0.016, 'RA (deg)', ha='center', va='center', rotation=-55,fontsize=15)

# Grid
ax.grid(True)

plt.show()