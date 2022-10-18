import pygame
from support import print_text
from file_path import res

class Show_next_level():
    def __init__(self, display_surface, stat):
        self.display_surface = display_surface
        self.stat = stat

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            if self.stat.level_num == 'level_5':
                self.stat.stat_now = 'boss'
            else:
                self.stat.stat_now = 'run'

    def run(self):
        self.input()
        if self.stat.level_num == 'level_5':
            print_text((480, 270), f'BOSS'.upper(), 60, self.display_surface)
        else:
            print_text((480, 270), f'Level {self.stat.level_num[-1]}'.upper(), 60, self.display_surface)
        print_text((520, 670), 'PRESS ENTER', 20, self.display_surface)