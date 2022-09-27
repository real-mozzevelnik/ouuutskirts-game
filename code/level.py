import pygame
from enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from support import import_csv_layout, import_cut_graphics, import_folder
from particles import AnimationPlayer
import random
from ui import UI
from file_path import res
from heart import Heart

class Level:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        # sprites
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.stoppers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.ui = pygame.sprite.GroupSingle()
        self.grass = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()
        self.coins_score = 0

        self.create_map()
        self.shift_speed = 0

        # weapon
        weapon = Weapon(self.player.sprite)
        self.weapon = pygame.sprite.GroupSingle()
        self.weapon.add(weapon)

        # animations
        self.animation_speed = 0.15
        self.animation_player = AnimationPlayer()

        # ui
        self.ui_menu = UI(self.player.sprite.health, self.display_surface, self.player.sprite)
        self.ui.add(self.ui_menu)

    def create_map(self):
        layouts = {
            'terrain': import_csv_layout(res('../level/level_1_csv/terrain.csv')),
            'box': import_csv_layout(res('../level/level_1_csv/box.csv')),
            'door': import_csv_layout(res('../level/level_1_csv/door.csv')),
            'coins': import_csv_layout(res('../level/level_1_csv/coins.csv')),
            'enemies': import_csv_layout(res('../level/level_1_csv/enemies.csv')),
            'stoppers': import_csv_layout(res('../level/level_1_csv/stoppers.csv')),
            'player': import_csv_layout(res('../level/level_1_csv/player.csv')),
            'grass': import_csv_layout(res('../level/level_1_csv/grass.csv'))}

        coin_image = pygame.image.load(res('../graphics/tiles/coin.png')).convert_alpha()
        box_image = pygame.image.load(res('../graphics/tiles/crate.png')).convert_alpha()
        obstacles = import_cut_graphics(res('../graphics/tiles/terrain_tiles.png'))
        door_image = import_cut_graphics(res('../graphics/tiles/door.png'), 46)
        stopper_image = pygame.image.load(res('../graphics/stopper.png')).convert_alpha()
        background_image = pygame.image.load(res('../graphics/tiles/background.png')).convert_alpha()
        grass_image = import_cut_graphics(res('../graphics/tiles/grass.png'))

        # enemies
        self.enemy_images = {
            'ghost': import_folder(res('../graphics/enemies/ghost')),
            'lich': import_folder(res('../graphics/enemies/lich'))
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
                        if style == 'terrain':
                            tile = Tile((x,y), self.display_surface, obstacles[int(col)], 'terrain')
                            self.obstacle_sprites.add(tile)
                            self.visible_sprites.add(tile)
                        if style == 'box':
                            y += 25
                            tile = Tile((x,y), self.display_surface, box_image, 'box')
                            self.obstacle_sprites.add(tile)
                            self.visible_sprites.add(tile)
                            self.boxes.add(tile)
                        if style == 'door':
                            y += 21
                            self.door = Tile((x,y), self.display_surface, door_image[0], 'door')
                            self.visible_sprites.add(self.door)
                        if style == 'coins':
                            tile = Tile((x,y), self.display_surface, coin_image, 'coin')
                            self.visible_sprites.add(tile)
                            self.coins.add(tile)
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
                            player = Player((x,y),self.display_surface, self.create_attack, self.visible_sprites,
                                            self.play_ultra, self.destroy_boxes)
                            self.player.add(player)
                        if style == 'grass':
                            tile = Tile((x,y), self.display_surface, grass_image[0], 'grass')
                            self.visible_sprites.add(tile)
                            self.grass.add(tile)

    # I hate this method, that's insane
    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x

        for sprite in self.obstacle_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    if not player.on_ground and not player.in_air and not pygame.sprite.spritecollideany(player,self.grass):
                        player.on_wall = True
                    else:
                        player.on_wall = False

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    if not player.on_ground and not player.in_air and not pygame.sprite.spritecollideany(player,self.grass):
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

    def create_attack(self):
        for enemy in self.enemies:
            if 0 <= self.player.sprite.rect.x - enemy.rect.x <= 200 and -64 <= self.player.sprite.rect.y - enemy.rect.y <= 64\
                    and self.player.sprite.side == 'left'or -200 <= self.player.sprite.rect.x - enemy.rect.x <= 0\
                    and -64 <= self.player.sprite.rect.y - enemy.rect.y <= 64 and self.player.sprite.side == 'right':
                enemy.health -= 20
                enemy.can_be_attacked = False
                enemy.attacked_time = pygame.time.get_ticks()

    def destroy_boxes(self):
        for box in self.boxes.sprites():
            if 0 <= self.player.sprite.rect.x - box.rect.x <= 150 and -64 <= self.player.sprite.rect.y - box.rect.y <= 64 \
                    and self.player.sprite.side == 'left' or -150 <= self.player.sprite.rect.x - box.rect.x <= 0 \
                    and -64 <= self.player.sprite.rect.y - box.rect.y <= 64 and self.player.sprite.side == 'right':
                box.kill()
                heart = Heart((box.rect.x,box.rect.y), self.display_surface)
                self.hearts.add(heart)
                self.visible_sprites.add(heart)

    def dont_go_out_of_screen(self):
        player = self.player.sprite
        if player.rect.y <= -10:
            player.rect.y = -9

        if player.rect.x >= (SCREEN_WIDTH/4) * 3:
            player.rect.x = (SCREEN_WIDTH/4) * 3

        if player.rect.x <= SCREEN_WIDTH/4:
            player.rect.x = SCREEN_WIDTH/4

    def get_coins(self):
        player = self.player.sprite
        for coin in self.coins.sprites():
            if coin.rect.colliderect(player.rect):
                self.coins_score += 1
                coin.kill()
                if player.ultra<player.ultra_max:
                    player.ultra+=1

    def play_ultra(self):
        for sprite in self.enemies.sprites():
            if 0<=sprite.rect.x<=SCREEN_WIDTH and 0<=sprite.rect.y<=SCREEN_HEIGHT:
                sprite.health -= 80
                self.animation_player.create_particles('ultra',(sprite.rect.centerx, sprite.rect.centery), self.visible_sprites)

    def add_hearts(self):
        player = self.player.sprite
        for heart in self.hearts.sprites():
            if player.rect.colliderect(heart.rect):
                heart.kill()
                player.health+=30
                if player.health > 100:
                    player.health = 100



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

        # ui
        self.ui.draw(self.display_surface)
        self.ui.update(self.player.sprite.health)

        # interactions
        self.get_coins()
        self.add_hearts()
