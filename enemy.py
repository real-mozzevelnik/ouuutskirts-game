import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, tiles):
        super().__init__()
        self.image = pygame.Surface((TILESIZE//2, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill('white')
        self.direction = pygame.math.Vector2(0,0)

        self.speed = 5

    def update(self, shift_speed):
        self.rect.x += shift_speed

class Stoper(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((TILESIZE // 2, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift_speed):
        self.rect.x += shift_speed