from random import *
import numpy as np
import time
import logging
import tkinter as tk
from PIL import Image, ImageTk
import pygame as pygame

#*************************************************************************
# Classe Paquet:
# Une carte est representé par sa valuer, sa figure et le fichier image
# le represantant.
# La classe offre divers methods pour comparer deux cartes entre elles
#*************************************************************************
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
        if self.__couleur == 0:
            return "Carreau"
        elif self.__couleur == 1:
            return "Coeur"
        elif self.__couleur == 2:
            return "Pique"
        elif self.__couleur == 3:
            return "Trèfle"

    def Obtenir_Code_Couleur(self):
        return self.__couleur

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
            self.__couleur = 0
        elif couleur == "Coeur":
            self.__couleur = 1
        elif couleur == "Pique":
            self.__couleur = 2
        elif couleur == "Trèfle":
            self.__couleur = 3
        self.__Attribuer_Figure(self.__valeur, self.__couleur)

    def __Attribuer_Figure(self, valeur, couleur):
        """String*String->None
        Attribue le fichier image en fonction de la valeur et de la couleur"""
        #self.__figure = str(self.__valeur*10+self.__couleur)+".jpg"
        self.__figure = f"{self.Obtenir_Valeur().lower()}-{self.Obtenir_Couleur().lower()}.png"

    def __repr__(self):
        """None->None
        Permet d'afficher la carte lors de l'appel par print"""
        return "{0}-{1}".format(self.Obtenir_Valeur(), self.Obtenir_Couleur())

    def __eq__(self, carte):
        return ((self.Obtenir_Couleur() == carte.Obtenir_Couleur()) and (self.Obtenir_Valeur() == carte.Obtenir_Valeur()))

    # Methodes pour comparer la valeur de la carte (self) par rapport a une autre passé en parametre d'entrée
    # La couleur ne compte pas dans ces comparaisons
    def __valeur_eq__(self, carte):
        return (self.__valeur == carte.__valeur)

    def __valeur_gt__(self, carte):
        if self.__valeur_eq__(carte):
            return False
        #L'As bat toute autre carte sauf en cas d'egalité avec un autre As
        if self.__valeur == 1:
            return True
        elif carte.__valeur == 1:
            return False
        else:
            return (self.__valeur > carte.__valeur)

    def __valeur_lt__(self, carte):
        if self.__valeur_eq__(carte):
            return False
        return not (self.__valeur_gt__(carte))

#*************************************************************************
# Classe Paquet:
# Un paquet est constinué de N cartes. Le constructeur prend en
# entrée le nombre de cartes du paquet que l'on désir créer
#*************************************************************************
class Paquet:

    def __init__(self, nb_cartes):
        self.__deck = []
        self.__nb_cartes = nb_cartes

        couleurs = ["Carreau", "Coeur", "Pique", "Trèfle"]
        valeurs = { 52: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"],
                    32: ["1", "7", "8", "9", "10", "Valet", "Dame", "Roi"] }

        if self.__nb_cartes in [32, 52]:
            for couleur in couleurs:
                for valeur in valeurs[self.__nb_cartes]:
                    self.__deck.append(Carte(valeur, couleur))
        else:
            while len(self.__deck) < nb_cartes:
                rand_couleur = randint(0,len(couleurs)-1)
                rand_valeur = randint(0,len(valeurs[52])-1)
                new_card = Carte(valeurs[52][rand_valeur], couleurs[rand_couleur])
                if not self.Carte_Existe(new_card):
                    self.__deck.append(Carte(valeurs[52][rand_valeur], couleurs[rand_couleur]))

    def Obtenir_nombre_cartes(self):
        return self.__nb_cartes

    def Obtenir_cartes(self):
        return self.__deck

    def afficher(self):
        print(self.Obtenir_cartes())

    def melanger(self):
        shuffle(self.Obtenir_cartes())

    def Carte_Existe(self, card):
        if len(self.__deck) > 0:
            for i in range(len(self.__deck)):
                if card.__eq__(self.__deck[i]):
                    return True
        return False

