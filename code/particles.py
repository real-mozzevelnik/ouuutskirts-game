import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            # player attack
            'slash': import_folder('../graphics/particles/slash'),
            'ghost_death': import_folder('../graphics/particles/ghost_death'),
            'lich_death': import_folder('../graphics/particles/lich_death')
            }

        for index, frame in enumerate(self.frames['ghost_death']):
            frame = pygame.transform.scale(frame, (64,64))
            self.frames['ghost_death'][index] = frame

        for index, frame in enumerate(self.frames['lich_death']):
            frame = pygame.transform.scale(frame, (64,64))
            self.frames['lich_death'][index] = frame

    @staticmethod
    def reflect_images(frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups, 0.25)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, animation_speed = 0.18):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = animation_speed
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