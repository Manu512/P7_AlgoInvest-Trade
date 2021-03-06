""" bruteforce.py """
import csv
import os
import time
import itertools as it

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
        file = 'action.csv'

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
        self.taux = float(str(args[2]).replace('%', ''))
        self.profit = round(self.value * self.taux / 100, 2)

    def __repr__(self):
        return "{}".format(self.name)

    def __lt__(self, other):
        return self.taux < other.taux

    def __gt__(self, other):
        return self.taux > other.taux


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
        for combination in it.combinations(data, n):
            somme = 0
            profit = 0
            for action in combination:
                somme = somme + action.value
                profit = profit + action.profit
            if somme <= investissement:
                liste.append((combination, somme, profit))
    liste.sort(key=lambda x: x[2], reverse=True)
    return liste[:5]


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
    proposition = bruteforce(action, 500)
    stop = time.time()
    duree = stop - start
    affichage(proposition, duree)

main()
