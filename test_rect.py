import pygame,sys
from pygame.locals import *

pygame.init()
ecran=pygame.display.set_mode((800,600))

sprite=pygame.image.load('squidred.png').convert_alpha()
ecran.blit(sprite,(400,300))

myRect=sprite.get_rect()

print(myRect)

pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
