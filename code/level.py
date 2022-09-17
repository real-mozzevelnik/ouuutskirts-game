import pygame
from enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from support import import_csv_layout, import_cut_graphics, import_folder
from particles import AnimationPlayer
import random

class Level:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        # sprites
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.stoppers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.create_map()
        self.shift_speed = 0

        # weapon
        weapon = Weapon(self.player.sprite)
        self.weapon = pygame.sprite.GroupSingle()
        self.weapon.add(weapon)

        # animations
        self.animation_speed = 0.15
        self.animation_player = AnimationPlayer()

    def create_map(self):
        layouts = {
            'obstacles': import_csv_layout('../level/level_1_csv/obstacles.csv'),
            'box': import_csv_layout('../level/level_1_csv/box.csv'),
            'door': import_csv_layout('../level/level_1_csv/door.csv'),
            'coins': import_csv_layout('../level/level_1_csv/coins.csv'),
            'enemies': import_csv_layout('../level/level_1_csv/enemies.csv'),
            'stoppers': import_csv_layout('../level/level_1_csv/stoppers.csv'),
            'player': import_csv_layout('../level/level_1_csv/player.csv')}

        coin_image = pygame.image.load('../graphics/tiles/coin.png').convert_alpha()
        box_image = pygame.image.load('../graphics/tiles/crate.png').convert_alpha()
        obstacles = import_cut_graphics('../graphics/tiles/terrain_tiles.png')
        door_image = import_cut_graphics('../graphics/tiles/door.png', 46)
        stopper_image = pygame.image.load('../graphics/stopper.png').convert_alpha()
        background_image = pygame.image.load('../graphics/tiles/background.png').convert_alpha()

        # enemies
        self.enemy_images = {
            'ghost': import_folder('../graphics/enemies/ghost'),
            'lich': import_folder('../graphics/enemies/lich')
        }

        # background
        background = Tile((0,0),self.display_surface, background_image, 'background')
        self.visible_sprites.add(background)

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'obstacles':
                            tile = Tile((x,y), self.display_surface, obstacles[int(col)], 'obstacle')
                            self.obstacle_sprites.add(tile)
                            self.visible_sprites.add(tile)
                        if style == 'box':
                            y += 25
                            tile = Tile((x,y), self.display_surface, box_image, 'box')
                            self.obstacle_sprites.add(tile)
                            self.visible_sprites.add(tile)
                        if style == 'door':
                            y += 21
                            self.door = Tile((x,y), self.display_surface, door_image[0], 'door')
                            self.visible_sprites.add(self.door)
                        if style == 'coins':
                            tile = Tile((x,y), self.display_surface, coin_image, 'coin')
                            self.visible_sprites.add(tile)
                        if style == 'enemies':
                            enemy_type = random.choice(list(self.enemy_images.keys()))
                            enemy = Enemy((x,y), self.display_surface, self.enemy_images[enemy_type], enemy_type, self.visible_sprites)
                            self.enemies.add(enemy)
                            self.visible_sprites.add(enemy)
                        if style == 'stoppers':
                            tile = Tile((x,y), self.display_surface, stopper_image, 'stopper')
                            self.stoppers.add(tile)
                            self.visible_sprites.add(tile)
                        if style == 'player':
                            player = Player((x,y),self.display_surface, self.create_attack)
                            self.player.add(player)



    # I hate this method, that's insane
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x

        for sprite in self.obstacle_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    if not player.on_ground and not player.in_air:
                        player.on_wall = True
                    else:
                        player.on_wall = False

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    if not player.on_ground and not player.in_air:
                        player.on_wall = True
                    else:
                        player.on_wall = False

                player.in_air = False

            if player.on_ground:
                player.on_wall = False
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
        if player.rect.x >= (SCREEN_WIDTH/4) * 3 and player.direction.x > 0:
            self.shift_speed = -5
            player.speed = 0.0000001

        elif player.rect.x <= SCREEN_WIDTH/4 and player.direction.x < 0:
            self.shift_speed = 5
            player.speed = 0.00000001

        else:
            self.shift_speed = 0
            player.speed = 5

    def change_enemy_side(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollideany(enemy, self.stoppers):
                if enemy.speed > 0:
                    enemy.side = 'left'
                else:
                    enemy.side = 'right'
                enemy.speed = -enemy.speed

    def damage_player(self):
        player = self.player.sprite
        if pygame.sprite.spritecollideany(player, self.enemies) and player.can_be_attacked:
            player.can_be_attacked = False
            player.attacked_time = pygame.time.get_ticks()
            player.health -= 15
            self.animation_player.create_particles('slash', (player.rect.centerx, player.rect.centery),self.visible_sprites)
            print(player.health)

    def create_attack(self):
        for enemy in self.enemies:
            if -200<=self.player.sprite.rect.x - enemy.rect.x<=200 and -64<=self.player.sprite.rect.y - enemy.rect.y<=64:
                enemy.health -= 20
                self.animation_player.create_particles('slash',(enemy.rect.centerx,enemy.rect.centery), self.visible_sprites)

    def dont_go_out_of_screen(self):
        player = self.player.sprite
        if player.rect.y <= -10:
            player.rect.y = -9

        if player.rect.x >= (SCREEN_WIDTH/4) * 3:
            player.rect.x = (SCREEN_WIDTH/4) * 3

        if player.rect.x <= SCREEN_WIDTH/4:
            player.rect.x = SCREEN_WIDTH/4


    def run(self):

        # tiles
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(self.shift_speed)

        self.shift_x()


        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)
        self.damage_player()
        self.dont_go_out_of_screen()

        # enemies
        self.change_enemy_side()

        # weapon
        self.weapon.update()
        if not self.player.sprite.on_wall:
            self.weapon.draw(self.display_surface)
