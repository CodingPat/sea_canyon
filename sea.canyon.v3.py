import pygame,random,sys,time
import patgametools.sprite as sprite

from pygame.locals import *

class Joueur(sprite.Sprite):
    
    
    def __init__(self,x,y,image,vies=3):
        sprite.Sprite.__init__(self,x,y,image)
        self.dx=5
        self.direction=0 # 0=immobile 1=droite -1=gauche
        self.vies=3
        self.distanceparcourue=0
        #gérer clignotment en cas de collision
        self.clock=pygame.time.Clock()
        self.delaidepuisclignotement=0#délai depuis dernier clignotement
        self.delailimiteclignotement=100#délai pour clignotement
        
    
    def reset(self):
        "redémarrer position initiale"
        #print("joueur reset")
        self.set_x(largeurecran/2)
        self.set_y(hauteurecran/2)
    
    def mise_a_jour(self):
        if self.direction==1: #déplacement vers la droite
            #vérifier limites ecran
            if self.x+self.direction*self.dx+self.largeur>moteurJeu.largeurecran:
                self.set_x=moteurJeu.largeurecran-self.largeur
            else:
                self.deplacer(self.direction*self.dx,0)
            
        elif self.direction==-1:#déplacement gauche
            #vérifier limites ecran
            if self.x-self.direction*self.dx<0:
                self.set_x=0
            else:
                self.deplacer(self.direction*self.dx,0)
                
                
    def dessiner(self,surface):
        if not moteurJeu.ecrancollision:
            #print("dessiner - pas de collision")
            surface.blit(self.surface,self.rect.topleft)
        else:
            #clignotement
            self.clock.tick()
            self.delaidepuisclignotement+=self.clock.tick()
            #print("dessiner - collision")
            if self.delaidepuisclignotement>self.delailimiteclignotement:
                #print("dessiner - collision - dépassement délai clignotement")
                self.delaidepuisclignotement=0
                surface.blit(self.surface,self.rect.topleft)
        


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
            
    def __init__(self,imageparoi):
        self.largeurMinimale=100
        self.largeurMaximale=400
        self.coordminx=100
        self.coordmaxx=moteurJeu.largeurecran-100
        self.imageparoi=imageparoi
        self.clock=pygame.time.Clock()
        self.temps_cumule=0
        self.delai_creation=200#toutes les xxx ms
        
        self.reset()
    
    
    def reset(self):
        Canyon.parois.clear()
        #position initiale
        paroigauchex=int(moteurJeu.largeurecran/2-self.largeurMaximale/2)
        paroidroitex=int(moteurJeu.largeurecran/2+self.largeurMaximale/2)
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
            if y>moteurJeu.hauteurecran:
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
            paroi.dessiner(moteurJeu.ecran)
                              
    

class MoteurJeu():
        
    def __init__(self,largeurecran,hauteurecran,titre):
        pygame.init()
        self.ecran=pygame.display.set_mode((largeurecran,hauteurecran))
        self.largeurecran=largeurecran
        self.hauteurecran=hauteurecran
        pygame.display.set_caption(titre)    

        self.clock=pygame.time.Clock()
        self.clockcollision=pygame.time.Clock()
        self.delaicollision=0
        self.delaicollisionmaximum=2000
        self.joueur=None
        self.canyon=None
        self.findepartie=False #ecran fin de partie
        self.ecrandemarrage=False #ecran demarrage
        self.jeuactif=False #jeu demarre
        self.ecrancollision=False
        self.jeupause=False #jeu pause
        
        
    def reset(self):
        #print("Moteur de jeu : reset")
        self.canyon.reset()
        self.joueur.reset()
        
        
    def ecrandemarrage(self):
        pass
    
    def jeudemarre(self):
        pass
    
    def jeupause(self):
        pass
    
    def findepartie(self):
        pass
    
    
    def boucle_principale(self):
       
        self.jeuactif=True
        
        while True:
            while self.jeuactif:
                self.ecran.fill((0,0,0))#effacer écran
                #mise à jour joueur
                self.joueur.mise_a_jour()
                #mise à jour canyon
                self.canyon.mise_a_jour()
                  
                #dessiner canyon
                self.canyon.dessiner()
                #dessiner joueur
                self.joueur.dessiner(self.ecran)
            
                                
                #update screen
                pygame.display.update()

                #vérifier collision
                if self.joueur.collisionavecsprites(Canyon.parois):
                    self.jeuactif=False
                    self.joueur.vies-=1
                    if self.joueur.vies>0:
                        self.ecrancollision=True
                        self.joueur.direction=0#plus de déplacement
                    else:
                        self.jeuactif=False
                        self.findepartie=True
                    break

                #control fps       
                self.tempsPasse=self.clock.tick(60)


                #test touches
                for event in pygame.event.get():
            
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_LEFT:
                            self.joueur.direction=-1
                            #print('déplacement gauche')
                        if event.key==pygame.K_RIGHT:
                            self.joueur.direction=1
                            #print('déplacement droite')
                        if event.key==pygame.K_ESCAPE:
                            self.quitter_jeu()

                    if event.type==pygame.KEYUP:
                        if event.key==pygame.K_LEFT:
                            self.joueur.direction=0
                            #print('pas de déplacement')
                        if event.key==pygame.K_RIGHT:
                            self.joueur.direction=0
                            #print('pas de déplacement')
                            
                    if event.type==pygame.QUIT:
                        self.quitterjeu()

            
            if self.ecrancollision:
                print("collision")
                print("Il reste {} vie(s)".format(self.joueur.vies))
                
                #mesurer le délai depuis la collision à partir de maintenant
                self.clockcollision.tick()
                self.delaicollision=0
                
                while self.delaicollision<self.delaicollisionmaximum:
                    self.delaicollision+=self.clockcollision.tick()
                    
                    """
                    OPTIONNEL : clignotement du joueur
                    """
                self.reset()    
                self.ecrancollision=False
                self.jeuactif=True
                
                                
            
            if self.findepartie:
                print("fin de partie")
                self.quitterjeu()
        
                    
            
    def quitterjeu(self):
        pygame.quit()
        sys.exit()
        
        



#démarrage du module
if __name__=="__main__":
    largeurecran=800
    hauteurecran=600
           
    moteurJeu=MoteurJeu(largeurecran,hauteurecran,"Sea canyon !")
    moteurJeu.joueur=Joueur(largeurecran/2,hauteurecran/2,"squidred.png",3)
    moteurJeu.canyon=Canyon("wall.png")
    
    moteurJeu.boucle_principale()
