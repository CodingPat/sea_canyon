import pygame
import patgametools.sprite as sprite

pygame.init()
ecran=pygame.display.set_mode((800,600))

inky=sprite.SpriteAnime(200,200,"squidred.png")
inky.dessiner(ecran)
pygame.display.update()

"""

clock=pygame.time.Clock()

while True:
    ecran.blit(inky,(400,200))
    pygame.display.update()
    clock.tick(60)
"""

    

