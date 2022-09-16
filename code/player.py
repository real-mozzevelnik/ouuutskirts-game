import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, create_attack):
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
        self.health = 100

        # animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.side = 'right'
        self.running = False

        self.player_running_animations = {
            '0': pygame.image.load('../graphics/player/running/0.png').convert_alpha(),
            '1': pygame.image.load('../graphics/player/running/1.png').convert_alpha(),
            '2': pygame.image.load('../graphics/player/running/2.png').convert_alpha(),
            '3': pygame.image.load('../graphics/player/running/3.png').convert_alpha(),
            '4': pygame.image.load('../graphics/player/running/4.png').convert_alpha()}
        self.player_on_wall_animation = pygame.image.load('../graphics/player/on_wall/0.png').convert_alpha()
        self.player_jumping_animation = pygame.image.load('../graphics/player/jump/0.png').convert_alpha()

        # basic setup
        self.image = self.player_running_animations['0']
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)

        self.create_attack = create_attack

        # cooldowns
        self.can_attack = False
        self.attack_cooldown = 400
        self.attack_time = 0

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
        elif keys[pygame.K_c] and self.can_attack:
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.can_attack = False

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

    def animate_all(self):
        if self.running and not self.on_wall and not self.in_air:
            self.animate_run()

        elif self.on_wall and not self.on_ground and not self.in_air:
            if self.side == 'right':
                self.image = self.player_on_wall_animation
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = self.player_on_wall_animation

        elif self.in_air:
            if self.side == 'right':
                self.image = self.player_jumping_animation
            else:
                self.image = self.player_jumping_animation
                self.image = pygame.transform.flip(self.image, True, False)

        elif not self.running and not self.on_wall and not self.in_air:
            if self.side == 'right':
                self.image = self.player_running_animations['0']
            else:
                self.image = self.player_running_animations['0']
                self.image = pygame.transform.flip(self.image, True, False)

    def animate_run(self):
        if self.side == 'right':
            self.image = self.player_running_animations[str(int(self.frame_index))]
        else:
            self.image = self.player_running_animations[str(int(self.frame_index))]
            self.image = pygame.transform.flip(self.image, True, False)
        if self.frame_index >= 4.5:
            self.frame_index = 0
        self.frame_index += self.animation_speed

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown + 200:
                self.can_attack = True

    def update(self):
        self.if_in_air()
        self.if_on_wall()
        self.slow_gravity_if_on_wall()
        self.input()
        self.animate_all()
        self.cooldowns()