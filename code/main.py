import pygame, sys
from settings import *
from level import Level

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('ouuutskirts')
clock = pygame.time.Clock()
level = Level(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('green')
    level.run()
    pygame.display.update()
    clock.tick(60)



