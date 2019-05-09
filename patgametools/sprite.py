import pygame

class Sprite():
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.dx=0
        self.dy=0
        self.surface=pygame.image.load(image).convert_alpha()
        self.hauteur=self.surface.get_height()
        self.largeur=self.surface.get_width()
        self.rect=pygame.rect.Rect(self.x,self.y,self.largeur,self.hauteur)
   
    
    def set_x(self,x):
        self.x=x
        self.rect.x=x
        
    def set_y(self,y):
        self.y=y
        self.rect.y=y
        
    def deplacer(self,dx,dy):
        self.x=self.x+dx
        self.y=self.y+dy
        self.rect.topleft=(self.x,self.y)
        
    def dessiner(self,surface):
        surface.blit(self.surface,self.rect.topleft)
        
            
    
    def collisionavecsprites(self,liste_sprites):
        collision=False
        for sprite in liste_sprites:
            if self.rect.colliderect(sprite.rect):
                collision=True
                break
        return collision

class SpriteAnime(Sprite):
    def __init__(self,x,y,image,rectdict,maxcount,animation="default"):
        print("SpriteAnime init")
        print("x,y : {},{}".format(x,y))
        print("image : {}".format(image))
        print("rectdict : {}".format(rectdict))
        print("maxcount : {}".format(maxcount))
        print("animation : {}".format(animation))
        
        Sprite.__init__(self,x,y,image)
        self.subsurfacenr=0
        self.maxsubsurfaces=0
        self.count=0
        self.maxcount=maxcount
        self.animation=animation
        self.rectdict=rectdict#{'default':[liste rects]}
        self.surfacedict={}
        self.creersurfacedict()
        self.setanimation(self.animation)
        self.estdelaianimation=False#existe-t-il un délai pour l'animation en cours ?
        self.delaiencoursanimation=None#temps déjà passé de l'animation 
        self.delaimaximumanimation=0#temps maximum pour l'animation
        self.horlogeanimation=None#horloge pour suivre le temps d'animation
        
        
    def setanimation(self,animation,delai=None):
        self.animation=animation
        self.subsurfacenr=0
        self.maxsubsurfaces=len(self.surfacedict[animation])
        self.set_surface()
        if delai:
            self.estdelaianimation=True
            self.delaiencoursanimation=0
            self.delaimaximumanimation=delai
            self.horlogeanimation=pygame.time.Clock()
        
    
    def set_surface(self):
        self.surface=self.surfacedict[self.animation][self.subsurfacenr]
        self.hauteur=self.surface.get_height()
        self.largeur=self.surface.get_width()
        self.rect=pygame.rect.Rect(self.x,self.y,self.largeur,self.hauteur)
    
    def dessiner(self,surface):
        
        #debug
        print("subsurfacenr:{}".format(self.subsurfacenr))
        print("animation:{},subsurface:{}".format(self.animation,self.surfacedict[self.animation][self.subsurfacenr]))
        print("surface:{}",self.surface)
        print("rect : {}", self.rect)
        surface.blit(self.surface,self.rect.topleft)
        
        #vérifier le timer d'animation. Si temps écoulé, basculer vers l'animation par défaut
        if self.estdelaianimation:
            self.delaiencoursanimation+=self.horlogeanimation.tick()
            if self.delaiencoursanimation>=self.delaimaximumanimation:
                self.setanimation("default")
                self.estdelaianimation=False
        
        
        
        #vérifier le nombre de frames avant de passer à l'image suivante
        self.count+=1
        #print("count: {}".format(self.count))
        if self.count>self.maxcount:
            #print("maxcount atteint")
            self.set_surface()
            self.count=0
            self.subsurfacenr+=1
            if self.subsurfacenr>self.maxsubsurfaces-1:
                self.subsurfacenr=0
     
    def creersurfacedict(self):
        for nomdict in self.rectdict:
            listsurfaces=[]
            for rect in self.rectdict[nomdict]:
                listsurfaces.append(self.surface.subsurface(rect))
            
            self.surfacedict[nomdict]=listsurfaces
        #debug
        print("création dictionnaire des surfaces")
        for key,value in self.surfacedict.items():
            print(key,value)
            
            
            
            
            