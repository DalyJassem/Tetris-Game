#DALY JASSEM
import numpy as np
from copy import deepcopy
class Plateau:
    def __init__(self):
        self.nbr_lignes=25
        self.nbr_colonnes=25
        self.taille_case=10
        self.jeu = np.zeros((self.nbr_lignes, self.nbr_colonnes), dtype=int).reshape(25,25)
    def affiche_plateau(self):
        for ligne in range(self.nbr_lignes):
            for colonnes in range(self.nbr_colonnes):
                print(self.jeu[ligne,colonnes],end=" ")
    def couleurs (self):
        return['noir','vert','rouge','orange','jaune','bleu','move','TURQUOISE']
    def presentation_plateau(self,ecran,TETRA,TETRA2):
        plateau=deepcopy(self)
        if TETRA2!=0:
            for elemnt in TETRA2.liste:
                x=elemnt.abscisse
                y=elemnt.ordonne
                plateau.jeu[y][x]=TETRA2.couleur
        for elemnt in TETRA.liste:
                        x=elemnt.abscisse
                        y=elemnt.ordonne
                        plateau.jeu[y][x]=TETRA.couleur
        for ligne in range(plateau.nbr_lignes):
                for colonnes in range(plateau.nbr_colonnes):
                    case=plateau.jeu[ligne,colonnes]
                    ecran.cursor = (ligne, colonnes)
                    ecran.write("  ",fgcolor=ecran.COULEUR[plateau.couleurs()[plateau.jeu[ligne,colonnes]]],
                            bgcolor=ecran.COULEUR[plateau.couleurs()[plateau.jeu[ligne,colonnes]]])
                
    def collision(self,TETRA):
        for compteur in (TETRA.liste):
            x=compteur.abscisse
            y=compteur.ordonne
            if  self.jeu[y][x+1]!=0 :
                return True
        return False
    def game_over(self):
        for ligne in range(self.nbr_lignes):
            if self.jeu[ligne][0]!=0:
                return True
        return False
    def check_ligne(self):
        for ligne in range(20):
            nbr_de_zeros=0
            for colone in range(20):
                if self.jeu[colone][ligne]==0:
                    nbr_de_zeros+=1
            if nbr_de_zeros<=0:
                return ligne
        return -1
            
    def efface_ligne(self,ligne_a_effacer):
        for colone in range(self.nbr_colonnes):
            self.jeu[colone][ligne_a_effacer]=0
        
        for lignes in range(ligne_a_effacer,0,-1):
            for colone in range(self.nbr_colonnes):
                self.jeu[colone][lignes]=self.jeu[colone][lignes-1]
             
       
                
        return self


