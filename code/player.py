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

        # animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.side = 'right'
        self.running = False

        self.player_running_animations = {
            '0': pygame.image.load('0.png').convert_alpha(),
            '1': pygame.image.load('1.png').convert_alpha(),
            '2': pygame.image.load('2.png').convert_alpha(),
            '3': pygame.image.load('3.png').convert_alpha(),
            '4': pygame.image.load('4.png').convert_alpha()
        }

        # test visibility
        self.image = self.player_running_animations['0']
        self.rect = self.image.get_rect(topleft = pos)
        #self.image.fill('red')
        self.direction = pygame.math.Vector2(0,0)

        self.tiles = tiles

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
            self.side = 'left'
            self.running = True

        elif keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
            self.side = 'right'
            self.running = True

        else:
            self.direction.x = 0
            self.running = False

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

    def if_running(self):
        if self.running and not self.on_wall and not self.in_air:
            self.animate()
        else:
            if self.side == 'right':
                self.image = self.player_running_animations['0']
            else:
                self.image = self.player_running_animations['0']
                self.image = pygame.transform.flip(self.image, True, False)


    def animate(self):
        if self.side == 'right':
            self.image = self.player_running_animations[str(int(self.frame_index))]
        else:
            self.image = self.player_running_animations[str(int(self.frame_index))]
            self.image = pygame.transform.flip(self.image, True, False)
        if self.frame_index >= 4.5:
            self.frame_index = 0
        self.frame_index += self.animation_speed

    def update(self):
        self.if_in_air()
        self.if_on_wall()
        self.slow_gravity_if_on_wall()
        self.input()
        self.if_running()