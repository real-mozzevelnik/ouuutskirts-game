import pygame
from support import print_text

class Death_screen():
    def __init__(self, display_surface, stat):
        self.display_surface = display_surface
        self.stat = stat

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            self.stat.stat_now = 'run'

    def run(self):
        self.input()
        print_text((370, 270), 'YOU ARE DEAD', 60, self.display_surface, color='red')
        print_text((520, 670), 'PRESS ENTER', 20, self.display_surface, color='red')