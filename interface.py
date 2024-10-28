#DALY JASSEM
import pygame
from pygame.locals import *
import random
import numpy as np
from plateau import *

from tetra import Point,Tetramino
from copy import deepcopy
class KST:
    __slots__ = ()  # empêche la ré-écriture accidentelle des constantes  

    # codes numériques pour les 4 directions, utilisés aussi par le module
    # d'inteface graphique
    HAUT = 0
    DROITE = 1
    BAS = 2
    GAUCHE = 3
    ESPACE = 4

class Interface:
    def __init__(self, dim_x, dim_y, titre):
        self.clock = pygame.time.Clock()
        self.cursor = (0, 0)
        self.taille_fonte_y = 30
        pygame.init()
        if not pygame.font.get_init():
            print("Désolé, les fontes de caractères sont absentes, je ne peux démarrer")
            quit()
        self.font = pygame.font.SysFont("Courrier, Monospace",
                                    self.taille_fonte_y)
        self.taille_fonte_x = self.font.size('M')[0]
        self.ecran = pygame.display.set_mode((dim_x  * self.taille_fonte_x ,
                                          dim_y * self.taille_fonte_y))
        pygame.display.set_caption(titre)
        # dictionnaire de couleurs: comme une liste mais indexé par des chaînes 
        self.COULEUR = {  
            'vert'   : (11, 240, 11),    # "vert" défini par intensités (rouge, vert, bleu)
            'rouge'   : (213, 11, 11),
            'orange'   : (213, 120, 5),
            'jaune'   : (255, 233, 51),
            'bleu'    : (40, 40, 240),
            'blanc'   : (255, 255, 255),
            'TURQUOISE'   : (51, 255, 233),
            'noir'    : (0, 0, 0),
            'move':(181, 51, 255)
        }
        # liste des noms de couleurs
        self.NOM_COULEUR = list(self.COULEUR.keys())
        # dictionnaire des indices des noms de couleurs
        self.IND_COULEUR = {}
        for indice,nom in enumerate(self.NOM_COULEUR):
            self.IND_COULEUR[nom] = indice

    # place le "curseur" : la position de la prochaine commande "write"
    def curseur(self, x, y):
        self.cursor = (x, y)
        
    # écrire une chaine à la position du curseur
    def write(self, texte, fgcolor=(255,255,255), bgcolor=(0,0,0)):
        texte = self.font.render(texte,
                            True,
                            pygame.Color(fgcolor),
                            pygame.Color(bgcolor))
        self.ecran.blit(texte,
                        (self.cursor[0]*self.taille_fonte_x,
                         self.cursor[1]*self.taille_fonte_y))

    # faire une temporisation
    def pause(self, tempo): 
        self.clock.tick(tempo)

    # affiche les modifications effectuées depuis le dernier appel
    def mise_a_jour(self):
        pygame.display.flip()

    # retourne code d'une touche de déplacement du clavier (touches "flêches")
    # ou None sinon
    # teste d'abord si nouvelle pression sur une touche
    def lire_touche(self):
        key = None
        for event in pygame.event.get():
            # teste d'abord si fermeture fenêtre
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key = KST.HAUT
                elif event.key == pygame.K_DOWN:
                    key = KST.BAS
                elif event.key == pygame.K_LEFT:
                    key = KST.GAUCHE
                elif event.key == pygame.K_RIGHT:
                    key = KST.DROITE
                elif event.key == pygame.K_SPACE:
                    key = KST.ESPACE
        # l'appel à pygame.event.get() a mis à jour l'état des touches
        if key != None:
            return key
        # teste maintenant si pression continue (et pas nouvelle) sur touche
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            return KST.DROITE
        if keys[pygame.K_LEFT]:
            return KST.GAUCHE
        if keys[pygame.K_UP]:
            return KST.HAUT
        if keys[pygame.K_DOWN]:
            return KST.BAS
        if keys[pygame.K_SPACE]:
            return KST.ESPACE

        # si ici, alors pas de touche qui nous intéresse
        return None

    # ferme la librairie (au cas où la fenêtre graphique reste "bloquée"
    def fermer(self):
        pygame.quit()
    
