import pygame
from settings import TILESIZE
from tile import Tile
from support import import_csv_layout, import_cut_graphics
from file_path import res
from support import print_text

class Boss:
    def __init__(self, screen):
        self.display_surface = screen
        self.create_map()
        pygame.mouse.set_visible(False)
        self.check_collides = True

    def create_map(self):
        layouts = {
            'terrain': import_csv_layout(res('../level/boss/boss_terrain.csv')),
            'player': import_csv_layout(res('../level/boss/boss_player.csv')),
            'reach': import_csv_layout(res('../level/boss/boss_reach.csv')),
            'screamer': import_csv_layout(res('../level/boss/boss_screamer.csv')),
        }
        obstacles = import_cut_graphics(res('../graphics/tiles/terrain_tiles/level_4.png'))
        screamer = pygame.image.load(res('../graphics/tiles/crate.png')).convert_alpha()
        screamer.set_alpha(0)
        reach = import_cut_graphics(res('../graphics/tiles/terrain_tiles/level_3.png'))
        player = pygame.image.load(res('../graphics/boss_player.png')).convert_alpha()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.screamer_image = pygame.image.load(res('../graphics/screamer.jpg')).convert_alpha()
        self.screamer_image = pygame.transform.scale(self.screamer_image, (1200,704))

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'terrain':
                            tile = Tile((x,y), self.display_surface, obstacles[int(col)], 'terrain')
                            self.visible_sprites.add(tile)
                            self.obstacle_sprites.add(tile)
                        if style == 'player':
                            self.player = Tile((x,y), self.display_surface, player, 'terrain')
                            self.start_x = x
                            self.start_y = y
                            self.player.image.fill('white')
                            self.visible_sprites.add(self.player)
                        if style == 'screamer':
                            self.screamer = Tile((x,y), self.display_surface, screamer, 'terrain')
                            self.visible_sprites.add(self.screamer)
                        if style == 'reach':
                            tile = Tile((x, y), self.display_surface, reach[int(col)], 'terrain')
                            self.visible_sprites.add(tile)

    def move(self):
        self.player.rect.x = pygame.mouse.get_pos()[0]
        self.player.rect.y = pygame.mouse.get_pos()[1]

    def collide(self):
        for sprite in self.obstacle_sprites.sprites():
            if self.player.rect.colliderect(sprite.rect):
                self.player.rect.x = self.start_x
                self.player.rect.y = self.start_y
                pygame.mouse.set_pos(self.start_x, self.start_y)

    def collide_screamer(self):
        if self.player.rect.colliderect(self.screamer):
            self.run_screamer()

    def run_screamer(self):
        self.check_collides = False
        pygame.mouse.set_visible(True)
        self.display_surface.blit(self.screamer_image, (0,0))
        print_text((270,100), 'Марго остался без пива', 60, self.display_surface)

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update(0)
        if self.check_collides:
            self.move()
            self.collide()
        self.collide_screamer()


