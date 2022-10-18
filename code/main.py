import pygame, sys
from tkinter import messagebox
from settings import *
from level import Level
from file_path import res
from death_screen import Death_screen
from show_next_level import Show_next_level
from boss import Boss

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('ouuutskirts')

class Stat():
    def __init__(self):
        self.stat_now = 'run'
        self.level_num = 'level_1'
        self.dialog_num = 1
        self.dialog_num_after_death = 1

class Game:
    def __init__(self):
        self.stat = Stat()
        self.level = Level(screen, self.stat)
        self.death_screen = Death_screen(screen, self.stat)
        self.show_next_level = Show_next_level(screen, self.stat)
        self.clock = pygame.time.Clock()
        self.main_sound = pygame.mixer.Sound(res('../sounds/main.ogg'))
        self.main_sound.set_volume(0.5)
        self.main_sound.play(loops=-1)

    def check_stat(self):
        if self.stat.stat_now == 'run':
            self.level.run()
        elif self.stat.stat_now == 'death':
            self.level = None
            self.level = Level(screen, self.stat)
            self.stat.dialog_num = self.stat.dialog_num_after_death
            self.stat.stat_now = 'death_screen'
        elif self.stat.stat_now == 'death_screen':
            self.death_screen.run()
        elif self.stat.stat_now == 'new_level':
            self.level = None
            if self.stat.level_num == 'level_5':
                self.boss = Boss(screen)
            else:
                self.level = Level(screen, self.stat)
            self.stat.stat_now = 'show_next_level'
            self.stat.dialog_num_after_death = self.stat.dialog_num
        elif self.stat.stat_now == 'show_next_level':
            self.show_next_level.run()
        elif self.stat.stat_now == 'boss':
            self.boss.run()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.stat.stat_now == 'boss':
                        messagebox.showinfo(title='конец', message='Спасибо за игру!')
                    pygame.quit()
                    sys.exit()

            screen.fill('black')
            self.check_stat()
            pygame.display.update()
            self.clock.tick(60)
            # print(self.stat.level_num)

if __name__=='__main__':
    game = Game()
    game.run()


