import pygame
from support import import_folder
from file_path import res

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.pos = pos
        self.display_surface = display_surface
        self.all_images = import_folder(res('../graphics/tiles/silver'))
        self.image = self.all_images[0]
        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):
        if self.frame_index >= len(self.all_images):
            self.frame_index = 0
        self.image = self.all_images[int(self.frame_index)]
        self.frame_index += self.animation_speed

    def update(self, shift_speed):
        self.rect.x += shift_speed
        self.animate()