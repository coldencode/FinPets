import pandas as pd
import pygame
from furnitureloader import Furniture
from constants import TILE_SIZE, PLACEHOLDER

def create_furniture(name: str):
    df = pd.read_excel("data/furniture.xlsx")
    for index, row in df.iterrows():
        check_name = row['furniture_name']
        if name == check_name:
            image_path = row['image_path']
            offset_y = row['offset_y'] # If the furniture is calculated is 2 pixels, but is technically 1, (e.g. chair)
            offset_x = row['offset_x']
            # Load the image and scale it to fit the tile size
            image = pygame.image.load(image_path)
            preview = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
            return Furniture(name, image, preview, offset_y, offset_x)
        elif name == PLACEHOLDER:
            return PLACEHOLDER
