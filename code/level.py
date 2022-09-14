import pygame
from enemy import Enemy, Stopper
from settings import *
from tile import Tile
from player import Player
from weapon import Weapon
from support import import_csv_layout

class Level:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        # sprites
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.stoppers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.level_setup()
        self.shift_speed = 0

        # weapon
        weapon = Weapon(self.player.sprite)
        self.weapon = pygame.sprite.GroupSingle()
        self.weapon.add(weapon)

        import_csv_layout('../level/level_1_csv/background_1.csv')


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
                    self.enemies.add(enemy)
                if col == 's':
                    stopper = Stopper((x,y))
                    self.visible_sprites.add(stopper)
                    self.stoppers.add(stopper)

    '''def create_map(self):
        layouts = {
            'background_1': import_csv_layout('../level/level_1_csv/background_1.csv'),
            'background_2': import_csv_layout('../level/level_1_csv/background_2.csv'),
            'background_3': import_csv_layout('../level/level_1_csv/background_3.csv'),
            'background_4': import_csv_layout('../level/level_1_csv/background_4.csv'),
            'background_5': import_csv_layout('../level/level_1_csv/background_5.csv'),
            'door': import_csv_layout('../level/level_1_csv/door.csv'),
            'coins': import_csv_layout('../level/level_1_csv/coins.csv'),
            'enemies': import_csv_layout('../level/level_1_csv/obstacles.csv')
        }

        images = 

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'background_1':
                            Tile((x, y), image)
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.obstacle_sprites, self.visible_sprites, self.attackable_sprites],
                                 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.obstacle_sprites, self.visible_sprites], 'object', surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites,
                                                     self.create_attack, self.destroy_attack, self.create_magic)
                            else:
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(monster_name, (x, y), [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites, self.damage_player, self.trigger_death_particles,
                                      self.add_exp)'''

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

        # enemies
        self.change_enemy_side()

        # weapon
        self.weapon.update()
        self.weapon.draw(self.display_surface)
