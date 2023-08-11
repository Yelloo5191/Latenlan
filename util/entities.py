import pygame
import math

from .util import display

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage, image, direction):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
    
    def draw(self):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255, 0, 0), self.rect, 1)
    
    def update(self):
        self.x += math.cos(math.radians(self.direction)) * self.speed
        self.y += math.sin(math.radians(self.direction)) * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        self.draw()