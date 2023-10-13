import random
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


class Particle:
    def __init__(self, x, y, color, size, velocity):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.velocity = velocity
        self.lifetime = 0

    def draw(self):
        pygame.draw.circle(display, self.color,
                           (int(self.x), int(self.y)), self.size)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime += 1
        self.draw()


class GhoulDeath(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 255), 2, (0, 0))
        self.velocity = [
            random.randint(-5, 5) / 10, random.randint(-5, 5) / 10]
        self.lifetime = 0
        self.size = random.randint(0, 5)
        self.color = (110, 15, 255)

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime += 1
        self.size -= 0.1
        self.color = (self.color[0], self.color[1],
                      self.color[2], int(255 - (self.lifetime * 2.5)))
        self.draw()


class ProjectileHit(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, (255, 255, 255), 2, (0, 0))
        # particle for when a projectile hits a ghoul
        self.velocity = [
            random.randint(-5, 5) / 10, random.randint(-5, 5) / 10]
        self.lifetime = 0
        self.size = random.randint(0, 3)
        self.color = (150, 0, 200)

    def update(self):
        # make it more springy than ghoul daeth
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.lifetime += 1
        self.size -= 0.2
        self.color = (self.color[0], self.color[1],
                      self.color[2], int(255 - (self.lifetime)))
        self.draw()
