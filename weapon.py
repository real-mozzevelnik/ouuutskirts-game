import pygame
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.image = pygame.Surface((TILESIZE, TILESIZE//4))
        self.rect = self.image.get_rect(topleft=(self.player.rect.x+32, self.player.rect.y//2))
        self.image.fill('blue')
        self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        self.rect.x = self.player.rect.x+32
        self.rect.y = self.player.rect.y + TILESIZE//2
