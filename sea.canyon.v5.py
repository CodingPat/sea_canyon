import pygame,random,sys,time
import patgametools.sprite as sprite

from pygame.locals import *

class Joueur(sprite.Sprite):
    
    
    def __init__(self,x,y,image,vies=3):
        sprite.Sprite.__init__(self,x,y,image)
        self.dx=5
        self.direction=0 # 0=immobile 1=droite -1=gauche
        self.vies=3
        
        #gérer clignotment en cas de collision
        self.clock=pygame.time.Clock()
        self.delaidepuisclignotement=0#délai depuis dernier clignotement
        self.delailimiteclignotement=100#délai pour clignotement
        
    
    def reset_position(self):
        "redémarrer position initiale"
        #print("joueur reset_position")
        self.set_x(largeurecran/2)
        self.set_y(hauteurecran/2)
        
    def reset(self,vies=3):
        self.reset_position()
        self.vies=vies
        self.direction=0
    
    def miseajour(self):
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
                
        
        
    def dessiner(self):
        #print("dessiner - pas de collision")
        moteurJeu.ecran.blit(self.surface,self.rect.topleft)
        


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
        self.distance=0#km parcourus      
        self.reset_position()
    
    def reset(self):
        self.reset_position()
    
    def reset_position(self):
        Canyon.parois.clear()
        self.distance=0
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
        
            
    
    def miseajour(self):
                
        self.temps_cumule+=self.clock.tick()
        
        if self.temps_cumule>self.delai_creation:
            self.temps_cumule=0
            self.deplacerparois()
            self.effacerparoisinactives()
            self.creerparois()
            self.distance+=1
            
               
    def dessiner(self):
        for paroi in Canyon.parois:
            paroi.dessiner(moteurJeu.ecran)
                              
class BandeauScore():
    def __init__(self,margegauche=500,margehaut=20,font="arialblack",fontsize=15,color=(255,255,255)):
        self.margegauche=margegauche
        self.margehaut=margehaut
        self.font=pygame.font.SysFont(font,fontsize)
        self.color=color
        
        
    def miseajour(self):
        texte="Vies : {} Distance : {} km".format(moteurJeu.joueur.vies-1,str(moteurJeu.canyon.distance).rjust(8,'0'))
        self.surface=self.font.render(texte,True,self.color)
    
    def dessiner(self):
        #moteurJeu.blit()
        moteurJeu.ecran.blit(self.surface,(self.margegauche,self.margehaut))
    
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
        self.bandeauscore=None
        self.estfindepartie=False #ecran fin de partie
        self.estecrandemarrage=False #ecran demarrage
        self.estjeuactif=False #jeu demarre
        self.estecrancollision=False
        self.estjeuenpause=False #jeu pause
        
        
    def reset_position(self):
        #print("Moteur de jeu : reset_position")
        self.canyon.reset_position()
        self.joueur.reset_position()
        
    def reset_jeu(self):
        self.canyon.reset()
        self.joueur.reset()
        
        
    def ecrandemarrage(self):
        pass
    
    def jeudemarre(self):
        pass
    
    def jeupause(self):
        pass
    
    def findepartie(self):
                
        font1=pygame.font.SysFont("arialblack",48)
        font2=pygame.font.SysFont("arialblack",24)
        color=(255,0,0)
        titre1="GAME OVER "
        titre2="--- appuyer sur espace pour redémarrer ---"
        surfacetitre1=font1.render(titre1,True,color)
        largeurtitre1=surfacetitre1.get_width()
        hauteurtitre1=surfacetitre1.get_height()
        surfacetitre2=font2.render(titre2,True,color)
        largeurtitre2=surfacetitre2.get_width()
        hauteurtitre2=surfacetitre2.get_height()
        #self.ecran.fill((0,0,0)) 
        self.ecran.blit(surfacetitre1,((largeurecran-largeurtitre1)/2,hauteurecran/2-hauteurtitre1))
        self.ecran.blit(surfacetitre2,((largeurecran-largeurtitre2)/2,hauteurecran/2+hauteurtitre1))
        pygame.display.update()
                
        for event in pygame.event.get():
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    self.estfindepartie=False
                    self.estecrandemarrage=True
                            
                if event.key==pygame.K_ESCAPE:
                    self.quitterjeu()
            if event.type==pygame.QUIT:
                self.quitterjeu()

    
    
    def boucle_principale(self):
       
        self.estjeuactif=False
        self.estecrandemarrage=True
        
        while True:
            while self.estjeuactif:
                self.ecran.fill((0,0,0))#effacer écran
                #mises à jour
                self.joueur.miseajour()
                self.canyon.miseajour()
                self.bandeauscore.miseajour()                  
                #dessiner
                self.canyon.dessiner()
                self.joueur.dessiner()
                self.bandeauscore.dessiner()
                
                                
                #mise à jour écran
                pygame.display.update()

                #vérifier collision
                if self.joueur.collisionavecsprites(Canyon.parois):
                    self.estjeuactif=False
                    self.joueur.vies-=1
                    self.estecrancollision=True
                    self.joueur.direction=0#plus de déplacement
                    
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

            
            if self.estecrancollision:
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
                self.reset_position()    
                self.estecrancollision=False
                if not(self.joueur.vies>0):
                    self.estjeuactif=False
                    self.estfindepartie=True
                else:
                    self.estjeuactif=True
                
                                
            if self.estecrandemarrage:
                self.reset_jeu()
                font1=pygame.font.SysFont("arialblack",48)
                font2=pygame.font.SysFont("arialblack",24)
                color=(0,0,255)
                titre1="S E A  C A N Y O N "
                titre2="--- appuyer sur espace pour démarrer ---"
                surfacetitre1=font1.render(titre1,True,color)
                largeurtitre1=surfacetitre1.get_width()
                hauteurtitre1=surfacetitre1.get_height()
                surfacetitre2=font2.render(titre2,True,color)
                largeurtitre2=surfacetitre2.get_width()
                hauteurtitre2=surfacetitre2.get_height()
                self.ecran.fill((0,0,0))
                self.ecran.blit(surfacetitre1,((largeurecran-largeurtitre1)/2,hauteurecran/2-hauteurtitre1))
                self.ecran.blit(surfacetitre2,((largeurecran-largeurtitre2)/2,hauteurecran/2+hauteurtitre1))
                pygame.display.update()
                
                for event in pygame.event.get():
            
                    if event.type==pygame.KEYDOWN:
                        if event.key==pygame.K_SPACE:
                            self.estecrandemarrage=False
                            self.estjeuactif=True
                        if event.key==pygame.K_ESCAPE:
                            self.quitterjeu()
                    if event.type==pygame.QUIT:
                        self.quitterjeu()

            
            if self.estfindepartie:
                self.findepartie()
                    
            
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
    moteurJeu.bandeauscore=BandeauScore()
    moteurJeu.boucle_principale()
