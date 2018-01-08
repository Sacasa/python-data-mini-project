"""
    Affiche les centrales électriques sur une carte
    du royaume uni
"""
import matplotlib.pyplot as plt
import matplotlib.cm
import math
 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

import get_data_power_plants as get_data

def scale_size(data):

    list_size = [station[2] for station in data]

    for station in data:
        station[2] = math.log(station[2]) + 10


markers ={
    "ccgt":"bo",
    "coal":"k^",
    "ocgt":"co",
    "coal + biomass":"ko",
    "gas chp":"mo",
    "oil, gas":"r^",
    "coal, oil + gas":"ro",
    "biomass":"yo",
    "agr":"go",
}

data = get_data.get_data_plants()

data = sorted(data,key=lambda x: x[2],reverse=True)
scale_size(data)

fig, ax = plt.subplots(figsize=(10,20))

m = Basemap(resolution='c', # c, l, i, h, f or None
            projection='merc',
            lat_0=-1.945, lon_0=52.875,
            llcrnrlon=-5.79, llcrnrlat= 49.94, urcrnrlon=1.9, urcrnrlat=55.81)

for station in data:
    x,y = m(station[0][1],station[0][0])
    m.plot(x,y , markers[station[1]], markersize=station[2])

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
m.drawcoastlines()

plt.title('Power plants in England producing morethan 100 MW')
plt.show()