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
    maximum = max(list_size)

    for station in data:
        station[2] = 30*math.pow(station[2]/maximum,0.7)


markers ={
    "ccgt":("c^","Cycle combiné"),
    "coal":("ko","Charbon"),
    "coal + biomass":("ro","Charbon + Biomasse"),
    "gas chp":("mo","Gaz (cogénération)"),
    "agr":("go","Nucléaire"),
}



data = get_data.get_data_plants()

data = sorted(data,key=lambda x: x[2],reverse=True)
scale_size(data)

fig, ax = plt.subplots(figsize=(10,20))

m = Basemap(resolution=None, # c, l, i, h, f or None
            projection='merc',
            lat_0=-1.945, lon_0=52.875,
            llcrnrlon=-5.79, llcrnrlat= 49.94, urcrnrlon=1.9, urcrnrlat=55.81, epsg=27700)

list_plots = []
for station in data:
    x,y = m(station[0][1],station[0][0])
    elt = m.plot(x,y ,markers[station[1]][0],label=markers[station[1]][1], markersize=station[2], markeredgecolor="#444444")
    list_plots.append(elt[0])

list_plots.reverse()
list_labels = []
list_handles = []
for elt in list_plots:
    if not elt.get_label() in list_labels:
        list_labels.append(elt.get_label())
        list_handles.append(elt)


m.drawmapboundary(fill_color='#46bcec')
# m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
# m.drawcoastlines()
m.arcgisimage(service='World_Imagery', xpixels = 1000, verbose= False)
# m.drawrivers()    
plt.title("20 plus grandes centrales électrique d'Angleterre")


plt.legend(handles=list_handles,numpoints=1,loc='center left', bbox_to_anchor=(1, 0.5),title="Légende",edgecolor="black",labelspacing=1, borderpad=1,fancybox=False)
plt.show()