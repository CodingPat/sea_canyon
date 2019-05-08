import pygame
import patgametools.sprite as sprite

pygame.init()
ecran=pygame.display.set_mode((800,600))

mondict={"default":[(0,0,100,150),\
    (100,0,100,150),\
    (200,0,100,150),\
    (300,0,100,150),\
    (400,0,100,150)]
    }

mermaid=sprite.SpriteAnime(400,300,"mermaid.png",mondict,50)


clock=pygame.time.Clock()

while True:
    mermaid.dessiner(ecran)
    pygame.display.update()
    clock.tick(60)


    

