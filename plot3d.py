import pickle
import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


df = pd.read_pickle("./processed_feature.pickle")

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = 'morning_ior'
y = 'evening_ior'
z = 'weekdayend_r'


xs = df[x]
ys = df[y]
zs = df[z]
ax.scatter(xs, ys, zs, c='b', marker='o')

for index, row in df.iterrows():
    print index, row['morning_ior']
    ax.text(row[x], row[y], row[z], index, size=8, zorder=1,
            color='k')

ax.set_xlabel(x)
ax.set_ylabel(y)
ax.set_zlabel(z)

plt.show()

