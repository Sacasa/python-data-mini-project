"""
    Les données traitées sont ici le nombre de grammes de CO2
    produit pour la production d'un kWh d'électricité au
    Royaume Uni.
    Ce module a pour but de récupérer les données depuis septembre
    2017 puis deles afficher.
"""

import datetime
import requests
import matplotlib.pyplot as plt

def get_data(tab_urls):
    """
        Récupère les données aux url dans tab_urls et les convertit
        en JSON
    """
    headers = {
        'Accept': 'application/json'
    }
    total = []

    for url in tab_urls:
        total += requests.get(url, params={}, headers=headers).json()['data']

    return total

def is_week_day(date):
    """
        Retourne si une date est un jour de la semaine ou non
    """
    year, month, day = (int(x) for x in date.split("-"))
    ans = datetime.date(year, month, day)
    return ans.weekday() <= 5

def plot_scales(tab, fig, x_label, y_label, titre):
    """
        Paramètres:
            tab : tableau de mesures
            fig: figure sur laquelle afficher le graph
            x: libellé de l'axe x
            y: libellé de l'axe y
            titre: titre du graphique
        Va afficher avec pyplot un histogramme des données étudiées
    """
    maximum = float(max(tab))
    list_low = [x for x in tab if x <= 200]
    list_moderate = [x for x in tab if x <= 300 and x > 200]
    list_high = [x for x in tab if x <= 400 and x > 300]
    list_veryhigh = [x for x in tab if x > 400]

    bins = list(range(min(tab), max(tab), 10))
    plt.hist(list_low, bins=bins, color="#33cc33", label="Très faible", edgecolor="#006600")
    plt.hist(list_moderate, bins=bins, color="yellow", label="Modéré", edgecolor="#cccc00")
    plt.hist(list_high, bins=bins, color="orange", label="Elevé", edgecolor="#e65c00")
    plt.hist(list_veryhigh, bins=bins, color="red", label="Très élevé", edgecolor="#cc0000")

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Impact environnemental de la production d'électricité\nau Royaume Uni "+titre+\
        " entre le 26/09/17 et le 19/12/17")
    plt.legend()
    fig.show()

def main():
    """
        Fonction principale qui va récupérer les données puis les traiter
        et enfin les afficher.
    """
    urls = [
        'https://api.carbonintensity.org.uk/intensity/2017-11-29/2017-12-19',\
        'https://api.carbonintensity.org.uk/intensity/2017-11-08/2017-11-28',\
        'https://api.carbonintensity.org.uk/intensity/2017-10-18/2017-11-07',\
        'https://api.carbonintensity.org.uk/intensity/2017-09-27/2017-10-17',\
        'https://api.carbonintensity.org.uk/intensity/2017-09-12/2017-09-26'
    ]

    total = get_data(urls)

    output_list = [(int(x['from'][11:13]), x['intensity']['actual']) \
                  if x['intensity']['actual'] != None \
                  else (int(x['from'][11:13]), x['intensity']['forecast']) for x in total]

    day_list = [(x['from'][0:10], x['intensity']['actual']) \
               if x['intensity']['actual'] != None \
               else (x['from'][0:10], x['intensity']['forecast']) for x in total]


    list_semaine = [x[1] for x in day_list if is_week_day(x[0])]
    list_weekend = [x[1] for x in day_list if not is_week_day(x[0])]

    list_jour = [x[1] for x in output_list if x[0] >= 8 and x[0] < 20]
    list_nuit = [x[1] for x in output_list if x[0] < 8 or x[0] >= 20]

    #------------------------------------------

    nuit = plt.figure(1)
    plot_scales(list_nuit, nuit, "Facteur d'émission de C02(gCO2.kWh)", \
                'Nombre de fois atteint', "la nuit")

    #------------------------------------------

    jour = plt.figure(2)
    plot_scales(list_jour, jour, "Facteur d'émission de C02(gCO2.kWh)", \
                'Nombre de fois atteint', "le jour")

    #------------------------------------------

    semaine = plt.figure(3)
    plot_scales(list_semaine, semaine, "Facteur d'émission de C02(gCO2.kWh)", \
                'Nombre de fois atteint', "la semaine")

    #------------------------------------------

    weekend = plt.figure(4)
    plot_scales(list_weekend, weekend, "Facteur d'émission de C02(gCO2.kWh)", \
                'Nombre de fois atteint', "le week-end")

    input()

if __name__ == '__main__':
    main()
