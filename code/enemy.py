import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, image):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(self.image, (64,64))
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)

        self.speed = -2

    def move(self):
        self.direction.x = self.speed
        self.rect.x += self.direction.x

    def update(self, shift_speed):
        self.rect.x += shift_speed
        self.move()
