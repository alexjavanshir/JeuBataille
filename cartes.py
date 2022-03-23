from random import *

class Carte:
    """Une classe carte rudimentaire définie par \n
        - sa valeur : 1 à 10, Valet, Dame, Roi\n
        - sa couleur : Carreau, Coeur, Pique, Trèfle\n
        - sa figure (le nom du fichier image correspondant)"""

    __valeur = 0
    __couleur = 0
    __figure = ""

    def __init__(self, valeur, couleur):
        """String*String->Carte
        Construit l'objet Carte avec la valeur et la couleur fournclearie"""
        self.Attribuer_Valeur(valeur)
        self.Attribuer_Couleur(couleur)
        self.__Attribuer_Figure(self.__valeur, self.__couleur)

    def Obtenir_Valeur(self):
        """None->String
        Retourne la valeur de la carte"""
        if self.__valeur < 11:
            return str(self.__valeur)
        elif self.__valeur == 11:
            return "Valet"
        elif self.__valeur == 12:
            return "Dame"
        elif self.__valeur == 13:
            return "Roi"

    def Obtenir_Couleur(self):
        """None->String
        retourne la couleur de la carte"""
        if self.__couleur == 1:
            return "Carreau"
        elif self.__couleur == 2:
            return "Coeur"
        elif self.__couleur == 3:
            return "Pique"
        else:
            return "Trèfle"

    def Obtenir_Figure(self):
        """None->String
        Retourne le nom du fichier image correspondant à la carte"""
        return self.__figure

    def Attribuer_Valeur(self, valeur):
        """String->None
        Change la valeur de la carte"""
        if valeur == "Valet":
            self.__valeur = 11
        elif valeur == "Dame":
            self.__valeur = 12
        elif valeur == "Roi":
            self.__valeur = 13
        else:
            self.__valeur = int(valeur)
        self.__Attribuer_Figure(self.__valeur, self.__couleur)

    def Attribuer_Couleur(self, couleur):
        """String->None
        Change la couleur de la carte"""
        if couleur == "Carreau":
            self.__couleur = 1
        elif couleur == "Coeur":
            self.__couleur = 2
        elif couleur == "Pique":
            self.__couleur = 3
        else:
            self.__couleur = 4
        self.__Attribuer_Figure(self.__valeur, self.__couleur)

    def __Attribuer_Figure(self, valeur, couleur):
        """String*String->None
        Attribue le fichier image en fonction de la valeur et de la couleur"""
        self.__figure = str(self.__valeur*10+self.__couleur)+".jpg"

    def __repr__(self):
        """None->None
        Permet d'afficher la carte lors de l'appel par print"""
        return "le {0} de {1}".format(self.Obtenir_Valeur(), self.Obtenir_Couleur())

    def __eq__(self, carte):
        return ((self.Obtenir_Couleur() == carte.Obtenir_Couleur()) and (self.Obtenir_Valeur() == carte.Obtenir_Valeur()))


class Paquet:

    def __init__(self, nb_carte):
        self.__deck = []
        self.__nb_carte = nb_carte

        couleurs = ["Carreau", "Coeur", "Pique", "Trefle"]
        valeurs = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]

        if self.__nb_carte == 52:
            for couleur in couleurs:
                for valeur in valeurs:
                    self.__deck.append(Carte(valeur, couleur))

        elif self.__nb_carte == 32:
            valeurs = ["1", "7", "8", "9", "10", "Valet", "Dame", "Roi"]
            for couleur in couleurs:
                for valeur in valeurs:
                    self.__deck.append(Carte(valeur, couleur))
        else:
            while len(self.__deck) < nb_carte:
                rand_card = randint(0,len(couleurs)-1), randint(0,len(valeurs)-1)
                rand_couleur = rand_card[0]
                rand_valeur = rand_card[1]

                new_card = Carte(valeurs[rand_valeur], couleurs[rand_couleur])
                if not self.Carte_Existe(new_card):
                    self.__deck.append(Carte(valeurs[rand_valeur], couleurs[rand_couleur]))

                '''
                if rand_card not in all_rand_cards:
                    all_rand_cards.append(rand_card)
                    self.__deck.append(Carte(valeurs[rand_valeur], couleurs[rand_couleur]))
                else:
                    print("Duplicate")
                '''

    def Obtenir_nombre_cartes(self):
        return self.__nb_carte

    def Obtenir_cartes(self):
        return self.__deck

    def Carte_Existe(self, card):
        if len(self.__deck) > 0:
            for i in range(len(self.__deck)):
              if card.__eq__(self.__deck[i]):
                    return True
        return False




deck = Paquet(0)
question = int(input("Avec combien de carte souhaitez vous jouer ?\n"))
deck = Paquet(question)
deckfinale = deck.Obtenir_cartes()
print(deckfinale, "\n\n")

class Bataille : 
    def __init__(self):

    def melange_distribution():
        deck_melange = sample(deckfinale, len(deckfinale))
        moite = len(deck_melange)//2
        moite1 = deck_melange[:moite]
        moite2 = deck_melange[moite:]



