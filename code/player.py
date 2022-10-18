import pygame
from math import sin
from particles import AnimationPlayer
from file_path import res

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, create_attack, visible_sprites, play_ultra, desrtoy_boxes, stat):
        super().__init__()
        self.pos = pos
        self.display_surface = display_surface

        # sounds
        self.weapon_attack_sound = pygame.mixer.Sound(res('../sounds/attack.wav'))
        self.weapon_attack_sound.set_volume(0.5)
        self.jump_sound = pygame.mixer.Sound('../sounds/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.fire_sound = pygame.mixer.Sound(res('../sounds/fire.wav'))
        self.fire_sound.set_volume(0.5)

        # player stats
        self.speed = 5
        self.side = None
        self.gravity_speed = 0.8
        self.on_ground = True
        self.on_wall = False
        self.in_air = False
        self.jump_speed = -20
        self.health = 100
        self.ultra = 0
        self.ultra_max = 10

        # game stat
        self.stat = stat

        # animation
        self.frame_index = 0
        self.animation_speed = 0.15
        self.side = 'right'
        self.running = False
        self.animation_player = AnimationPlayer()

        self.player_running_animations = {
            '0': pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/running/0.png')).convert_alpha(),
            '1': pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/running/1.png')).convert_alpha(),
            '2': pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/running/2.png')).convert_alpha(),
            '3': pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/running/3.png')).convert_alpha(),
            '4': pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/running/4.png')).convert_alpha()}
        self.player_on_wall_animation = pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/on_wall/0.png')).convert_alpha()
        self.player_jumping_animation = pygame.image.load(res(f'../graphics/player/{self.stat.level_num}/jump/0.png')).convert_alpha()

        # basic setup
        self.image = self.player_running_animations['0']
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)

        self.create_attack = create_attack
        self.visible_sprites = visible_sprites
        self.play_ultra = play_ultra
        self.destroy_boxes = desrtoy_boxes

        # cooldowns
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = 0

        self.can_be_attacked = True
        self.can_be_attacked_cooldown = 400
        self.attacked_time = 0

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
            self.jump_sound.play()

        elif keys[pygame.K_c] and self.can_attack:
            self.weapon_attack_sound.play()
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()
            self.destroy_boxes()
            self.can_attack = False
            if self.side == 'right':
                self.animation_player.create_particles('attack_right', (self.rect.x + 98, self.rect.y + 32)
                                                       , self.visible_sprites, player_attack=True, player_rect = self.rect, player_side='right')
            else:
                self.animation_player.create_particles('attack_left', (self.rect.x - 66, self.rect.y + 32)
                                                       ,self.visible_sprites, player_attack=True, player_rect = self.rect, player_side='left')

        elif keys[pygame.K_LCTRL]:
            if self.ultra == self.ultra_max:
                self.play_ultra()
                self.ultra = 0
                self.fire_sound.play()

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

        if not self.can_be_attacked:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

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

        if not self.can_be_attacked:
            if current_time - self.attacked_time >= self.can_be_attacked_cooldown + 400:
                self.can_be_attacked = True

    @staticmethod
    def wave_value():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.if_in_air()
        self.if_on_wall()
        self.slow_gravity_if_on_wall()
        self.input()
        self.animate_all()
        self.cooldowns()