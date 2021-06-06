""" bruteforce.py """
import csv
import os
import time
from math import ceil

import logging

data_folder = "data/"


class Data:
    """
    Class instanciant le fichier de donnée
    """

    def __init__(self):
        self.actions = []

    def load_actions(self):
        """
        Methode qui va cherche le fichier à analyser
        """
        print('Saisir le nom du fichier à analyser [action.csv si vide][1 = dataset1_Python+P7.csv][2 = '
              'dataset2_Python+P7.csv]:')
        file = input('---->')
        if file == '':
            file = 'action.csv'
        elif file == "1":
            file = 'dataset1_Python+P7.csv'
        elif file == "2":
            file = 'dataset2_Python+P7.csv'

        file_to_open = data_folder + file

        if os.path.exists(file_to_open):
            print('Chargement de : {}'.format(file_to_open))
            with open(file_to_open, newline='') as csvfile:
                actions = csv.reader(csvfile, delimiter=',')
                for action in actions:
                    try:
                        var = Action(action)
                        if isinstance(var, Action):
                            self.actions.append(var)
                    except ValueError as e:
                        pass
        else:
            print("Le fichier n'existe pas")
            return False

        return self.actions


class Action:
    """
    Class permettant d'instancer une action
    """

    def __new__(cls, args):
        """

        :param args:
        """
        # TODO : ne pas instancier si profit < 0.
        if args[2]:
            taux = float(str(args[2]).replace('%', ''))
            if taux > 0 and float(args[1]) > 0:
                return super(Action, cls).__new__(cls)

    def __init__(self, args: list):
        """
        :param args : liste qui contient : name:str, value:float, taux:float
        """
        self.name = args[0]
        self.value = float(args[1])
        self.value2 = ceil(self.value)
        self.taux = float(str(args[2]).replace('%', ''))
        self.profit = round(self.value * self.taux / 100, 2)

    def __repr__(self):
        return "{}".format(self.name)


def optimized(data: list, investissement: float):
    gestion_cents = False
    if gestion_cents:
        facteur = int(100)
    else:
        facteur = int(1)

    investissement = int(investissement * facteur)

    matrice = [[0 for x in range(investissement + 1)] for x in range(len(data) + 1)]

    for w in range(1, investissement + 1):
        for i in range(1, len(data) + 1):  # parcours des actions
            # parcours du montant a investir (*100 pour gérer les centimes)
            valeur_action = int(data[i - 1].value2 * facteur)
            if valeur_action <= w:  # si il me reste des fonds pour investir/acheter l'action je
                # verifie si j'augmente mon profit en achetant celle ci.
                matrice[i][w] = max(data[i - 1].profit + matrice[i - 1][int(w - valeur_action)], matrice[i - 1][w])
            else:
                matrice[i][w] = matrice[i - 1][w]

    # retrouver les éléments en fonction de la somme
    w = investissement
    n = len(data)
    data_selection = []

    while w >= 0 and n >= 0:
        valeur_action = int(data[n - 1].value2 * facteur)  # valeur de l'action * 100 pour les centimes.
        d = data[n - 1].profit  # Valeur du profit
        if matrice[n][w] == matrice[n - 1][w - valeur_action] + d:
            data_selection.append(data[n - 1])
            w -= valeur_action
        n -= 1

    t = sum([v.value for v in data_selection])

    return data_selection, t, matrice[-1][-1]


def glouton(data: list, investissement: float):
    """
    Methode naive pour l'achat d'actions
    :param data: liste d'action contenant 4 attributs (name, value, taux, profit)
    :param investissement: montant d'investissement
    :return: un tuple composé d'un tuple de 5 proposition d'investissement, le montant placé, le profit
    """
    liste = []
    profit, somme = 0, 0

    data.sort(reverse=True)
    remain = investissement
    for i in range(0, len(data)):
        if (data[i].value > 0) and (data[i].profit > 0) and remain - data[i].value > 0:
            remain = remain - data[i].value
            liste.append(data[i])
            somme = somme + data[i].value
            profit = profit + data[i].profit

    return liste, somme, profit


def affichage(data, data_time=None):
    """
    Fonction permettant la gestion de l'affichage.
    :param data_time: temps pour le traitement
    :param data: donnée venant de l'algorithme
    """
    print('------------------------------------------------------------')
    print('------------------------ Optimized ------------------------')
    print('------------------------------------------------------------')

    print('La meilleur proposition est la suivante :')
    print(*data[0], sep="\n")
    print('Avec une dépense totale de : {0:.2f} \nAvec un profit '
          'espéré de : {1:.2f}'.format(data[1], data[2]))
    print('------------------------------------------------------------')
    print('Calculé en {0:.2f} secondes'.format(data_time))


def main():
    action = Data().load_actions()
    if action:
        start = time.time()
        proposition = optimized(action, 500)
        stop = time.time()
        duree = stop - start
        affichage(proposition, duree)


main()
