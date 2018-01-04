"""
    Affiche les centrales électriques sur une carte
    du royaume uni
"""
import matplotlib.pyplot as plt
import matplotlib.cm
 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

fig, ax = plt.subplots(figsize=(10,20))

m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=54.485, lon_0=-6.375,
            llcrnrlon=-10.72, llcrnrlat= 49.84, urcrnrlon=2.03, urcrnrlat=59.13)


m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
m.drawcoastlines()

plt.title('Power plants in the UK')
plt.show()