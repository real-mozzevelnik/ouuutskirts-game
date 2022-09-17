import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # player attack
            'slash': import_folder('../graphics/particles/slash'),
            'ghost_death': import_folder('../graphics/particles/ghost_death'),
            'lich_death': import_folder('../graphics/particles/lich_death'),
            'attack_right': import_folder('../graphics/particles/level1_attack'),
            'attack_left': import_folder('../graphics/particles/level1_attack')
            }

        for index, frame in enumerate(self.frames['ghost_death']):
            frame = pygame.transform.scale(frame, (64,64))
            self.frames['ghost_death'][index] = frame

        for index, frame in enumerate(self.frames['lich_death']):
            frame = pygame.transform.scale(frame, (64,64))
            self.frames['lich_death'][index] = frame

        for index, frame in enumerate(self.frames['attack_left']):
            frame = pygame.transform.flip(frame, True, False)
            self.frames['attack_left'][index] = frame

    @staticmethod
    def reflect_images(frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups, player_attacking=False, animation_speed=0.25)

    def create_particles(self, animation_type, pos, groups, player_attack=False, player_rect=None, player_side=None):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups, player_attacking=player_attack, player_rect = player_rect, player_side=player_side)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, player_attacking, animation_speed = 0.18, player_rect=None, player_side=None):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.player_attack = player_attacking
        self.player_rect = player_rect
        self.player_side = player_side
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift_x):
        self.animate()
        if self.player_attack:
            if self.player_side == 'right':
                self.rect.centerx = self.player_rect.x + 98
                self.rect.centery = self.player_rect.y + 32
            else:
                self.rect.centerx = self.player_rect.x - 66
                self.rect.centery = self.player_rect.y + 32
