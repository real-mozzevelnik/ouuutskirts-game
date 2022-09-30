import pygame
from settings import *
from support import print_text

class Dialog(pygame.sprite.Sprite):
    def __init__(self, text, display_surface, dialog_place):
        super().__init__()
        self.texts = text
        self.display_surface = display_surface
        self.dialog_place = dialog_place
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT/3))
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(topleft = (0, (SCREEN_HEIGHT*2)/3))
        self.exist = True

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.exist = False
            self.dialog_place.sprite.kill()
            self.kill()

    def text(self):
        start_y = (SCREEN_HEIGHT*2)/3 + 5
        for index, text in enumerate(self.texts):
            x = 20
            y = start_y + 30*index
            print_text((x,y),text, 20, self.display_surface)
        print_text((480,670),'PRESS ENTER', 20, self.display_surface)

    def update(self):
        self.input()
        self.text()