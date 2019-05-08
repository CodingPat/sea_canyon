import pygame,random,sys,time

from pygame.locals import *




class Joueur():
    
    global ecran,largeurEcran,hauteurEcran
    
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.sprite=pygame.image.load(image).convert_alpha()
        self.largeur=self.sprite.get_width()
        self.hauteur=self.sprite.get_height()
        self.vitesse=5
        self.direction=0 # 0=immobile 1=droite -1=gauche
        
    def mise_a_jour(self):
        if self.direction==1:
            #droite
            self.x+=self.vitesse
            #vérifier limites ecran
            if self.x+self.largeur>largeurEcran:
                self.x=largeurEcran-self.largeur
            
        elif self.direction==-1:
            #gauche
            self.x-=self.vitesse
            if self.x<0:
                self.x=0
                
        print(self.sprite.get_rect())
  
    def dessiner(self):
        ecran.blit(self.sprite,(self.x,self.y))



class Paroi():
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.image=image
        self.hauteur=self.sprite.get_height()
        self.largeur=self.sprite.get_width()
        self.rectangle=(self.x,self.y,self.largeur,self.hauteur)
   
    def move(self,x,y):
        self.x=x
        self.y=y
        self.rectangle.topleft=(x,y)
        
    def dessiner(self,surface):
        surface.blit(self.image,self.rectangle.topleft)
        
    
    
class Canyon():
    #variable de classe
    parois=[]
        
    global largeurEcran
    
    
    def __init__(self,image):
        self.largeurMinimale=100
        self.largeurMaximale=400
        self.coordx_min=100
        self.coordx_max=largeurEcran-100
        self.direction_gauche=0#0 immobile, 1=vers droite, -1=vers la gauche
        self.direction_droite=0
        self.sprite=pygame.image.load(image).convert_alpha()
        self.hauteur_paroi=self.sprite.get_height()
        self.largeur_paroi=self.sprite.get_width()
        
        self.clock=pygame.time.Clock()
        self.temps_cumule=0
        self.delai_creation=200#toutes les xxx ms
        self.paroi_gauche_x=int(largeurEcran/2-self.largeurMaximale/2)
        self.paroi_droite_x=int(largeurEcran/2+self.largeurMaximale/2)
        self.y=0
        self.creer_paroi()
        
    def nouvelles_coordonnees(self):
        
        valid=False
        sauvegarde_gauche_x=self.paroi_gauche_x
        sauvegarde_droite_x=self.paroi_droite_x
        
        while not valid:
            self.paroi_gauche_x=sauvegarde_gauche_x
            self.paroi_droite_x=sauvegarde_droite_x
            self.direction_gauche=random.randint(-1,1)
            self.paroi_gauche_x+=int(self.direction_gauche*self.largeur_paroi)
            #vérifier coordonnées dans limites
            if self.paroi_gauche_x<self.coordx_min:
                self.paroi_gauche_x=self.coordx_min
        
            self.direction_droite=random.randint(-1,1)
            self.paroi_droite_x+=int(self.direction_droite*self.largeur_paroi)
            #vérifier coordonnées dans limites
            if self.paroi_droite_x>self.coordx_max:
                self.paroi_droite_x=self.coordx_max
            
            #print("x1:{} x2:{}".format(self.paroi_gauche_x,self.paroi_droite_x))
            #vérifier largeur canyon
            if self.paroi_droite_x-self.paroi_gauche_x>=self.largeurMinimale \
               and self.paroi_droite_x-self.paroi_gauche_x<=self.largeurMaximale:
                valid=True
        
        
            
    def creer_paroi(self):
        
        Canyon.parois.append([self.paroi_gauche_x,self.paroi_droite_x,self.y])
        #print("gauche:{} droite:{} ".format(self.paroi_gauche_x,self.paroi_droite_x))
        
            
    
    def mise_a_jour(self):
        y=0
        self.temps_cumule+=self.clock.tick()
        
        if self.temps_cumule>self.delai_creation:
            self.temps_cumule=0
            for paroi in Canyon.parois:
                paroi[2]+=self.hauteur_paroi
            
            self.nouvelles_coordonnees()
            self.creer_paroi()
            
            
    
    def dessiner(self):
        for paroi in Canyon.parois:
            #dessiner paroi gauche
            ecran.blit(self.sprite,(paroi[0],paroi[2]))
            #dessiner paroi droite
            ecran.blit(self.sprite,(paroi[1],paroi[2]))
            
                              
    

class MoteurJeu():
    global joueur
    
    def __init__(self):
        self.clock=pygame.time.Clock()
        self.joueur=Joueur(largeurEcran/2,hauteurEcran/2,"squidred.png")
        self.canyon=Canyon("wall.png")
        
    def boucle_principale(self):
        while True:
            ecran.fill((0,0,0))#effacer écran
            #mise à jour joueur
            self.joueur.mise_a_jour()
            #mise à jour canyon
            self.canyon.mise_a_jour()
            #dessiner joueur
            self.joueur.dessiner()
            #dessiner canyon
            self.canyon.dessiner()
            
            
            #update screen
            pygame.display.update()

            #control fps       
            self.tempsPasse=self.clock.tick(60)


            #test touches
            for event in pygame.event.get():
            
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        pass
                        self.joueur.direction=-1
                        #print('déplacement gauche')
                    if event.key==pygame.K_RIGHT:
                        pass
                        self.joueur.direction=1
                        #print('déplacement droite')
                    if event.key==pygame.K_ESCAPE:
                        self.quitter_jeu()

                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT:
                        pass
                        self.joueur.direction=0
                        #print('pas de déplacement')
                    if event.key==pygame.K_RIGHT:
                        pass
                        self.joueur.direction=0
                        #print('pas de déplacement')
                            
                if event.type==pygame.QUIT:
                    self.quitter_jeu()

            
            
            
            
            
    def quitter_jeu(self):
        pygame.quit()
        sys.exit()
        
        



#démarrage du module
if __name__=="__main__":
    
    largeurEcran=800
    hauteurEcran=600
        
    pygame.init()
    
    ecran=pygame.display.set_mode((largeurEcran,hauteurEcran))

    pygame.display.set_caption("Sea canyon !")

    
    monMoteurJeu=MoteurJeu()        
    monMoteurJeu.boucle_principale()
