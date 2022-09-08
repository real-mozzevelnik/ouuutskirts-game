import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.level_setup()
        self.shift_speed = 0

    def level_setup(self):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for ceil_index, ceil in enumerate(test_level):
            for col_index, col in enumerate(ceil):
                x = col_index * TILESIZE
                y = ceil_index * TILESIZE
                if col == 'x':
                    tile = Tile((x,y), self.display_surface)
                    self.tiles.add(tile)
                if col == 'p':
                    player = Player((x,y), self.display_surface)
                    self.player.add(player)

    def player_move(self):
        player = self.player.sprite
        player.rect.x += player.direction.x

    def shift_x(self):
        player = self.player.sprite
        if player.rect.x >= (SCREEN_WIDTH/4) * 3 and player.side == 'right':
            self.shift_speed = -5
            player.speed = 0

        elif player.rect.x <= SCREEN_WIDTH/4 and player.side == 'left':
            self.shift_speed = 5
            player.speed = 0

        else:
            self.shift_speed = 0
            player.speed = 5


    def run(self):

        # tiles
        self.tiles.update(self.shift_speed)
        self.tiles.draw(self.display_surface)
        self.shift_x()


        # player
        self.player.update()
        self.player_move()
        self.player.draw(self.display_surface)

