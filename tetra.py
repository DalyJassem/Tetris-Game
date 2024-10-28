#DALY JASSEM
from random import*
from copy import deepcopy
class Point:
    def __init__(self, x, y):
        self.abscisse = x
        self.ordonne = y

    def __add__(self, vecteur):
        x = self.abscisse + vecteur.abscisse
        y = self.ordonne + vecteur.ordonne
        return Point(x, y)

    def __sub__(self, vecteur):
        x = self.abscisse - vecteur.abscisse
        y = self.ordonne - vecteur.ordonne
        return Point(x, y)


    def rotation(self, center, sens_positif=True):
        # Translate point back to origin
        translation = self - center
        # rotation point
        if sens_positif:
            rotation = Point(translation.ordonne, -translation.abscisse)
        else:
            rotation = Point(-translation.ordonne, translation.abscisse)
        # Translate point back to its original position
        return rotation + center

class Tetramino :
    
    def __init__(self,x,y):
        #choix aléatoire du forme 
        liste_formes=["square","straight","T","L","J","skew","skew_inverse"]
        indice_aleatoire=randint(0,len(liste_formes)-1)
        self.forme=liste_formes[indice_aleatoire]# initialisation du forme 
        self.vecteur_position=Point(x,y) #initialisation de vecteur de position
        self.liste=[]
        self.mouvement=True
        if self.forme == "straight" :
            self.liste.append(self.vecteur_position+Point(0,0)) # je  fixe le centre
            self.liste.append(self.vecteur_position+Point(1,0))
            self.liste.append(self.vecteur_position+Point(2,0))
            self.liste.append(self.vecteur_position+Point(3,0))
            self.couleur=1
        elif self.forme =="square":
            self.liste.append(self.vecteur_position+Point(0,0)) # je  fixe le centre
            self.liste.append(self.vecteur_position+Point(1,0))
            self.liste.append(self.vecteur_position+Point(0,1))
            self.liste.append(self.vecteur_position+Point(1,1))
            self.couleur=2

        elif self.forme =="T" :
            self.liste.append(self.vecteur_position+Point(1,0))
            self.liste.append(self.vecteur_position+Point(0,0))
            self.liste.append(self.vecteur_position+Point(2,0))
            self.liste.append(self.vecteur_position+Point(1,1))
            self.couleur=3

        elif self.forme =="L" :
            self.liste.append(self.vecteur_position+Point(0,0)) # je  fixe le centre
            self.liste.append(self.vecteur_position+Point(1,0))
            self.liste.append(self.vecteur_position+Point(2,0))
            self.liste.append(self.vecteur_position+Point(0,1))
            self.couleur=4

        elif self.forme == "skew" :
            self.liste.append(self.vecteur_position+Point(1,0))# je  fixe le centre
            self.liste.append(self.vecteur_position+Point(2,0))
            self.liste.append(self.vecteur_position+Point(1,1))
            self.liste.append(self.vecteur_position+Point(0,1))
            self.couleur=5

        elif self.forme == "skew_inverse" :
            self.liste.append(self.vecteur_position+Point(1,1))# je  fixe le centre
            self.liste.append(self.vecteur_position+Point(2,1))
            self.liste.append(self.vecteur_position+Point(1,0))
            self.liste.append(self.vecteur_position+Point(0,0))
            self.couleur=6

        elif self.forme =="J" :
            self.liste.append(self.vecteur_position+Point(0,1)) # je  fixe le centre
            self.liste.append(self.vecteur_position+Point(1,1))
            self.liste.append(self.vecteur_position+Point(2,1))
            self.liste.append(self.vecteur_position+Point(0,0))
            self.couleur=7

    def tourner(self, sens_positif=True):
        # rotation all points around the first point (centre)
        centre = self.liste[0]
        nouvelle_position = [centre] + [p.rotation(centre, sens_positif) for p in self.liste[1:]]
        self.liste = nouvelle_position
        return self
    def clonage(self):
        clonage=deepcopy(self)
        return clonage
    def deplacer(self,x,y):
        for point in range(4):
            self.liste[point]+=Point(x,y)
        return self
    def image(self):
        image=Tetramino.clonage(self)
        image.tourner()
        return image
    def verif_droite(self,plateau):
        
        
        for point in self.liste:
            x=point.abscisse
            y=point.ordonne
            if (y+1>19) or (plateau.jeu[y+1][x] !=0) :
                return False
        return True
            
    def verif_gauche(self,plateau):

        for point in self.liste:
            x=point.abscisse
            y=point.ordonne
            if (y-1<0 ) or (plateau.jeu[y-1][x] !=0):
                return False
        return True
        
    def verif_bas(self):
        for point in self.liste:
            if (point.abscisse+1>19) :
                return True
        return False
    def retourne_au_plateau(self):
        '''  '''
        
        ymin=0
        ymax=19
        nbr_decalage_a_droite=0
        nbr_decalage_a_gauche=0
        for point in self.liste:
            x=point.abscisse
            y=point.ordonne
            if y<ymin:
                nbr_decalage_a_droite+=1
            if y>ymax:
                nbr_decalage_a_gauche+=1
            
        for repition in range(nbr_decalage_a_droite):
            self.deplacer(0,1)
        for repition in range(nbr_decalage_a_gauche):
            self.deplacer(0,-1)
        return self 
        