if __name__ == "__main__":               
    # création d'un écran de 10x10 caractères
    ecran = Interface(32, 20, "Bureau d'étude")
    
    plateau=Plateau()
    
    
    nbr_ligne_efface=0
    TETRA=Tetramino(0,6)
    TETRAPROCHAINE=Tetramino(0,6)
    # illustrons la zone de l'écran
    SCORE=0
    deuxTETRA=False
    TETRA2=0
    
    # testons la saisie de touches
    compteur_temps = 0
     # en millièmes de seconde, soit un dixième de seconde ici
    while True: # boucle d'animation, réglée par la pause en dernière instruction
        plateau.presentation_plateau(ecran,TETRA,TETRA2)
        temporisation = 100
        
        for y in range(20):
            for x in range(20,32):
                ecran.cursor = (x, y)
                ecran.write(" ",fgcolor=ecran.COULEUR['blanc'],
                                bgcolor=ecran.COULEUR['blanc'])
        ecran.cursor = (20, 5)
        ecran.write("VOTRE SCORE:",fgcolor=ecran.COULEUR['noir'],
                            bgcolor=ecran.COULEUR['blanc'])
        ecran.cursor = (25, 6)
        ecran.write(str(SCORE),fgcolor=ecran.COULEUR['noir'],
                            bgcolor=ecran.COULEUR['blanc'])
        ecran.cursor = (20, 12)
        ecran.write(" PROCHAINE:",fgcolor=ecran.COULEUR['noir'],
                            bgcolor=ecran.COULEUR['blanc'])
        for elemnt in TETRAPROCHAINE.liste:
                    x=elemnt.abscisse
                    y=elemnt.ordonne   
                    ecran.cursor = (18+y,14+x)
                    ecran.write("  ",fgcolor=ecran.COULEUR[plateau.couleurs()[TETRAPROCHAINE.couleur]],
                            bgcolor=ecran.COULEUR[plateau.couleurs()[TETRAPROCHAINE.couleur]])
        # affiche en bas un compteur en 1/10 de seconde (approximativement)

        compteur_temps = (compteur_temps + 1) % 100

        # saisie une touche lettre et affiche au milieu sur fond de couleur alea
        numero_couleur = random.randint(0, len(ecran.NOM_COULEUR)-1)
        couleur_alea = ecran.COULEUR[ecran.NOM_COULEUR[numero_couleur]]
        # touche curseur pressée ?
        touche = ecran.lire_touche()
        if compteur_temps%50==0 and TETRA.mouvement==True:
            TETRA=TETRA.deplacer(1,0)
            if deuxTETRA==True:
                TETRA2=TETRA2.deplacer(1,0)
        
                
        
        if plateau.game_over():
            
            for y in range(20):
                for x in range(32):
                    ecran.cursor = (x, y)
                    ecran.write(" GAME OVER",fgcolor=ecran.COULEUR['blanc'],
                            bgcolor=ecran.COULEUR['noir'])
            ecran.cursor = (11, 6)
            ecran.write("GAME OVER",fgcolor=ecran.COULEUR['blanc'],
                            bgcolor=ecran.COULEUR['noir'])
            ecran.cursor = (8, 8)
            ecran.write("Votre score est:",fgcolor=ecran.COULEUR['blanc'],
                            bgcolor=ecran.COULEUR['noir'])
            ecran.cursor = (15, 9)
            ecran.write(str(SCORE),fgcolor=ecran.COULEUR['blanc'],
                            bgcolor=ecran.COULEUR['noir'])
            
            
        if deuxTETRA==True:    
            if TETRA2.verif_bas() or plateau.collision(TETRA2) :
                deuxTETRA=False
                for compteur in (TETRA2.liste):
                    x=compteur.abscisse
                    y=compteur.ordonne
                    plateau.jeu[y][x]=TETRA2.couleur
            if TETRA.verif_bas() or plateau.collision(TETRA):
                for compteur in (TETRA2.liste):
                    x=compteur.abscisse
                    y=compteur.ordonne
                    plateau.jeu[y][x]=TETRA2.couleur
                TETRA=deepcopy(TETRA2)
        if TETRA.verif_bas() or plateau.collision(TETRA) :
                TETRA.mouvement=False
                
                for compteur in (TETRA.liste):
                    x=compteur.abscisse
                    y=compteur.ordonne
                    plateau.jeu[y][x]=TETRA.couleur
                nbr_ligne_efface=0
                while plateau.check_ligne()!=-1:
                            
                    ligne=plateau.check_ligne()
                    plateau=plateau.efface_ligne(ligne)
                    nbr_ligne_efface+=1
                    plateau.check_ligne()
                if nbr_ligne_efface>=2:
                    deuxTETRA=True
                    TETRA=TETRAPROCHAINE
                    TETRA2=Tetramino(0,12)
                    TETRAPROCHAINE=Tetramino(0,6)
                if deuxTETRA==False:
                    TETRA=TETRAPROCHAINE
                    TETRAPROCHAINE=Tetramino(0,6)
                if nbr_ligne_efface==1:
                    SCORE+=40
                elif nbr_ligne_efface==2:
                    SCORE+=200
                elif nbr_ligne_efface==3:
                    SCORE+=300
                elif nbr_ligne_efface==4:
                    SCORE+=1200
        
            
            
                
        
        
        
        if touche != None: # oui, une touche curseur pressée
            
            
            if touche ==4 and deuxTETRA==True:
                temporisation=2
                aux=deepcopy(TETRA)
                TETRA=deepcopy(TETRA2)
                TETRA2=deepcopy(aux)
            temporisation=10
            if touche==0 and TETRA.mouvement==True and TETRA.forme!='square':
                image_tetra=Tetramino.image(TETRA)
                if  plateau.collision(image_tetra)==False:
                    TETRA=TETRA.tourner()
                TETRA=TETRA.retourne_au_plateau()
            if touche==1 and TETRA.mouvement==True and TETRA.verif_droite(plateau):
                TETRA=TETRA.deplacer(0,1)
            if touche==2 and TETRA.verif_bas()==False and plateau.collision(TETRA)==False:
                TETRA=TETRA.deplacer(1,0)
            if touche==3 and TETRA.mouvement==True and TETRA.verif_gauche(plateau):
                TETRA=TETRA.deplacer(0,-1)
            
            
                        
                
            
        
        
        
            
        
            
            
        # affiche les écritures faites sur l'écran (SINON RIEN n'apparaît...)
        ecran.mise_a_jour()
        # règle la vitesse de l'animation avec une pause
        ecran.pause(temporisation)

    ecran.fermer()
