# button.py
import pygame
from constants import *

class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def is_clicked(self, pos):
        return self.is_hovered(pos) and pygame.mouse.get_pressed()[0]

class WoodenButton(Button):
    def __init__(self, x, y, width, height, text=None):
        # Set the path for the wooden button's image
        self.image = pygame.image.load(WOOD_BUTTON)  # Specify the path to the wooden button image
        super().__init__(x, y, width, height, None, text)
    
    def draw(self, screen, font):
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(self.image, (self.rect.x-31 , self.rect.y-18))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

class StreakButton(Button):
    def __init__(self, x, y, width, height, text=None):
        # Set the path for the wooden button's image
        self.image = pygame.image.load(STREAK_BUTTON)  # Specify the path to the wooden button image
        self.image = pygame.transform.scale(self.image, (50, 50))
        super().__init__(x, y, width, height, None, text)
    
    def draw(self, screen, font):
        screen.blit(self.image, (self.rect.x-31 , self.rect.y-18))

class LongButton(Button):
    def __init__(self, x, y, width, height, text=None):
        # Set the path for the wooden button's image
        self.image = pygame.image.load(LONG_WOOD_BUTTON)  # Specify the path to the wooden button image
        self.image = pygame.transform.scale(self.image, (200, 70))
        super().__init__(x, y, width, height, None, text)

    def draw(self, screen, font):
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(self.image, (self.rect.x - 31, self.rect.y - 18))
        screen.blit(text_surface, (self.rect.x + 45, self.rect.y + 13))