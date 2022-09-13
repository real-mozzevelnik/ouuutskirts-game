import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.pos = pos
        self.display_surface = display_surface
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill('gray')

    def update(self, shift_speed):
        self.rect.x += shift_speed