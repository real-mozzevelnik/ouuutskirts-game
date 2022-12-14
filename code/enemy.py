import pygame
from math import sin
from particles import AnimationPlayer

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, images, enemy_type, visible_sprites):
        super().__init__()
        self.all_images = images

        for index, image in enumerate(self.all_images):
            image = pygame.transform.scale(image, (64,64))
            self.all_images[index] = image

        self.image = self.all_images[0]
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.side = 'right'
        self.display_surface = display_surface
        self.enemy_type = enemy_type

        # stats
        self.speed = 2
        self.health = 80

        # animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_player = AnimationPlayer()
        self.visible_sprites = visible_sprites

        self.can_be_attacked = True
        self.can_be_attacked_cooldown = 400
        self.attacked_time = 0

    def move(self):
        self.direction.x = self.speed
        self.rect.x += self.direction.x

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.animation_player.create_particles(f'{self.enemy_type}_death', (self.rect.centerx, self.rect.centery), self.visible_sprites)

    def animate(self):
        if self.side == 'right':
            self.image = self.all_images[int(self.frame_index)]
        else:
            self.image = self.all_images[int(self.frame_index)]
            self.image = pygame.transform.flip(self.image, True, False)
        if self.frame_index >= len(self.all_images)-1:
            self.frame_index = 0
        self.frame_index += self.animation_speed

        if not self.can_be_attacked:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    @staticmethod
    def wave_value():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_be_attacked:
            if current_time - self.attacked_time >= self.can_be_attacked_cooldown + 200:
                self.can_be_attacked = True

    def update(self, shift_speed):
        self.rect.x += shift_speed
        self.move()
        self.check_death()
        self.animate()
        self.cooldowns()