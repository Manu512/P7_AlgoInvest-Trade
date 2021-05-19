""" bruteforce.py """
import csv
import os
import time
from itertools import combinations

PLACEMENT_MAX = 500

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
              'dataset1_Python+P7.csv]:')
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
                        self.actions.append(Action(action))
                    except ValueError:
                        pass
        else:
            print("Le fichier n'existe pas")

        return self.actions


class Action:
    """
    Class permettant d'instancer une action
    """

    def __init__(self, args: list):
        """
        :param args : liste qui contient : name:str, value:float, taux:float
        """
        self.name = args[0]
        self.value = float(args[1])
        self.taux = float(str(args[2]).replace('%', ''))
        self.profit = round(self.value * self.taux / 100, 2)

    def __repr__(self):
        return "{}".format(self.name)

    def __lt__(self, other):
        return self.profit < other.profit

    def __gt__(self, other):
        return self.profit > other.profit


def bruteforce(data: list, investissement: float):
    """
    methode de bruteforce pour tester toutes les combinaisons possibles.
    complexité O(2^n)
    :param data: liste d'action contenant 4 attributs (name, value, taux, profit)
    :param investissement: montant d'investissement
    :return: un tuple composé d'un tuple de 5 proposition d'investissement, le montant placé, le profit
    """

    liste = []
    for n in range(1, len(data) + 1):
        for combination in combinations(data, n):
            somme = 0
            profit = 0
            for action in combination:
                somme = somme + action.value
                profit = profit + action.profit
            if somme <= investissement:
                liste.append((combination, somme, profit))
    liste.sort(key=lambda x: x[2], reverse=True)
    return liste[:5]


def optimized(data: list, investissement: float):
    liste = []
    profit, somme = 0, 0

    data.sort(reverse=True)
    remain = investissement
    for i in range(0, len(data)):
        if data[i].value > 0:
            if remain - data[i].value <= 0:
                pass
            else:
                remain = remain - data[i].value
                liste.append(data[i])

    for action in liste:

        somme = somme + action.value
        profit = profit + action.profit
    var = [0]
    var[0] = liste, somme, profit
    return var


def affichage(data, data_time=None):
    """
    Fonction permettant la gestion de l'affichage.
    :param data_time: temps pour le traitement
    :param data: donnée venant de l'algorithme
    """
    print('------------------------------------------------------------')
    print('------------------------ Bruteforce ------------------------')
    print('------------------------------------------------------------')

    print('La meilleur proposition est la suivante : {0}\nAvec une dépense totale de : {1:.2f} \nAvec un profit '
          'espéré de : {2:.2f}'.format(data[0][0], data[0][1], data[0][2]))
    print('------------------------------------------------------------')
    print('Calculé en {0:.2f} secondes'.format(data_time))


def main():
    action = Data().load_actions()
    start = time.time()
    # proposition = optimized(action, 500)
    proposition = bruteforce(action, 500)
    stop = time.time()
    duree = stop - start
    affichage(proposition, duree)

main()