#*************************************************************************
# Classe Bataille:
# Classe definisaant le jeu ainsi que toutes les actions lié au jeu
#*************************************************************************
class Bataille:
    def __init__(self, nb_cartes):
        self.__paquet = Paquet(nb_cartes)
        self.__cartes_joueurs = {1:[], 2:[]}

    #-----------------------------------------------------------------------
    # Initialise un nouvelle partie
    #-----------------------------------------------------------------------
    def initialiser_partie(self):

        # Si en mode DEBUG on crée manuellement le jeu de chaque joueur
        # Sinon distribue la moitié du paquet de façon aléatoire à chaque joueur
        if DEBUG:
            self.__cartes_joueurs[1] = []
            self.__cartes_joueurs[2] = []
            couleurs = ["Carreau", "Coeur", "Pique", "Trèfle"]

            for valeur in ["5", "9", "Dame", "10", "4", "10"]:
                rand_couleur = randint(0,len(couleurs)-1)
                self.__cartes_joueurs[1].append(Carte(valeur, couleurs[rand_couleur]))

            for valeur in ["8", "9", "Dame", "10", "7", "2"]:

                rand_couleur = randint(0,len(couleurs)-1)
                self.__cartes_joueurs[2].append(Carte(valeur, couleurs[rand_couleur]))
        else:
            self.__paquet.melanger()
            paquet_complet = self.__paquet.Obtenir_cartes()

            #Distribuer la moité du paquet à chaque joueur
            index_milieu = len(paquet_complet) // 2
            self.__cartes_joueurs[1] = paquet_complet[:index_milieu]
            self.__cartes_joueurs[2] = paquet_complet[index_milieu:]

    #-----------------------------------------------------------------------
    # Entrée:
    # Sortie: Le paquet de cartes du jeu
    #-----------------------------------------------------------------------
    def obtenir_paquet(self):
        return self.__paquet

    #-----------------------------------------------------------------------
    # Entrée: Un numero de joueur (1 ou 2)
    # Sortie: La liste replresantant la carte du joueur passé en entrée
    #-----------------------------------------------------------------------
    def obtenir_cartes_joueur(self, joueur):
        return self.__cartes_joueurs[joueur]

    #-----------------------------------------------------------------------
    # Un tour de jeu: Prend en entrée la liste des cartes des deux joueurs
    # Compare la première carte, établie le vainqueur
    # En sortie les deux listes on été mises à jour
    #-----------------------------------------------------------------------
    def tour_de_jeu_imperatif(self, cartes_joueur_1, cartes_joueur_2):
        if cartes_joueur_1[0].__valeur_gt__(cartes_joueur_2[0]):
            cartes_joueur_1.append(cartes_joueur_1[0])
            cartes_joueur_1.append(cartes_joueur_2[0])

            del cartes_joueur_1[0]
            del cartes_joueur_2[0]

        elif cartes_joueur_1[0].__valeur_lt__(cartes_joueur_2[0]):
            cartes_joueur_2.append(cartes_joueur_1[0])
            cartes_joueur_2.append(cartes_joueur_2[0])

            del cartes_joueur_1[0]
            del cartes_joueur_2[0]
        else:
            #En cas d'égalité: Bataille
            index_egalite = 0
            while cartes_joueur_1[index_egalite].__valeur_eq__(cartes_joueur_2[index_egalite]):
                if len(cartes_joueur_1[index_egalite + 1:]) == 0:
                    break
                elif len(cartes_joueur_2[index_egalite + 1:]) == 0:
                    break
                else:
                    if cartes_joueur_1[index_egalite + 1].__valeur_eq__(cartes_joueur_2[index_egalite + 1]):
                        index_egalite +=1
                    else:
                        break
            logging.debug(f"Indice Egalite: {index_egalite}")

            if cartes_joueur_1[index_egalite + 1].__valeur_gt__(cartes_joueur_2[index_egalite + 1]):
                for i in range(0, index_egalite + 1):
                    cartes_joueur_1.append(cartes_joueur_1[i])
                    cartes_joueur_1.append(cartes_joueur_2[i])
                    del cartes_joueur_1[i]
                    del cartes_joueur_2[i]
            elif cartes_joueur_1[index_egalite + 1].__valeur_lt__(cartes_joueur_2[index_egalite + 1]):
                for i in range(0, index_egalite +1):
                    cartes_joueur_2.append(cartes_joueur_1[i])
                    cartes_joueur_2.append(cartes_joueur_2[i])
                    del cartes_joueur_1[i]
                    del cartes_joueur_2[i]

    #-----------------------------------------------------------------------
    # Un tour de jeu: Prend en entrée la liste des cartes des deux joueurs
    # Compare la première carte, établie le vainqueur
    # En cas d'égalité on regarde la caret suivante et ainsi de suite
    # jusqu'à ne plus avoir de carte egale en valeur. Dès qu'un joueur a une
    # carte plus forte il rafle toutes les cartes précedanctes qui étaient
    # egales.
    # On utilise la recusrivité pour faciliter l'implementation de cet
    # algorythm.
    #-----------------------------------------------------------------------
    def tour_de_jeu(self, cartes_joueur_1, cartes_joueur_2, nb_batailles=0):
        if cartes_joueur_1[0].__valeur_gt__(cartes_joueur_2[0]):
            return 1 * (nb_batailles +1)
        elif cartes_joueur_1[0].__valeur_lt__(cartes_joueur_2[0]):
            return -1 * (nb_batailles +1)
        else:
            #En cas d'égalité: Bataille. On fait un appel recursif
            return self.tour_de_jeu(cartes_joueur_1[1:], cartes_joueur_2[1:], nb_batailles+1)


    def tour_de_jeu2(self, cartes_joueur_1, cartes_joueur_2):
        if cartes_joueur_1[0].__valeur_gt__(cartes_joueur_2[0]):
            return 1, 1
        elif cartes_joueur_1[0].__valeur_lt__(cartes_joueur_2[0]):
            return 2, 1
        else:
            #En cas d'égalité: Bataille. On fait un appel recursif
            resultat = self.tour_de_jeu(cartes_joueur_1[1:], cartes_joueur_2[1:])
            return resultat[0], 1 + resultat[1]

    #------------------------------------------------------------------
    # Retourne le joueur gagnant (1 ou 2).
    # Si pas encore de gagnant renvoi 0
    #------------------------------------------------------------------
    def gagnant(self):
        if len(self.__cartes_joueurs[1]) == 0:
            return 2
        elif len(self.__cartes_joueurs[2]) == 0:
            return 1
        else:
            return 0

    #------------------------------------------------------------------
    # Retourne le joueur gagnant (1 ou 2).
    # Si pas encore de gagnant renvoi 0
    #------------------------------------------------------------------
    def partie_finie(self):
        if self.gagnant() == 0:
            return False
        else:
            return True

    #------------------------------------------------------------------
    # Commencer une partie
    #------------------------------------------------------------------
    def commencer_partie(self):
        self.initialiser_partie()
        logging.info("Commencons le jeu")

        # Commencer la bataille jusqu'à ce qu'un des joueurs n'ait plus de cartes
        i = 1
        while not self.partie_finie():
            input(f"Appuyer sur une touche pour le round {i}")
            logging.info(f"Joueur 1:{self.__cartes_joueurs[1]} -- Joueur 2:{self.__cartes_joueurs[2]}")

            resultat = self.tour_de_jeu(self.obtenir_cartes_joueur(1), self.obtenir_cartes_joueur(2))
            logging.info(f"Resultat: {resultat}")

            if resultat > 0:
                for j in range(0, resultat):
                    self.obtenir_cartes_joueur(1).append(self.obtenir_cartes_joueur(1)[0])
                    self.obtenir_cartes_joueur(1).append(self.obtenir_cartes_joueur(2)[0])
                    del self.obtenir_cartes_joueur(1)[0]
                    del self.obtenir_cartes_joueur(2)[0]
            elif resultat < 0:
                for j in range(0, (resultat * -1 )):
                    self.obtenir_cartes_joueur(2).append(self.obtenir_cartes_joueur(1)[0])
                    self.obtenir_cartes_joueur(2).append(self.obtenir_cartes_joueur(2)[0])
                    del self.obtenir_cartes_joueur(1)[0]
                    del self.obtenir_cartes_joueur(2)[0]
            '''
            joueur_gagnant = resultat[0]
            nb_cartes_gagnees = resultat[1]

            if joueur_gagnant == 1:
                joueur_perdant = 2
            else:
                joueur_perdant = 1

            for i in range(0, nb_cartes_gagnees):
                self.obtenir_cartes_joueur(joueur_gagnant).append(self.obtenir_cartes_joueur(joueur_gagnant)[0])
                self.obtenir_cartes_joueur(joueur_gagnant).append(self.obtenir_cartes_joueur(joueur_perdant)[0])
                del self.obtenir_cartes_joueur(joueur_gagnant)[0]
                del self.obtenir_cartes_joueur(joueur_perdant)[0]
            '''
            logging.info(f"Joueur 1:{self.__cartes_joueurs[1]} -- Joueur 2:{self.__cartes_joueurs[2]}")
            i += 1

