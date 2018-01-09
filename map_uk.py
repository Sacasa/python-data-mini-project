"""
    Affiche les centrales électriques sur une carte
    du royaume uni
"""
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mplines
from mpl_toolkits.basemap import Basemap

import get_data_power_plants as get_data

MARKERS = {
    "ccgt":("c^", "Cycle combiné"),
    "coal":("ko", "Charbon"),
    "coal + biomass":("ro", "Charbon + Biomasse"),
    "gas chp":("mo", "Gaz (cogénération)"),
    "agr":("go", "Nucléaire"),
}

def create_legend(marker):
    """
        Crée la légende à partir des marqueurs
    """
    list_handles = []
    for elt in marker.values():
        point = mplines.Line2D([0], [0], marker=elt[0][1], markerfacecolor=elt[0][0], markersize=16,
                               label=elt[1], markeredgecolor="#444444", linewidth=0)
        list_handles.append(point)

    plt.legend(handles=list_handles, numpoints=1, loc='center left', bbox_to_anchor=(1, 0.5),
               title="Légende", edgecolor="black", labelspacing=1, borderpad=1, fancybox=False)



def scale_size(data):
    """
        Met les données à l'échelle afin de permettre un meilleur affichage
        car les données varient beaucoup
    """

    list_size = [station[2] for station in data]
    maximum = max(list_size)

    for station in data:
        station[2] = 30*math.pow(station[2]/maximum, 0.7)


def main():
    """
        Récupère les données puis les traites et les affiche
        sur une carte
    """
    data = get_data.get_data_plants()

    #On tri ici les données pourafficher les plus grandes en premier
    #ce qui évite de masquer les petites
    data = sorted(data, key=lambda x: x[2], reverse=True)
    scale_size(data)

    plt.subplots(figsize=(10, 20))

    map_plot = Basemap(resolution=None, # c, l, i, h, f or None
                       projection='merc',
                       lat_0=-1.945, lon_0=52.875,
                       llcrnrlon=-5.79, llcrnrlat=49.94, urcrnrlon=1.9, urcrnrlat=55.81, epsg=27700)

    for station in data:
        x_values, y_values = map_plot(station[0][1], station[0][0])
        map_plot.plot(x_values, y_values, MARKERS[station[1]][0], label=MARKERS[station[1]][1],
                      markersize=station[2], markeredgecolor="#444444")

    map_plot.drawmapboundary(fill_color='#46bcec')
    map_plot.arcgisimage(service='World_Imagery', xpixels=1000, verbose=False)
    plt.title("20 plus grandes centrales électrique d'Angleterre")
    create_legend(MARKERS)
    plt.show()

if __name__ == "__main__":
    main()
