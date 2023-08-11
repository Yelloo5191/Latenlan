import pygame

from .util import display

class UI:

    def __init__(self):
        pass

    def draw(self):
        pass

class HealthBar(UI):

    def __init__(self, x, y, width, height, color, max_health, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.max_health = max_health
        self.health = health

    def draw(self):
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(display, self.color, (self.x, self.y, self.width * (self.health / self.max_health), self.height))
    
    def update(self, health):
        self.health = health
        self.draw()