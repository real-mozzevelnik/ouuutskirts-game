from csv import reader
import pygame
from settings import *
from os import walk
from file_path import res

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path, TILESIZE=TILESIZE, heart = 0):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / TILESIZE)
	tile_num_y = int(surface.get_size()[1] / TILESIZE)

	cut_tiles = []
	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * (TILESIZE+heart) + heart
			y = row * TILESIZE
			new_surf = pygame.Surface((TILESIZE,TILESIZE),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,TILESIZE,TILESIZE))
			cut_tiles.append(new_surf)

	return cut_tiles

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return  surface_list

def print_text(pos, message, font_size, display, color = 'white'):
    FONT = pygame.font.Font(res('../graphics/tiles/Kurland.ttf'), font_size)
    text = FONT.render(message, False, color)
    display.blit(text, pos)
