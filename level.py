import pygame
from enemy import Enemy, Stoper
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        # sprites
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.stoppers = pygame.sprite.Group()

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
                    self.visible_sprites.add(tile)
                    self.obstacle_sprites.add(tile)
                if col == 'p':
                    player = Player((x,y), self.display_surface, self.tiles)
                    self.player.add(player)
                if col == 'e':
                    enemy = Enemy((x,y),self.display_surface, self.tiles)
                    self.visible_sprites.add(enemy)
                if col == 's':
                    stopper = Stoper((x,y))
                    self.visible_sprites.add(stopper)
                    self.stoppers.add(stopper)

    # I hate this method, that's insane
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x

        for sprite in self.obstacle_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0 and player.side == 'left':
                    player.rect.left = sprite.rect.right
                    if not player.on_ground and not player.in_air:
                        player.on_wall = True
                    else:
                        player.on_wall = False

                elif player.direction.x > 0 and player.side == 'right':
                    player.rect.right = sprite.rect.left
                    if not player.on_ground and not player.in_air:
                        player.on_wall = True
                    else:
                        player.on_wall = False

                player.in_air = False

            if player.on_ground:
                player.on_wall = False
                player.in_air = False

            collide = pygame.sprite.spritecollideany(player, self.obstacle_sprites)
            if collide:
                player.in_air = False

    # I hate this method, that's insane
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.gravity()

        for sprite in self.obstacle_sprites.sprites():
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
        self.visible_sprites.update(self.shift_speed)
        self.visible_sprites.draw(self.display_surface)
        self.shift_x()


        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

