import pygame
from settings import *
from support import print_text

class Dialog(pygame.sprite.Sprite):
    def __init__(self, text, display_surface, sprite_to_kill, stat, go_next=False):
        super().__init__()
        self.texts = text
        self.stat = stat
        self.go_next = go_next
        self.display_surface = display_surface
        self.sprite_to_kill = sprite_to_kill
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT/3))
        self.image.set_alpha(200)
        self.rect = self.image.get_rect(topleft = (0, (SCREEN_HEIGHT*2)/3))

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.sprite_to_kill.kill()
            self.kill()

    def text(self):
        start_y = (SCREEN_HEIGHT*2)/3 + 5
        for index, text in enumerate(self.texts):
            x = 20
            y = start_y + 30*index
            print_text((x,y),text, 20, self.display_surface)
        print_text((480,670),'PRESS ENTER', 20, self.display_surface)

    def go_to_next_level(self):
        self.stat.level_num = self.stat.level_num[:-1] + str(int(self.stat.level_num[-1]) + 1)
        self.stat.stat_now = 'new_level'

    # def update(self, shift_speed):
    #     self.rect.x += shift_speed

    # def update_if_active(self):
    def update(self):
        self.input()
        self.text()

    def __del__(self):
        self.stat.dialog_num += 1
        if self.go_next:
            self.go_to_next_level()