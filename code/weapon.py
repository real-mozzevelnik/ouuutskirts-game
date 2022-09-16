import pygame
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.image = pygame.image.load('../graphics/weapon/rythm.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64,32))
        self.right_image = self.image
        self.left_image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(topleft=(self.player.rect.x+10, self.player.rect.y+15))
        self.direction = pygame.math.Vector2(0, 0)

    def update(self):
        if self.player.side == 'right':
            self.image = self.right_image
            self.rect.x = self.player.rect.x+10
            self.rect.y = self.player.rect.y + 15
        elif self.player.side == 'left':
            self.image = self.left_image
            self.rect.x = self.player.rect.x-40
            self.rect.y = self.player.rect.y + 15

