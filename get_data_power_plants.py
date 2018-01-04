"""
    Ce module a pour but de récupérer la liste des centrales
    electriques au Royaume Uni puis de préparer ces donnés
    pour pour les afficher sur une carte en fonction
    de leur type et capacité.
"""
import urllib.request
from bs4 import BeautifulSoup

def print_station_tri(station):
    """
        Affiche une station lorsque le traitement est finit
    """
    print("Coordinates : ", station[0])
    print("Type: ", station[1])
    print("Capacity (MW) : ", station[2])
    print("===================================================")

def parse_html(html_data):
    """
        Récupère les tables contenant les données utiles
        présentes sur la page.
        Puis, à partir de chaque ligne (et donc colonne)
        va créer une liste qui correspondra à une station
        le tout est ensuite mis dans la liste des stations
        qui sera retournée ensuite
    """

    soup = BeautifulSoup(html_data, 'html.parser')
    raw_list = []
    station = []

    for table in soup.find_all("table", {"class": "wikitable sortable"}):
        for row in table.find_all("tr"):
            for column in row.find_all("td"):
                station.append(column.text)

            if station != []:
                raw_list.append(station)
                station = []
    return raw_list


def filter_coordinates(liste_stations):
    """
        Sert à filtrer les coordonnées afin qu'elle soit exploitable.
        Les données sont converties au format (°N,°E)
    """
    for station in liste_stations:
        coords = station[1].split("/")[1][1:-1].split(" ")
        coords[0] = float(coords[0][1:-3])
        coords[1] = -float(coords[1][:-3]) if coords[1][-2] == "W" \
                  else float(coords[1][:-3])

        station[1] = (coords[0], coords[1])

def filter_open(liste_stations):
    """
        Retourne la liste des stations ouvertes/en activité
    """
    return [station for station in liste_stations \
            if not (station[9] or station[8] or station[7] == "TBD" or station[1] == '')]

def get_usefull_data(liste):
    """
        Retourne une liste contenant seuls les élements intéressants:
        Coordonnées, type, capacité de production
    """
    prepared_list = []
    for station in liste:
        prepared_list.append([station[1], station[5].lower(), float(station[6])])

    return prepared_list

def filter_out_small_plants(liste):
    """
        Retourne les stations sans celle ayant une capacité de moins
        de 10 MW
    """
    return [station for station in liste if station[2] > 10.0]


def main():
    """
        Fonction principale qui va récupérer les données puis tout trier
    """
    url = "https://en.wikipedia.org/wiki/List_of_power_stations_in_England"
    url_data = urllib.request.urlopen(url)
    data = url_data.read().decode('utf8')

    counter = 0

    raw_list = parse_html(data)
    filtered_open_list = filter_open(raw_list)
    filter_coordinates(filtered_open_list)
    prepared_data = get_usefull_data(filtered_open_list)
    prepared_data = filter_out_small_plants(prepared_data)

    for station in prepared_data:
        print_station_tri(station)
        counter += 1

    print("Il y a {} power stations".format(counter))

if __name__ == "__main__":
    main()