#*************************************************************************
# Classe BatailleGraphique:
# Cette classe gère toute la partie graphique du jeu mais ulilse la
# classe Bataille comme moteur du jeu lui même. Ainsi toutes les règles
# du jeu, et initialisations de cartes sont fait dans la classe Bataille.
#*************************************************************************
class BatailleGraphique():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.jeu= Bataille(0)
        self.window = tk.Tk()
        self.debug_mode = tk.BooleanVar(value=DEBUG)
        self.window.title('Bataille')
        self.new_button = tk.Button()
        self.exit_button = tk.Button()
        self.width=1024
        self.height=600
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.command_canvas = tk.Canvas(self.window, width=self.width, height=50, bd=1, relief='groove')
        self.canvas.pack()
        self.command_canvas.pack()
        self.initialise_gui()

    def debug_changed(self):
        print(f"Changed: {self.debug_mode.get()}")
        global DEBUG
        DEBUG = self.debug_mode.get()
        if self.debug_mode.get():
            self.canvas.create_text(self.width/2, 20, font="cmr 24 bold", fill="Black", text="Mode DEBUG", tags=["debug"])
        else:
            self.canvas.delete("debug")

    def initialise_gui(self):
        reduction = 0.65
        bg_dimension = int(1500*reduction), int(791*reduction)
        las_vegas = ImageTk.PhotoImage(Image.open('images/las_vegas_4.jpg').resize(bg_dimension), Image.ANTIALIAS)
        self.canvas.create_image(30, 50, image = las_vegas, anchor = "nw")

        self.canvas.create_line(0,self.height/2, self.width, self.height/2)
        self.canvas.create_text(90, 20, font="cmr 16 bold", fill="blue", text="Joueur 1")
        self.canvas.create_text(90, (self.height) - 15, font="cmr 16 bold", fill="red", text="Joueur 2")

        self.new_button = tk.Button(self.command_canvas, text="Nouvelle partie avec", width = 20, activebackground = "blue")
        self.new_button.configure(command=lambda: self.commencer_partie(int(entry.get())))
        self.new_button.pack(side=tk.LEFT,padx=5, pady=5)

        entry = tk.Entry(self.command_canvas, width = 5)
        entry.pack(side=tk.LEFT, padx=5, pady=5)
        entry.insert(tk.END, '32')

        label = tk.Label(self.command_canvas, text = "cartes")
        label.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Checkbutton(self.command_canvas, text='Debug', command=self.debug_changed,
            variable=self.debug_mode, onvalue=True, offvalue=False).pack(side=tk.LEFT, padx=5, pady=5)

        self.exit_button = tk.Button(self.command_canvas, text="Sortir", command=lambda: self.window.quit())
        self.exit_button.configure(width = 20, activebackground = "red")
        self.exit_button.pack(side=tk.RIGHT,padx=20, pady=5)

        self.window.mainloop()

    def afficher_carte(self, carte, pos_x, pos_y, visible=False):
        dimension_carte = 100, 144
        if visible:
            fichier_image = f'images/{carte.Obtenir_Figure()}'
        else:
            fichier_image = 'images/dos_carte.jpg'

        image_carte=ImageTk.PhotoImage(Image.open(fichier_image).resize(dimension_carte), Image.ANTIALIAS)
        self.canvas.create_image(pos_x, pos_y, image=image_carte, tags=["carte"])
        self.window.update()

    def commencer_partie(self, nb_cartes):

        self.new_button["state"] = tk.DISABLED
        self.exit_button["state"] = tk.DISABLED

        self.jeu = Bataille(nb_cartes)
        self.jeu.initialiser_partie()

        dimension_carte = 100, 144
        decalage_carte = 25
        dos_carte = ImageTk.PhotoImage(Image.open('images/dos_carte.jpg').resize(dimension_carte), Image.ANTIALIAS)

        x_joueur_1 = 90
        y_joueur_1 = 150

        x_joueur_2 = 90
        y_joueur_2 = (self.height/2) + 150

        # Preparer les images de toutes les cartes des deux joueurs
        images_cartes={}
        for carte in (self.jeu.obtenir_cartes_joueur(1) + self.jeu.obtenir_cartes_joueur(2)):
            key=f'{carte.Obtenir_Valeur()}-{carte.Obtenir_Code_Couleur()}'
            images_cartes[key]=ImageTk.PhotoImage(Image.open(f'images/{carte.Obtenir_Figure()}').resize(dimension_carte), Image.ANTIALIAS)

        while not self.jeu.partie_finie():
            cartes_joueur_1 = self.jeu.obtenir_cartes_joueur(1)
            cartes_joueur_2 = self.jeu.obtenir_cartes_joueur(2)

            logging.debug(f"Joueur 1:{cartes_joueur_1} -- Joueur 2:{cartes_joueur_2}")

            # Pour Joueur 1: Afficher le dos de toutes les cartes sauf la premiere. Dans le mode DEBUG afficher toutes les cartes
            for i in range(len(cartes_joueur_1)-1, -1, -1):
                if i==0:
                    key=f'{cartes_joueur_1[i].Obtenir_Valeur()}-{cartes_joueur_1[i].Obtenir_Code_Couleur()}'
                    image_carte=images_cartes[key]
                else:
                    image_carte=dos_carte
                carte_joeur_1 = self.canvas.create_image(x_joueur_1 + (i * decalage_carte), y_joueur_1, image=image_carte, tags=["carte"])

            self.window.update()

            # Pour Joueur 2: Afficher le dos de toutes les cartes sauf la premiere. Dans le mode DEBUG afficher toutes les cartes
            for i in range(len(cartes_joueur_2)-1, -1, -1):
                if i==0:
                    key=f'{cartes_joueur_2[i].Obtenir_Valeur()}-{cartes_joueur_2[i].Obtenir_Code_Couleur()}'
                    image_carte=images_cartes[key]
                else:
                    image_carte=dos_carte
                carte_joeur_2 = self.canvas.create_image(x_joueur_2 + (i * decalage_carte), y_joueur_2, image=image_carte, tags=["carte"])

            self.window.update()
            time.sleep(VITESSE)

            resultat = self.jeu.tour_de_jeu(self.jeu.obtenir_cartes_joueur(1), self.jeu.obtenir_cartes_joueur(2))
            logging.debug(f"Resultat: {resultat}")

            cartes_perdante = []
            if resultat > 0:
                joueur_gagnant = 1
                joueur_perdant = 2
                cartes_perdante.append(carte_joeur_2)
                direction_annimation = -1
            elif resultat < 0:
                joueur_gagnant = 2
                joueur_perdant = 1
                cartes_perdante.append(carte_joeur_1)
                direction_annimation = 1

            # Retourner successivement toutes les cartes egales si il y en a
            cartes_egales={1: [], 2:[]}
            if abs(resultat) > 1:
                for i in range(abs(resultat)):
                    key1=f'{cartes_joueur_1[i].Obtenir_Valeur()}-{cartes_joueur_1[i].Obtenir_Code_Couleur()}'
                    image_carte1=images_cartes[key1]
                    cartes_egales[1].append(self.canvas.create_image(x_joueur_1 + (i * decalage_carte), y_joueur_1, image=image_carte1, tags=["carte"]))

                    key2=f'{cartes_joueur_2[i].Obtenir_Valeur()}-{cartes_joueur_2[i].Obtenir_Code_Couleur()}'
                    image_carte2=images_cartes[key2]
                    cartes_egales[2].append(self.canvas.create_image(x_joueur_2 + (i * decalage_carte), y_joueur_2, image=image_carte2, tags=["carte"]))

                    self.window.update()
                    time.sleep(0.5)

            # Animation des carte: La ou les carte perdante(s) vont vers le joueur gagnant en suivant un diagonal
            # Hors cas de bataille seule une carte perdants bouge: La carte la plus faible
            # En cas de Bataille on bouche toutes les cartes égales avant d'avoir trouvé une carte gagnante
            # On concatène à la liste de carte perdante (un seul élément) la liste de toutes les cartes précedantes qui étaient egales (0 ou N cartes)
            cartes_perdante.extend(cartes_egales[joueur_perdant])
            for j in range(25):
                for carte_perdante in cartes_perdante:
                    self.canvas.move(carte_perdante, 1.5*j, j * direction_annimation)
                time.sleep(0.04)
                self.window.update()

            # Après toutes les animations il est temps de mettre à jour l'état finale des cartes des deux joueurs
            # pour préparte le tour suivant.
            for i in range(abs(resultat)):
                self.jeu.obtenir_cartes_joueur(joueur_gagnant).append(self.jeu.obtenir_cartes_joueur(1)[0])
                self.jeu.obtenir_cartes_joueur(joueur_gagnant).append(self.jeu.obtenir_cartes_joueur(2)[0])
                del self.jeu.obtenir_cartes_joueur(1)[0]
                del self.jeu.obtenir_cartes_joueur(2)[0]

            self.canvas.delete("carte")

        logging.debug(f'Gagnant: {self.jeu.gagnant()} / Partie Finie: {self.jeu.partie_finie()}')
        self.fin_partie()

    def fin_partie(self):
        self.canvas.delete("all")
        score_text = f'Le vainqueur est le joueur {self.jeu.gagnant()}\n'
        self.canvas.create_text(self.width/2, self.height/2, font="cmr 20 bold", fill="blue", text=score_text)

        self.new_button["state"] = tk.NORMAL
        self.exit_button["state"] = tk.NORMAL

    def rejouer(self, nb_cartes):
        self.initialise_gui()
        self.commencer_partie(nb_cartes)

    #------------------------------------------------------------------
    # Retourne le joueur gagnant (1 ou 2).
    # Si pas encore de gagnant renvoi 0
    #------------------------------------------------------------------
    def gagnant(self):
        return self.jeu.gagnant()

def music(song):
    pygame.mixer.init()
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

#////////////////////////////////////////////////////////////////////
#
# Point d'entrée du programme.
#
#///////////////////////////////////////////////////////////////////
def main() -> int:
    music('music/september.mp3')

    if DEBUG:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    if GUI:
        jeu = BatailleGraphique()
    else:
        jeu = Bataille(12)
        jeu.commencer_partie()

    logging.info(f"Le gagnant est le joueur {jeu.gagnant()}")

    return 0

if __name__ == '__main__':
    DEBUG=False
    GUI=True
    VITESSE=1.0

    main()
