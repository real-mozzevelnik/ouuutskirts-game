import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, tiles):
        super().__init__()
        self.image = pygame.Surface((TILESIZE//2, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill('white')
        self.direction = pygame.math.Vector2(0,0)

        self.speed = -2

    def move(self):
        self.direction.x = self.speed
        self.rect.x += self.direction.x

    def update(self, shift_speed):
        self.rect.x += shift_speed
        self.move()

class Stopper(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('../graphics/stopper.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift_speed):
        self.rect.x += shift_speed