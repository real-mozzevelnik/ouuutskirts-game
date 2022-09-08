import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.pos = pos
        self.display_surface = display_surface

        # player stats
        self.speed = 5
        self.side = None
        self.gravity_speed = 0.8
        self.on_ground = True

        # test visibility
        self.image = pygame.Surface((TILESIZE//2, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill('red')
        self.direction = pygame.math.Vector2(0,0)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
            self.side = 'left'

        elif keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
            self.side = 'right'

        else:
            self.direction.x = 0
            self.side = None

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def gravity(self):
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = -20

    def update(self):
        self.input()