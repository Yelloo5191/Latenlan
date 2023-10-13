import pygame

from .util import display
from .config import colors


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
        # health bar
        pygame.draw.rect(display, colors[0],
                         (self.x, self.y, self.width, self.height))
        pygame.draw.rect(display, self.color, (self.x, self.y,
                         self.width * (self.health / self.max_health), self.height))

        # outlines
        pygame.draw.rect(display, (150, 150, 150),
                         (self.x, self.y, self.width, self.height), 1)

    def update(self, health):
        self.health = health
        self.draw()
