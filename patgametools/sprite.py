import pygame

class Sprite():
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.surface=pygame.image.load(image).convert_alpha()
        print("surface rect : {}".format(self.surface.get_rect()))
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
        
    def setanimation(self,animation):
        self.animation=animation
        self.subsurfacenr=0
        self.maxsubsurfaces=len(self.surfacedict[animation])
        
    def dessiner(self,surface):
        
        #print("subsurfacenr:{}".format(self.subsurfacenr))
        #print(self.surfacedict[self.animation][self.subsurfacenr])
        
        surface.blit(self.surfacedict[self.animation][self.subsurfacenr],self.rect.topleft)
        
        self.count+=1
        #print("count: {}".format(self.count))
        if self.count>self.maxcount:
            #print("maxcount atteint")
            self.count=0
            self.subsurfacenr+=1
            if self.subsurfacenr>self.maxsubsurfaces-1:
                self.subsurfacenr=0
     
    def creersurfacedict(self):
        for nomdict in self.rectdict:
            listsurfaces=[]
            for rect in self.rectdict[nomdict]:
                print(rect)
                listsurfaces.append(self.surface.subsurface(rect))
            print(listsurfaces)
            self.surfacedict[nomdict]=listsurfaces
            
            
            