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

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 and player.side == 'left':
                    player.rect.left = sprite.rect.right

                elif player.direction.x > 0 and player.side == 'right':
                    player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        if player.direction.y != 0:
            player.on_ground = False

    def shift_x(self):
        player = self.player.sprite
        if player.rect.x >= (SCREEN_WIDTH/4) * 3 and player.side == 'right':
            self.shift_speed = -5
            player.speed = 0.0000001

        elif player.rect.x <= SCREEN_WIDTH/4 and player.side == 'left':
            self.shift_speed = 5
            player.speed = 0.00000001

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
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

