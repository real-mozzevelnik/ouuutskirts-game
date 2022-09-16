import pygame
from enemy import Enemy
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from support import import_csv_layout, import_cut_graphics, import_folder

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
        self.player_attack_animation = import_folder('../graphics/particles/slash')

        # animations
        self.animation_speed = 0.15

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
        enemy_image = pygame.image.load('../graphics/tiles/Spooky ghost 1.png').convert_alpha()
        box_image = pygame.image.load('../graphics/tiles/crate.png').convert_alpha()
        obstacles = import_cut_graphics('../graphics/tiles/terrain_tiles.png')
        door_image = import_cut_graphics('../graphics/tiles/door.png', 46)
        stopper_image = pygame.image.load('../graphics/stopper.png').convert_alpha()
        background_image = pygame.image.load('../graphics/tiles/background.png').convert_alpha()

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
                            enemy = Enemy((x,y), self.display_surface, enemy_image)
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
                enemy.speed = -enemy.speed
                enemy.image = pygame.transform.flip(enemy.image, True, False)

    def damage_player(self):
        player = self.player.sprite
        if pygame.sprite.spritecollideany(player, self.enemies):
            player.health -= 15
            print(player.health)

    def create_attack(self):
        for enemy in self.enemies:
            if -100<=self.player.sprite.rect.x - enemy.rect.x<=100 and -30<=self.player.sprite.rect.y - enemy.rect.y<=30:
                self.run_player_attack_animation(enemy)

    def run_player_attack_animation(self, enemy):
        tile = Tile((enemy.rect.x, enemy.rect.y), self.display_surface, self.player_attack_animation[0], 'player_attack')
        self.visible_sprites.add(tile)
        frame_index = 0
        while True:
            if frame_index <= 3.5:
                frame_index += self.animation_speed
                tile.image = self.player_attack_animation[int(frame_index)]
            else:
                tile.kill()
                break

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

        # enemies
        self.change_enemy_side()

        # weapon
        self.weapon.update()
        if not self.player.sprite.on_wall:
            self.weapon.draw(self.display_surface)
