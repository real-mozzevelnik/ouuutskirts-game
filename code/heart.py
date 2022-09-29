import pygame
from support import import_cut_graphics
from file_path import res

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.pos = pos
        self.display_surface = display_surface
        self.all_images = import_cut_graphics(res('../graphics/tiles/Big Heart Idle (18x14).png'), 14, heart=4)
        self.convert_images()
        self.image = self.all_images[0]
        self.rect = self.image.get_rect(topleft=pos)
        print(self.all_images)

    def animate(self):
        if self.frame_index >= len(self.all_images)-2:
            self.frame_index = 0
        self.image = self.all_images[int(self.frame_index)]
        self.frame_index += self.animation_speed

    def convert_images(self):
        for index, image in enumerate(self.all_images):
            self.all_images[index] = pygame.transform.scale(image,(32,32))

    def update(self, shift_speed):
        self.rect.x += shift_speed
        self.animate()