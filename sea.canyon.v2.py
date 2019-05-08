import pygame,patgametools.sprite,random,sys,time
import patgametools.sprite as sprite

from pygame.locals import *
class Joueur(sprite.Sprite):
    
    global ecran,largeurEcran,hauteurEcran
    
    def __init__(self,x,y,image):
        sprite.Sprite.__init__(self,x,y,image)
        self.dx=5
        self.direction=0 # 0=immobile 1=droite -1=gauche
        
    def mise_a_jour(self):
        if self.direction==1: #déplacement vers la droite
            #vérifier limites ecran
            if self.x+self.direction*self.dx+self.largeur>largeurEcran:
                self.set_x=largeurEcran-self.largeur
            else:
                self.deplacer(self.direction*self.dx,0)
            
        elif self.direction==-1:#déplacement gauche
            #vérifier limites ecran
            if self.x-self.direction*self.dx<0:
                self.set_x=0
            else:
                self.deplacer(self.direction*self.dx,0)
                
                
    


class Paroi(sprite.Sprite):
    
    #variables de classe
    largeurparoi=0
    image=""
    
    def __init__(self,x,y,image):
        sprite.Sprite.__init__(self,x,y,image)
        self.active=1#si 0 à effacer de la liste des parois
        Paroi.image=image
    
    
class Canyon():
    #variables de classe
    parois=[]
    derniereparoigauchex=0
    derniereparoidroitex=0
            
    global largeurEcran,hauteurEcran
    
    
    def __init__(self,imageparoi):
        self.largeurMinimale=100
        self.largeurMaximale=400
        self.coordminx=100
        self.coordmaxx=largeurEcran-100
        self.imageparoi=imageparoi
        self.clock=pygame.time.Clock()
        self.temps_cumule=0
        self.delai_creation=200#toutes les xxx ms
        
        self.creerpremieresparois()
        
    def creerpremieresparois(self):
        #créer premières paroi
        paroigauchex=int(largeurEcran/2-self.largeurMaximale/2)
        paroidroitex=int(largeurEcran/2+self.largeurMaximale/2)
        y=0
        #créer paroi gauche
        Canyon.parois.append(Paroi(paroigauchex,y,self.imageparoi))
        Canyon.derniereparoigauchex=paroigauchex
        #créer paroi droite
        Canyon.parois.append(Paroi(paroidroitex,y,self.imageparoi))
        Canyon.derniereparoidroitex=paroidroitex
        #retenir la largeur d'une paroi sur base de la première paroi créée
        Paroi.largeurparoi=Canyon.parois[0].largeur
        
        
    def nouvelles_coordonnees(self):
        
        valid=False
        y=0
        paroigauchex=0
        paroidroitex=0
                    
        while not valid:
                  
            direction=random.randint(-1,1)  #direction paroi 0=inchangé, -1=gauche, 1=droite
            paroigauchex=Canyon.derniereparoigauchex+int(direction*Paroi.largeurparoi)
            #vérifier coordonnées dans limites
            if paroigauchex<self.coordminx:
                paroigauchex=self.coordminx
        
            direction=random.randint(-1,1)  #direction paroi 0=inchangé, -1=gauche, 1=droite
            paroidroitex=Canyon.derniereparoidroitex+int(direction*Paroi.largeurparoi)
            #vérifier coordonnées dans limites
            if paroidroitex>self.coordmaxx:
                paroidroitex=self.coordmaxx
            
            #print("x1:{} x2:{}".format(self.paroi_gauche_x,self.paroi_droite_x))
            #vérifier largeur canyon
            if paroidroitex-paroigauchex>=self.largeurMinimale \
               and paroidroitex-paroigauchex<=self.largeurMaximale:
                valid=True
        
        #retenir dernieres coordonnees des parois
        Canyon.derniereparoigauchex=paroigauchex
        Canyon.derniereparoidroitex=paroidroitex
        #retourner la liste des deux nouvelles coordonnées de parois
        return (paroigauchex,paroidroitex)
        
        
    def deplacerparois(self):
        for paroi in Canyon.parois:
            y=paroi.y+paroi.hauteur
            paroi.set_y(y)
            
            #si sortie écran => marquer paroi inactive (à effacer à la prochaine mise à jour)
            if y>hauteurEcran:
                paroi.active=0
    
    def creerparois(self):
        y=0
        
        paroigauchex,paroidroitex=self.nouvelles_coordonnees()
        
        self.parois.append(Paroi(paroigauchex,y,Paroi.image))
        self.parois.append(Paroi(paroidroitex,y,Paroi.image))
            
            
    def effacerparoisinactives(self):
        #print("parois avant effacement : {}".format(len(Canyon.parois)))
        nouvelleliste=[]
        index=0
        for paroi in Canyon.parois:
            if (paroi.active):
                nouvelleliste.append(paroi)
            index+=1
        
        Canyon.parois.clear()
        Canyon.parois.extend(nouvelleliste)
        
        del(nouvelleliste)
                
        #print("parois après effacement : {}\n".format(len(Canyon.parois)))        
        
            
    
    def mise_a_jour(self):
                
        self.temps_cumule+=self.clock.tick()
        
        if self.temps_cumule>self.delai_creation:
            self.temps_cumule=0
            self.deplacerparois()
            self.effacerparoisinactives()
            self.creerparois()
            
               
    def dessiner(self):
        for paroi in Canyon.parois:
            paroi.dessiner(ecran)
                              
    

class MoteurJeu():
    global joueur, ecran
    
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
            #vérifier collision
            if self.joueur.collisionavecsprites(Canyon.parois):
                print("collision")
            
            #dessiner canyon
            self.canyon.dessiner()
            #dessiner joueur
            self.joueur.dessiner(ecran)
            
            
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
