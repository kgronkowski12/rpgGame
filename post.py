from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    world_csv = []
    with open(path) as level_csv:
        layout = reader(level_csv,delimiter = ',')
        for row in layout:
            world_csv.append(list(row))
        return world_csv
    


def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
