import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, tiles):
        super().__init__()
        self.pos = pos
        self.display_surface = display_surface

        # player stats
        self.speed = 5
        self.side = None
        self.gravity_speed = 0.8
        self.on_ground = True
        self.on_wall = False
        self.in_air = False
        self.jump_speed = -20

        # test visibility
        self.image = pygame.Surface((TILESIZE//2, TILESIZE))
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill('red')
        self.direction = pygame.math.Vector2(0,0)

        self.tiles = tiles

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

        if keys[pygame.K_SPACE] and (self.on_ground or self.on_wall):
            self.jump()

    def gravity(self):
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed


    def if_in_air(self):
        if self.direction.y < 0:
            self.in_air = True

    def if_on_wall(self):
        if self.in_air:
            self.on_wall = False

    def slow_gravity_if_on_wall(self):
        if self.on_wall:
            self.gravity_speed = 0.1
            self.jump_speed = -15
        else:
            self.gravity_speed = 0.8
            self.jump_speed = -20

    def update(self):
        self.if_in_air()
        self.if_on_wall()
        self.slow_gravity_if_on_wall()
        self.input()