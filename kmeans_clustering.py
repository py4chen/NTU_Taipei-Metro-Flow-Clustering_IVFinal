from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

df = pd.read_pickle("processed_feature.pickle")

x = 'morning_ior'
y = 'evening_ior'
z = 'weekdayend_r'

X = df.as_matrix(columns=[x,y,z])

print X



kmeans = KMeans(n_clusters=4, random_state=0).fit(X)

print kmeans.labels_

df['class'] = kmeans.labels_

print df

# show df

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


plot_type = [{'c':'b'}, {'c':'g'},{'c':'r'},{'c': 'c'}, {'c': 'm'}, {'c': 'y'}, {'c':'k'}, {'c':'w'}]


for index, row in df.iterrows():
    ax.scatter([row[x]], [row[y]], [row[z]], c=plot_type[int(row['class'])]['c'], marker='o')
    ax.text(row[x], row[y], row[z], index, size=8, zorder=1,
            color='k')

ax.set_xlabel(x)
ax.set_ylabel(y)
ax.set_zlabel(z)

plt.show()



## write into metro_class.js

import json, io

d = {}
for index, row in df.iterrows():
    d[index] = [int(row['class']), row[x], row[y], row[z]]

print d

s = json.dumps(d, encoding='utf-8', ensure_ascii=False)
s = s.replace('"','')
print s

f = io.open("web/metroclass.js", mode="w", encoding='utf8')
f.write("var metroclass = " + s + ";")
